#encoding:utf-8
__author__ = 'binpo'

from common.base_handler import BaseHandler
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
from services.item.item_services import ItemService
from utils.logs import LOG
from data_cache.user_cache import UserCache
import rsa
import base64

user_cache = UserCache()

payorder_service = PayOrderService()
order_service = OrderServices()
item_service = ItemService()

pay_log = LOG('allpay_pay_callback_logs')
_log = LOG('all_pay_logs')

class PayOrdersHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self,order_no,*args, **kwargs):
        user_id = self.get_current_user().get('id')
        payorder_service.set_rdb(self.rdb)
        order = payorder_service.get_order_no(order_no,user_id)
        house_ware_id = order.house_ware_id
        item_service.set_rdb(self.rdb)
        notice_content = item_service.get_notice_content_by_house_ware_id(house_ware_id)
        #pay_order = payorder_service.get_payorder_by_id(pay_order_id,user_id)
        if not order.id:
            raise tornado.web.HTTPError(404)
        order_service.set_rdb(self.rdb)
        items = order_service.query_item_by_order_no(order_no)
        item_count = items.count()
        if not item_count:
            raise tornado.web.HTTPError(404)
        item_title = items[0].title
        if order.pay_status==0:
            self.echo('order/payway.html',{
            'item_count':item_count,
            'item_title':item_title,
            'order':order,
            'notice_content':notice_content
            },layout='order/order_base.html')
        else:
            self.redirect(self.reverse_url('member_order_detail',order_no))
            #self.echo('order/info.html',{'info':'订单已支付'},layout='order/order_base.html')

    def post(self, *args, **kwargs):
        pass


class PayOrderDetailHandler(BaseHandler):

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
        },layout='order/order_base.html')


#通联支付跳转
class AllinPayPaymentHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self,order_id,order_no):
        user_id = self.get_current_user().get('id')
        payorder_service.set_rdb(self.rdb)
        pay_order = payorder_service.get_payorder_by_order_id(order_id,user_id)
        order_service.set_rdb(self.rdb)
        order = order_service.get_order_no(order_no,user_id)
        user_address = ujson.loads(order.recevie_address)
        card_num = user_address.get('card_num')
        card_num = '01'+card_num
        # 身份证号rsa加密
        pubkey = rsa.PublicKey(149380992406927500716241361923785654160314473712177262569404352542855462290905900996898820349830223450863291102361998356737565352204766003197145257743784108967049311092979500247005291724928627891055953026325337822510580077557484401424165589043287424587640610886383070856297739481742150528531012906820072406507, 65537)
        crypto = rsa.encrypt(str(card_num), pubkey)
        card_num_rsa = base64.b64encode(crypto)
        user_name = user_address.get('user_name')
        if pay_order.pay_status==0:
            gmt_created = datetime.datetime.strftime(pay_order.gmt_created,'%Y%m%d%H%M%S')
            payback_url = self.reverse_url('allinpay_payment_payback',order_id,order_no)
            params = create_pay_info(pay_order.order_no,'','', pay_order.amount,gmt_created,card_num_rsa,user_name,
                                     return_url=PAYMENT_BACK_HOST+payback_url,notify_url=PAYMENT_BACK_HOST+payback_url)
            self.echo('pay/allinpayment.html',{'params':params},layout='')
        else:
            self.redirect(self.reverse_url('member_order_detail',pay_order.order_no))

#通联支付回调
class AllinPayBackHandler(BaseHandler):

    def check_xsrf_cookie(self):
        pass

    @tornado.web.authenticated
    def get(self,order_id,order_no, **kwargs):
        self.redirect(self.reverse_url('member_order_detail',order_no))

    def post(self,*args, **kwargs):

        self.get_paras_dict()
        is_ok,info = notify_verify(self.qdict)
        order_no = self.qdict.get('orderNo')
        _log.info(ujson.dumps(self.qdict))

        payorder_service.set_rdb(self.rdb)
        order_service.set_db(self.db)
        order_service.set_rdb(self.rdb)
        payorder_service.set_db(self.db)

        try:
            #支付回调成功，建立回调成功日志
            LogsServices(db=self.db).new_api_logs(
                logs_type=3,
                key_params=order_no,
                reqeust_url=self.request.host,
                params=ujson.dumps(self.qdict),
                action='post',
                result='',
                status=1,
                error=''
            )
        except:
            pass
        if is_ok:
            payAmount = self.qdict.get('payAmount')
            other_payment_id = self.qdict.get('paymentOrderId')
            payment_time = self.qdict.get('payDatetime')
            pay_order = payorder_service.get_payorder_by_order_no(order_no)
            order_id = pay_order.order_id
            order = order_service.get_order_by_order_id(order_id)
            if int(payAmount)==int(round(pay_order.amount*100)):

                if pay_order.pay_status!=1:
                    is_success,info = payorder_service.set_paysuccess(pay_order.id,pay_order.order_no,1,pay_type=7,
                                                                      other_payment_id=other_payment_id,
                                                                      payment_time=payment_time)
                    if is_success:
                        try:
                            user_cache.delete_user_daily_pay(order_id)
                            address = ujson.loads(order.recevie_address)
                            categories = order_service.get_category_id_by_order_id(order_id)
                            for c in categories:
                                user_cache.set_daily_buy_cache(c.category_id,address.get('card_num'))
                        except:
                            pass

                        try:
                            express_service = ExpressServices(db=self.db)
                            items = order_service.query_item_by_order_id(order_id=order_id)
                            express_service._add(order)
                        except Exception,e:
                            self.captureMessage('物流信息:')
                            self.captureException(sys.exc_info())
                        self.write('OK')
                    else:
                        pay_log.warning('支付成功修改状态失败 人工处理:'+ujson.dumps(self.qdict)+' error:'+info)
                        #如果修改支付成功，而订单等状态修改失败，建立一个任务，使得人工在后台进行状态修改
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
                        self.captureException(info)
                        self.captureMessage('支付成功修改状态失败 人工处理:'+ujson.dumps(self.qdict))
                        self.write('OK')
                        # logger.error(info)
                        #
                        # self.write('error')
            else:
                pay_log.warning('支付金额不匹配')
                self.captureMessage('支付金额不匹配:'+ujson.dumps(self.qdict))
                raise tornado.web.HTTPError(400)
        else:
            pay_log.warning('验证签名不正确')
            self.captureMessage('验证签名不正确:'+ujson.dumps(self.qdict))
            raise tornado.web.HTTPError(400)
