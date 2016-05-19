#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'gaoaifei'

from ..base_handler import DrpBaseHandler
from services.express.express_services import ExpressServices
import json,ujson
from models.express_do import InvoiceOrders

express_service = ExpressServices()

class ExpressHandler(DrpBaseHandler):

    def get(self,operation=None, *args, **kwargs):
        self.get_paras_dict()
        content = self.qdict.get('content','') #判断身份证号码，手机,订单号
        express_service.set_rdb(self.rdb)
        drp_user_id = self.current_user.get('id')
        self.qdict['drp_user_id'] = drp_user_id
        query = express_service.get_invoice_orders(**self.qdict)
        expresses = self.get_page_data(query)
        self.echo('admin_drp/express/express_list.html',{'data':expresses,
                                                     'content':content,
                                                     'count':query.count()})

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
class ExpressCheckHandler(DrpBaseHandler):
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
            content = kuaidi_query_2(company.get('code'),invoice_order.express_no)
            express_data = ujson.loads(content)
            express_content = express_data.get('data')
            status = express_data.get('status')
            if status==1:
                data['WaybillNumber'] = invoice_order.express_no
                data['company_name'] = company.get('name')
                data['data'] = '暂时没有物流信息'
                data['state'] = 201
            else:
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
