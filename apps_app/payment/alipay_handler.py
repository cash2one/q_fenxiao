#encoding:utf-8
__author__ = 'wangjinkuan'

from apps_app.common_handler import CommonHandler
import tornado.web
from common.alipay.alipay import *
from services.payments.payorder_services import PayOrderService
from services.orders.orders_services import OrderServices
import ujson,sys
from apps_api.yh_order_api import YhOrderApi
from services.express.express_services import ExpressServices
from services.logs.logs_services import LogsServices
from services.item.item_services import ItemService
from utils.logs import LOG
from data_cache.user_cache import UserCache

user_cache = UserCache()

payorder_service = PayOrderService()
order_service = OrderServices()
item_service = ItemService()

pay_log = LOG('alipay_pay_callback_logs')
_log = LOG('ali_pay_logs')

#支付宝回调
class AppAlipayBackHandler(CommonHandler):

    def check_xsrf_cookie(self):
        pass

    def get(self,*args, **kwargs):
        self.get_paras_dict()
        is_ok = notify_verify_for_app(self.qdict)
        order_no = self.qdict.get('out_trade_no')
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
                action='get',
                result='',
                status=1,
                error=''
            )
        except:
            pass
        if is_ok:
            payAmount = self.qdict.get('total_fee')
            other_payment_id = self.qdict.get('trade_no')
            pay_order = payorder_service.get_payorder_by_order_no(order_no)
            order_id = pay_order.order_id
            order = order_service.get_order_by_order_id(order_id)
            if str(payAmount)==str(pay_order.exchange):

                if pay_order.pay_status!=1:
                    is_success,info = payorder_service.set_paysuccess(pay_order.id,pay_order.order_no,1,pay_type=9,
                                                                      other_payment_id=other_payment_id)
                    if is_success:
                        try:
                            express_service = ExpressServices(db=self.db)
                            items = order_service.query_item_by_order_id(order_id=order_id)
                            express_service._add(order)
                        except Exception,e:
                            self.captureMessage('物流信息:')
                            self.captureException(sys.exc_info())
                        try:
                            yh_order_obj = YhOrderApi(self.db)
                            yh_order_obj.create_order_params(pay_order,order,items,order_type=3)
                            yh_order_obj.start() #执行run()
                        except:
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
                        self.write('success')
            else:
                pay_log.warning('支付金额不匹配')
                self.captureMessage('支付金额不匹配:'+ujson.dumps(self.qdict))
                raise tornado.web.HTTPError(400)
        else:
            pay_log.warning('验证签名不正确')
            self.captureMessage('验证签名不正确:'+ujson.dumps(self.qdict))
            raise tornado.web.HTTPError(400)


    def post(self,*args, **kwargs):

        self.get_paras_dict()
        is_ok = notify_verify_for_app(self.qdict)
        order_no = self.qdict.get('out_trade_no')
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
            payAmount = self.qdict.get('total_fee')
            other_payment_id = self.qdict.get('trade_no')
            pay_order = payorder_service.get_payorder_by_order_no(order_no)
            order_id = pay_order.order_id
            order = order_service.get_order_by_order_id(order_id)
            if str(payAmount)==str(pay_order.exchange):

                if pay_order.pay_status!=1:
                    is_success,info = payorder_service.set_paysuccess(pay_order.id,pay_order.order_no,1,pay_type=9,
                                                                      other_payment_id=other_payment_id)
                    if is_success:
                        try:
                            express_service = ExpressServices(db=self.db)
                            items = order_service.query_item_by_order_id(order_id=order_id)
                            express_service._add(order)
                        except Exception,e:
                            self.captureMessage('物流信息:')
                            self.captureException(sys.exc_info())
                        try:
                            yh_order_obj = YhOrderApi(self.db)
                            yh_order_obj.create_order_params(pay_order,order,items,order_type=3)
                            yh_order_obj.start() #执行run()
                        except:
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
                        self.write('success')
            else:
                pay_log.warning('支付金额不匹配')
                self.captureMessage('支付金额不匹配:'+ujson.dumps(self.qdict))
                raise tornado.web.HTTPError(400)
        else:
            pay_log.warning('验证签名不正确')
            self.captureMessage('验证签名不正确:'+ujson.dumps(self.qdict))
            raise tornado.web.HTTPError(400)
