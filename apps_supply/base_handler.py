#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'binpo'


from common.base_handler import DistributorHandler,BaseHandler
from common.permission_control import distributor_user_authenticated,supply_user_authenticated

from services.locations.location_services import LocationServices
from services.orders.orders_services import OrderServices
from services.express.express_services import ExpressServices
from services.users.user_services import UserServices
from conf.orders_conf import ORDER_STAYUS,PAY_STATUS,DELIVERRY_STATUS,PAYMENT_STATUS
from services.payments.payorder_services import PayOrderService
from services.logs.logs_services import LogsServices
from models.orders_do import ItemOrders,Orders,PayOrders
from models.express_do import InvoiceOrders
from models.location_do import *
from models.user_do import *
from models.item_do import ItemDetail
from data_cache.express_company_cache import ExpressCompanyCache
import sys
import ujson
import os
from apps_drp.base_handler import DrpBaseHandler

order_service = OrderServices()
express_service = ExpressServices()
user_service = UserServices()
pay_service = PayOrderService()
location_service = LocationServices()
logs_service = LogsServices()


class SupplyBaseHandler(DistributorHandler):

    @distributor_user_authenticated
    @supply_user_authenticated
    def prepare(self):
        pass

    def get_distributors_by_id(self,id):
        '''
        获取分销商
        :param id:
        :return:
        '''
        drp = self.rdb.query(DistributorUser).filter(DistributorUser.id==id,
                                                      DistributorUser.parent_id==0,DistributorUser.role_type==0).scalar()


        if not drp:
            return ''
        else:
            return drp.real_name

    # def echo(self, template, context=None, globals=None,layout='admin_supply/base.html'):
    #     pass
#SupplyBaseHandler
class SupplyHomeHandler(SupplyBaseHandler):

    def get(self, *args, **kwargs):

        self.echo('admin_supply/index.html',layout='admin_supply/base.html')

class OrdersHandler(SupplyBaseHandler):

    def get(self, *args, **kwargs):

        order_service.set_rdb(self.rdb)
        user_service.set_rdb(self.rdb)
        self.get_paras_dict()
        start_date = self.qdict.get('start_date','')
        end_date = self.qdict.get('end_date','')
        pay_start_date = self.get_argument('pay_start_date','')
        pay_end_date = self.get_argument('pay_end_date','')
        order_no = self.qdict.get('order_no','')
        order_status = self.qdict.get('order_status','')
        pay_status = self.qdict.get('pay_status','')
        delivery_status = self.qdict.get('delivery_status','')

        supply_user_id = self.current_user.get('id')
        content = self.qdict.get('content','') #判断身份证号码，手机,订单号
        user_id = self.qdict.get('user_id','')
        query = order_service._list(user_id=user_id,supply_user_id=supply_user_id,start_date=start_date,end_date=end_date,
                                    order_no=order_no,content=content,pay_start_date=pay_start_date,
                                    pay_end_date=pay_end_date)
        if str(order_status):
            query = query.filter(Orders.status == order_status)
        if str(pay_status):
            query = query.filter(Orders.pay_status == pay_status)
        if str(delivery_status):
            query = query.filter(Orders.delivery_status == delivery_status)
        data = self.get_page_data(query)
        self.echo('admin_supply/orders.html',
                      {'data':data,
                       'start_date':start_date,
                       'end_date':end_date,
                       'order_no':order_no,
                       'content':content,
                       'order_status':order_status,
                       'pay_status':pay_status,
                       'delivery_status':delivery_status,
                       'ORDER_STAYUS':ORDER_STAYUS,
                       'PAY_STATUS':PAY_STATUS,
                       'DELIVERRY_STATUS':DELIVERRY_STATUS,
                       'count':query.count(),
                       'pay_start_date':pay_start_date,
                       'pay_end_date':pay_end_date
                      },layout='admin_supply/include/base.html')


class OrderDetailHandler(SupplyBaseHandler):
    def get(self):
        order_service.set_rdb(self.rdb)
        express_service.set_rdb(self.rdb)
        self.get_paras_dict()
        #--------------下单人信息----------------
        order_id = self.qdict.get('order_id')
        order = order_service.get_order_by_order_id(order_id)
        user_service.set_rdb(self.rdb)
        user = user_service.get_user_by_id(order.user_id)

        #--------------订单商品信息----------------
        order_service.set_rdb(self.rdb)
        query = order_service.query_item_by_order_id(order_id)
        items_order = self.get_page_data(query)

        #--------------支付信息----------------
        pay_service.set_rdb(self.rdb)
        pay_info = pay_service._list(order_id=order_id)

        #---------------快递公司信息---------------
        invoice_order = express_service.get_invoiceOrder_by_orderId(order.id)
        if invoice_order and invoice_order.express_company_id:
            company = ExpressCompanyCache().get_express_company_info(invoice_order.express_company_id)
        else:
            company = None

        #---------------收获地址信息---------------
        user_address = ujson.loads(order.recevie_address)
        if user_address:
            address = user_address.get('province')+user_address.get('city')+user_address.get('area')+user_address.get('address')
        else:
            address = ''
        self.echo('admin_drp/order/order_user.html',{'user_name':user_address and user_address.get('user_name') or '',
                                                     'phone':user_address and user_address.get('phone') or '',
                                                     'address':address,
                                                     'identify_card_num':user_address and user_address.get('card_num') or '',
                                                     'item_orders':items_order,
                                                     'pay_order':pay_info,
                                                     'PAYMENT_STATUS':PAYMENT_STATUS,
                                                     'order':order,
                                                     'express_no':invoice_order and invoice_order.express_no or '',
                                                     'company_name':company and company.get('name') or '',
                                                     'user':user
                                                    },layout='admin_supply/include/base.html')

