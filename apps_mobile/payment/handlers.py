#encoding:utf-8
__author__ = 'gaoaifei'

from common.base_handler import MobileBaseHandler
import tornado.web
from common.allinpay.allinpay import create_pay_info,notify_verify,settings
from services.payments.payorder_services import PayOrderService
from services.orders.orders_services import OrderServices
import logging
import datetime
import ujson,sys
from setting import PAYMENT_BACK_HOST
from services.express.express_services import ExpressServices
from services.logs.logs_services import LogsServices
from utils.logs import LOG
from services.item.item_services import ItemService
import rsa
import base64
logger =logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.FileHandler(settings.LOGGING_PAYMENT))

payorder_service = PayOrderService()
order_service = OrderServices()
item_service = ItemService()
pay_log = LOG('pay_callback_logs')

from libs.wxpay import JSWXpay,QRWXpay
from conf.weixin_pay_conf import *
js_wxpay = JSWXpay(appid=WX_AppID,
                   mch_id=MERCH_ID,
                   key=PAY_KEY,
                   ip='120.26.135.176',
                   notify_url='http://fenxiao.qqqg.com/pay/jsapi/weixin/notify.html',
                   appsecret=WX_AppSecret)


qr_wxpay = QRWXpay(appid=WX_AppID,
                   mch_id=MERCH_ID,
                   key=PAY_KEY,
                   ip='120.26.135.176',
                   notify_url='http://fenxiao.qqqg.com/pay/jsapi/weixin/notify.html',
                   appsecret=WX_AppSecret)

from common.permission_control import mobile_user_authenticated,mobile_order_authenticated

class PayOrdersHandler(MobileBaseHandler):

    def get(self,order_no,*args, **kwargs):
        try:
            user_id = self.get_current_user().get('id')
            payorder_service.set_rdb(self.rdb)
            order = payorder_service.get_order_no(order_no,user_id)
            # is_abroad = order.is_abroad
            # house_ware_id = order.house_ware_id
            # item_service.set_rdb(self.rdb)
            # notice_content = item_service.get_notice_content_by_house_ware_id(house_ware_id)
            # print 'order_id:',order.id
            if not order.id:
                raise tornado.web.HTTPError(404)
            if order.pay_status==0:

                info_dict = {
                    'redirect_uri': 'http://fenxiao.qqqg.com/pay/jsapi/makepayment/',
                    'state':order_no
                }
                url = js_wxpay.generate_redirect_url(info_dict)
                self.redirect(url)
                #return redirect(url)
                #self.echo('mobile/member/payway.html',{'order':order,'is_abroad':False})
            else:
                self.redirect(self.reverse_url('member_order_detail',order_no))
        except Exception,e:
            print e.message


    def post(self, *args, **kwargs):
        pass

#http://fenxiao.qqqg.com/pay/jsapi/makepayment/
class JsApiHandler(MobileBaseHandler):

    def get(self, *args, **kwargs):
        self.get_paras_dict()
        code = self.qdict.get('code')
        order_no = self.qdict.get('state')
        js_wxpay.ip = self.get_client_ip
        openid = js_wxpay.generate_openid(code)

        user_id = self.get_current_user().get('id')
        payorder_service.set_rdb(self.rdb)
        order_service.set_rdb(self.rdb)
        order = payorder_service.get_order_no(order_no,user_id)

        #order = Orders.select().where(Orders.order_no==order_no).first()
        #pay_order = PayOrders.select().where(PayOrders.order_no==order_no).first()
        #
        # product={}
        # #for item in order.orderitems_set:
        # product = {
        #     'attach':u'测试数据',
        #     'body': u'测试数据',
        #     'out_trade_no':order.order_no,
        #     'total_fee':order.real_amount,
        # }
        items = order_service.query_item_by_order_no(order_no)
        for item in items:
            product = {
                'attach':item.title ,
                'body': item.summary,
                'out_trade_no':order.order_no,
                'total_fee':order.real_amount,
            }
            break
        #break
        ret_dict = js_wxpay.generate_jsapi(product, openid)
            #return render_template('order_detail.html',ret_dict=ret_dict,order=order,pay_order=pay_order,ORDER_STATUS=dict(ORDER_STATUS),ORDER_TYPES=dict(ORDER_TYPES))
        self.echo('mobile/member/payway.html',{'order':order,'is_abroad':False,'ret_dict':ret_dict})

