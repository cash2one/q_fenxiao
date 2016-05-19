#encoding:utf-8
__author__ = 'binpo'
from services.base_services import BaseService
from models.orders_do import Orders,ItemOrders
from models.express_do import InvoiceOrders,OrderExpress,ExpressCompany
from models.user_do import Users,UserAddress
from services.users.admin_services import AdminServices
import ujson
import traceback
from utils.message import send_msg
from conf.sms_conf import ORDER_SENDED_TEMPLATE
from utils.logs import LOG
from sqlalchemy.sql.functions import now
from sqlalchemy import or_

admin_services = AdminServices()

log = LOG('express_logs')
class ExpressServices(BaseService):

    def _add(self,order,express_no=None,express_company_id=None,send=None,rsp=None):
        '''
        根据订单添加发货单号
        :param order:
        :return:
        '''
        try:
            invoice_order = self.db.query(InvoiceOrders).filter(InvoiceOrders.deleted==0,InvoiceOrders.order_id==order.id,InvoiceOrders.order_no==order.order_no).first()
            if not invoice_order:
                invoice_order = InvoiceOrders()
                if send == 'ok':
                    invoice_order.status = 1
                    order.delivery_status = 1
                    self.db.add(order)
                else:
                    invoice_order.status = 0
            else:
                #有发货单 确认发货,状态为发货状态
                if express_no and express_company_id:
                    invoice_order.status = 1
                    invoice_order.delivery_time = now()
                else:
                    invoice_order.status = 0
            invoice_order.invoice_no = ''
            invoice_order.user_id = order.user_id
            invoice_order.order_id = order.id
            invoice_order.supply_id = order.supply_user_id
            invoice_order.drp_user_id = order.drp_usere_id
            invoice_order.order_no = order.order_no
            address = ujson.loads(order.recevie_address)
            name = self.db.query(UserAddress.name).filter(UserAddress.deleted==0,UserAddress.id==order.recevie_address_id)
            invoice_order.name = name
            invoice_order.province = address.get('province')
            invoice_order.city = address.get('city')
            invoice_order.county = address.get('area')
            invoice_order.zip = address.get('zipcode')
            invoice_order.addr = address.get('address')
            invoice_order.mobile = address.get('phone')
            invoice_order.express_no = express_no
            invoice_order.express_company_id = express_company_id
            self.db.add(invoice_order)
            self.db.commit()
        except Exception,e:
            rsp['stat'] = 'error'
            rsp['info'] = e.message
        return rsp
        # rsp['stat'] = 'success'
        # return rsp

    def batch_add(self,data):
        '''
        批量处理发货
        :param data:
        :return:
        '''
        error_data = []
        invoice_orders = []
        index=0
        express_cache = ExpressCompanyCache()
        for d in data:
            index+=1
            try:
                order_no = d.get('order_no','')
                express_no = d.get('express_no','')
                express_company_code = d.get('express_company_code','')
                order = self.db.query(Orders).filter(Orders.deleted == 0,Orders.order_no == order_no).scalar()
                if not order:
                    #d['error'] = d['error']+' 存在错误的订单号:'+str(order_no)
                    error_data.append(d)
                    continue
                express_company={}
                express_company = express_cache.get_express_company_info_by_company_code(express_company_code)
                invoice_order = self.db.query(InvoiceOrders).filter(InvoiceOrders.deleted==0,InvoiceOrders.order_id==order.id,InvoiceOrders.order_no==order.order_no).first()
                if not invoice_order:
                    invoice_order = InvoiceOrders()
                    invoice_order.status = 1
                    invoice_order.invoice_no = ''
                    invoice_order.order_id = order.id
                    invoice_order.order_no = order.order_no
                    address = ujson.loads(order.recevie_address)
                    invoice_order.province = address.get('province')
                    invoice_order.city = address.get('city')
                    invoice_order.county = address.get('area')
                    invoice_order.zip = address.get('zipcode')
                    invoice_order.addr = address.get('address')
                    invoice_order.mobile = address.get('phone')
                    invoice_order.express_no = express_no
                    invoice_order.express_company_id = express_company.get('id',0)
                    self.db.add(invoice_order)
                    self.db.flush()
                    #self.db.commit()
                elif invoice_order and invoice_order.status==0:
                    invoice_order.status = 1
                    invoice_order.express_no = express_no
                    invoice_order.express_company_id = express_company.get('id',0)
                    self.db.add(invoice_order)
                    self.db.flush()
                    # try:send_msg(address.get('phone'),ORDER_SENDED_TEMPLATE.format(express_company.name,express_no))
                    # except:pass
                invoice_orders.append(invoice_order)
            except Exception,e:
                log.warning(traceback.format_exc())
                d['error'] = d['error']+e.message
                error_data.append(d)
        self.db.commit()
        return error_data,invoice_orders

    def get_order_express_no(self,order,express_no,express_company_id):
        '''
        todo:查询物流单
        :param kwargs:
        :return:
        '''
        query = self.db.query(OrderExpress).\
            filter(OrderExpress.deleted == 0,OrderExpress.order_no == order.order_no,OrderExpress.express_no == express_no).scalar()
        if not query:
            order_express = OrderExpress()
            order_express.order_no = order.order_no
            order_express.express_no = express_no
            order_express.express_comoany_id = int(express_company_id)
            order_express.order_id = order.id
            self.db.add(order_express)
            self.db.commit()

    def get_express_company_code(self,**kwargs):
        '''
        todo:获取物流公司
        :param express_company_code:
        :return:
        '''
        query = self.rdb.query(ExpressCompany).filter(ExpressCompany.deleted == 0)
        if kwargs.get('express_company_code',''):
            query = query.filter(ExpressCompany.code == kwargs.get('express_company_code'))
        if kwargs.get('express_company_id',''):
            query = query.filter(ExpressCompany.id == kwargs.get('express_company_id'))
        return query

    def invoice_order_format(self,invoice_order):

        keys = ['id','order_id','order_no','express_no','express_company_id']

        return {key: getattr(invoice_order, key, '') for key in keys}

    def get_invoiceOrder_by_orderId(self,order_id):
        '''
        todo:
        :param order_id:
        :return:
        '''
        return self.rdb.query(InvoiceOrders).filter(InvoiceOrders.deleted==0,InvoiceOrders.order_id==order_id).scalar()

    def get_invoice_orders(self,**qdict):
        '''
        发货单列表
        :param qdict:
        :return:
        '''
        query = self.rdb.query(InvoiceOrders).filter(InvoiceOrders.deleted == 0)
        if qdict.get('content'):
            content = qdict.get('content')
            query = query.filter(or_(InvoiceOrders.order_no==content,InvoiceOrders.express_no==content,InvoiceOrders.user_id==(self.rdb.query(Users.id).filter(Users.deleted==0,Users.phone==content))))

        if qdict.get('supply_id'):
            query = query.filter(InvoiceOrders.supply_id==qdict.get('supply_id'))

        if qdict.get('drp_user_id'):
            query = query.filter(InvoiceOrders.drp_user_id==qdict.get('drp_user_id'))

        query = query.order_by(InvoiceOrders.gmt_created.desc())
        return query

    def get_express_company_by_id(self,id):
        return self.rdb.query(ExpressCompany.name).filter(ExpressCompany.id==id).scalar()

    def get_user_name_by_user_id(self,user_id):
        return self.rdb.query(Users.real_name).filter(Users.id==user_id).scalar()