from services.express.express_services import ExpressServices
express_service = ExpressServices()

class ExpressHandler(SupplyBaseHandler):

    def get(self,operation=None, *args, **kwargs):
        self.get_paras_dict()
        content = self.qdict.get('content','') #判断身份证号码，手机,订单号
        express_service.set_rdb(self.rdb)
        supply_user_id = self.current_user.get('id')
        self.qdict['supply_id'] = supply_user_id
        query = express_service.get_invoice_orders(**self.qdict)
        expresses = self.get_page_data(query)
        self.echo('admin_supply/express_list.html',{'data':expresses,
                                                     'content':content,
                                                     'count':query.count()},layout='admin_supply/include/base.html')

    def post(self, operation=None, *args, **kwargs):
        pass

    def get_express_name_by_id(self,id):
        '''
        获取物流公司名称
        :param id:
        :return:
        '''
        express_service.set_rdb(self.rdb)
        return express_service.get_express_company_by_id(id)

    def get_user_name_by_user_id(self,user_id):
        '''

        :param user_id:
        :return:
        '''
        express_service.set_rdb(self.rdb)
        return express_service.get_user_name_by_user_id(user_id)

from models.express_do import ExpressCompany
from utils.kuaidi import kuaidi_query,kuaidi_query_2
class ExpressCheckHandler(SupplyBaseHandler):
    def get(self, *args, **kwargs):
        order_id = self.get_argument('order_id','')
        invoice_order = self.rdb.query(InvoiceOrders).filter(InvoiceOrders.deleted==0,InvoiceOrders.order_id==order_id).scalar()
        #company = ExpressCompanyCache().get_express_company_info(invoice_order.express_company_id)
        company = self.db.query(ExpressCompany).filter(ExpressCompany.deleted==0,ExpressCompany.id==invoice_order.express_company_id).scalar()
        data = {'status':200,'data':''}
        if invoice_order and invoice_order.status==2 and invoice_order.express_content:
            data['data'] = ujson.loads(invoice_order.express_content)
            data['WaybillNumber'] = invoice_order.express_no
            data['company_name'] = company.get('name')
        else:
            #content = kuaidi_query(company.get('code'),invoice_order.express_no)
            content = kuaidi_query_2(company.get('code'),invoice_order.express_no)
            # content = kuaidi_query('yuantong','880350384879600241')
            express_data = ujson.loads(content)
            # condition = express_data.get('condition','')
            # is_check = express_data.get('ischeck','')
            express_content = express_data.get('data')
            status = express_data.get('status')
            if status==1:
                data['WaybillNumber'] = invoice_order.express_no
                data['company_name'] = company.get('name')
                data['data'] = '暂时没有物流信息'
                data['state'] = 201
            # if not express_content:
            #     content=express_data.get('message','')
            #     data['WaybillNumber'] = invoice_order.express_no
            #     data['company_name'] = company.get('name')
            #     data['data'] = content
            #     data['status'] = 201
            else:
                # [{"time":"2015-08-30 10:07:27","context":"客户 签收人: 邮件收发章 已签收","ftime":"2015-08-30 10:07:27"},
                #  {"time":"2015-08-30 08:20:40","context":"浙江省杭州市凤起路公司派件人: 张良良 派件中 派件员电话18958150267","ftime":"2015-08-30 08:20:40"},
                #  {"time":"2015-08-30 07:36:39","context":"快件到达 浙江省杭州市凤起路公司","ftime":"2015-08-30 07:36:39"},
                #  {"time":"2015-08-29 22:14:22","context":"杭州转运中心公司 已发出,下一站  浙江省杭州市凤起路","ftime":"2015-08-29 22:14:22"},
                #  {"time":"2015-08-28 20:52:09","context":"北京市朝阳区东坝公司 已打包,发往下一站 杭州转运中心","ftime":"2015-08-28 20:52:09"},
                #  {"time":"2015-08-28 19:02:02","context":"北京市朝阳区东坝公司 已揽收","ftime":"2015-08-28 19:02:02"}]}
                # if (condition and condition=='F00') and is_check=='1':
                #     invoice_order.express_content = ujson.dumps(express_content)
                #     invoice_order.status=2
                #     self.db.add(invoice_order)
                #     self.db.commit()
                if status==4:
                    invoice_order.express_content = ujson.dumps(express_content)
                    invoice_order.status=2
                    self.db.add(invoice_order)
                    self.db.commit()
                data['data']=express_content
                data['WaybillNumber']=invoice_order.express_no
                data['company_name']=company.get('name')
        if self.request.uri.startswith('/admin/mobile/'):
            self.echo('admin/mobile/order/express.html',{'data':data})
        else:
            self.echo('admin/order/express.html',{'data':data})