#http://fenxiao.qqqg.com/order/pay/notify.html
class WeixinPayNotifyHandler(MobileBaseHandler):

    def check_xsrf_cookie(self):
        pass

    def get(self):
        xml_str = self.request.body
        pay_log.warning(ujson.dumps(xml_str))
        payorder_service.set_rdb(self.rdb)
        order_service.set_rdb(self.rdb)
        order_service.set_db(self.db)
        payorder_service.set_db(self.db)
        ret, ret_dict = qr_wxpay.verify_notify(xml_str)
        order_no = ret_dict.get('out_trade_no')
        total_fee = ret_dict.get('total_fee')
        self.redirect(self.reverse_url('member_order_detail',order_no))


    def post(self, *args, **kwargs):

        xml_str = self.request.body
        pay_log.warning(ujson.dumps(xml_str))
        payorder_service.set_rdb(self.rdb)
        order_service.set_rdb(self.rdb)
        order_service.set_db(self.db)
        payorder_service.set_db(self.db)
        ret, ret_dict = qr_wxpay.verify_notify(xml_str)
        try:
            LogsServices(db=self.db).new_api_logs(
                logs_type=3,
                key_params=ret_dict.get('out_trade_no'),
                reqeust_url=self.request.host,
                params=xml_str,
                action='post',
                result='',
                status=1,
                error=''
            )
        except:
            pass

        # 在这里添加订单更新逻辑
        if ret:
            order_no = ret_dict.get('out_trade_no')
            total_fee = ret_dict.get('total_fee')

            other_payment_id = ret_dict.get('transaction_id')
            payment_time = ret_dict.get('time_end')
            pay_order = payorder_service.get_payorder_by_order_no(order_no)
            order_id = pay_order.order_id

            if int(total_fee)==int(round(pay_order.amount*100)):
                order = order_service.get_order_by_order_id(order_id)
                if pay_order.pay_status!=1:
                    is_success,info = payorder_service.set_paysuccess(pay_order.id,pay_order.order_no,1,pay_type=6,
                                                                      other_payment_id=other_payment_id,
                                                                      payment_time=payment_time)
                    if is_success:
                        try:
                            express_service = ExpressServices(db=self.db)
                            items = order_service.query_item_by_order_id(order_id=order_id)
                            express_service._add(order)
                        except Exception,e:
                            pay_log.warning('支付金额不匹配')
                        self.write('OK')
                    else:
                        pay_log.warning('支付成功修改状态失败 人工处理:'+ujson.dumps(self.qdict)+' error:'+info)
                        LogsServices(db=self.db).create_task(
                            task_type=3,
                            key_params=order_no,
                            reqeust_url=self.request.host+self.request.uri,
                            params=ujson.dumps(self.qdict),
                            action='post',
                            result='',
                            status=0,
                            error=info
                        )
                        self.write('OK')
                        # logger.error(info)
                        #
                        # self.write('error')
            else:
                pay_log.warning('支付金额不匹配')
                raise tornado.web.HTTPError(400)

            ret_dict = {
                'return_code': 'SUCCESS',
                'return_msg': 'OK',
            }
            ret_xml = qr_wxpay.generate_notify_resp(ret_dict)
            pay_log.info(ret_xml)
        else:
            ret_dict = {
                'return_code': 'FAIL',
                'return_msg': 'verify error',
            }
            ret_xml = qr_wxpay.generate_notify_resp(ret_dict)
        self.write(ret_xml)

class PayOrderDetailHandler(MobileBaseHandler):

    @tornado.web.authenticated
    def get(self,order_id,order_no,*args, **kwargs):

        user_id = self.get_current_user().get('id')
        payorder_service.set_rdb(self.rdb)
        order = payorder_service.get_order_id(order_id,user_id)
        order_service.set_rdb(self.rdb)
        items = order_service.query_item_by_order_id(order_id)
        self.echo('order/order_detail.html',{
           'order':order,
           'items':items
        })
