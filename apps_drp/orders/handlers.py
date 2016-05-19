#encoding:utf-8
__author__ = 'wangjinkuan'

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


class OrderHandler(DrpBaseHandler):
    def get(self):
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

        drp_user_id = self.current_user.get('id')
        content = self.qdict.get('content','') #判断身份证号码，手机,订单号
        user_id = self.qdict.get('user_id','')
        query = order_service._list(user_id=user_id,drp_user_id=drp_user_id,start_date=start_date,end_date=end_date,
                                    order_no=order_no,content=content,pay_start_date=pay_start_date,
                                    pay_end_date=pay_end_date)
        if str(order_status):
            query = query.filter(Orders.status == order_status)
        if str(pay_status):
            query = query.filter(Orders.pay_status == pay_status)
        if str(delivery_status):
            query = query.filter(Orders.delivery_status == delivery_status)
        data = self.get_page_data(query)
        self.echo('admin_drp/order/order_list.html',
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
                      })

    def check_order_YhOrderApi(self,key_params,status):
        '''
        :param key_params:
        :return:
        '''
        logs_service.set_rdb(self.rdb)
        query_success = logs_service._list(logs_type=1,key_params=key_params,status=status)
        if query_success.count() > 0:
            return True

class OrderDetailHandler(DrpBaseHandler):
    def get(self,operation):
        order_service.set_rdb(self.rdb)
        express_service.set_rdb(self.rdb)
        self.get_paras_dict()
        if operation == 'detail':
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
                                                        })
        elif operation == 'delivery':
            order_no = self.qdict.get('order_no')
            express_companys = express_service.get_express_company_code()
            if self.request.uri.startswith('/admin/mobile/'):
                self.echo('admin/mobile/order/delivery_goods.html',
                          {'data':express_companys,
                           'order_no':order_no,
                          })
            else:
                self.echo('admin/order/delivery_goods.html',
                          {'data':express_companys,
                           'order_no':order_no,
                          })

    def post(self,operation):
        if operation == 'delivery':
             rsp = {'stat':'success','info':''}
             order_no = self.get_argument('order_no','')
             express_no = self.get_argument('express_no','')
             express_company_id = self.get_argument('express_company_id','')
             order_service.set_rdb(self.rdb)
             order = order_service.get_order_by_order_no(order_no)
             # order = self.rdb.query(Orders).fitler(Orders.deleted == 0,Orders.order_no == order_no).scalar()
             express_service.set_db(self.db)
             express_service.get_order_express_no(order,express_no,express_company_id)
             rsp = express_service._add(order,express_no,express_company_id,'ok',rsp)
             if rsp['stat'] == 'success':
                 try:
                     sql_format = 'update item_detail set quantity=(quantity-{0}) where id={1};'
                     execute_sqls=[]
                     for item in self.db.query(ItemOrders).filter(ItemOrders.order_id==order.id):
                         execute_sqls.append(sql_format.format(item.buy_nums,item.item_id))
                     if execute_sqls:
                         self.db.execute(''.join(execute_sqls))
                     self.db.commit()
                 except Exception,e:
                     self.captureException(sys.exc_info())
                 self.write_json({'stat':'success','info':'发货成功'})
             else:
                 self.write_json(rsp)


class SoldItemsHandler(DrpBaseHandler):
    def get(self, *args, **kwargs):
        start_date = self.get_argument('start_date','')
        end_date = self.get_argument('end_date','')
        item_n_t = self.get_argument('item_n_t','')
        category_name = self.get_argument('category_name',u'全部')
        category_id = self.get_argument('category_id','')
        order_service.set_rdb(self.rdb)
        query = order_service._list_itemOrders(start_date=start_date,
                                               end_date=end_date,
                                               item_n_t=item_n_t,
                                               category_id = category_id,
                                               pay_status=1)
        sales_items = self.get_page_data(query)
        self.echo('admin/order/sales_items.html',
                  {'data':sales_items,
                   'count':query.count(),
                   'start_date':start_date,
                   'end_date':end_date,
                   'item_n_t':item_n_t,
                   'category_name':category_name,
                   'category_id' : category_id,
                   'PAY_STATUS':PAY_STATUS,
                  })

    def get_itemDetail_by_id(self,item_id):
        '''
        todo:通过id获取商品
        :param item_id:
        :return:
        '''
        return self.rdb.query(ItemDetail).filter(ItemDetail.id == item_id).scalar()

from conf.orders_conf import PAY_TYPE
class PaymentHandlers(DrpBaseHandler):

    def get(self, *args, **kwargs):
        drp_user_id = self.current_user.get('id')
        start_date = self.get_argument('start_date','')
        end_date = self.get_argument('end_date','')
        order_no = self.get_argument('order_no','')
        pay_status = self.get_argument('pay_status','')
        settlement = self.get_argument('settlement','')#结算状态
        pay_type = self.get_argument('pay_type','')
        pay_service.set_rdb(self.rdb)
        query = pay_service._list(drp_usere_id=drp_user_id,order_no=order_no,pay_type=pay_type,pay_status=pay_status,start_date=start_date,end_date=end_date,settlement=settlement)
        data = self.get_page_data(query)

        self.echo('admin_drp/payment/payment_list.html',
                  {'data':data,
                   'PAYMENT_STATUS':PAYMENT_STATUS,
                   'PAY_TYPE':PAY_TYPE,
                   'pay_type':pay_type,
                   'order_no':order_no,
                   'pay_status':pay_status,
                   'start_date':start_date,
                   'end_date':end_date,
                   'settlement':settlement,
                   'count':query.count()
                  })

class SettlementHandler(DrpBaseHandler):

    def get(self, *args, **kwargs):
        pay_service.set_rdb(self.rdb)
        drp_user_id = self.current_user.get('id')
        query = pay_service.settlements(drp_user_id)
        data = self.get_page_data(query)
        self.echo('admin_drp/payment/settlements.html',{'data':data,'count':query.count()})

    def post(self, *args, **kwargs):
        pass


from utils.kuaidi import kuaidi_query,kuaidi_query_2
class ExpressCheckHandler(DrpBaseHandler):
    def get(self, *args, **kwargs):
        order_id = self.get_argument('order_id','')
        invoice_order = self.rdb.query(InvoiceOrders).filter(InvoiceOrders.deleted==0,InvoiceOrders.order_id==order_id).scalar()
        company = ExpressCompanyCache().get_express_company_info(invoice_order.express_company_id)
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
        # if self.request.uri.startswith('/admin/mobile/'):
        #     self.echo('admin_drp/mobile/order/express.html',{'data':data})
        # else:
        self.echo('admin_drp/order/express.html',{'data':data})
