#encoding:utf-8
__author__ = 'gaoaifei'

from common.base_handler import BaseHandler
import tornado.web
from common.ehkingpay.ehkingpay import create_pay_info,settings,checkHmac
from services.payments.payorder_services import PayOrderService
from services.orders.orders_services import OrderServices
from services.users.user_services import UserServices
import logging
import datetime,time
import ujson,sys
from setting import PAYMENT_BACK_HOST
from services.express.express_services import ExpressServices
from services.logs.logs_services import LogsServices
from utils.logs import LOG

from data_cache.user_cache import UserCache
user_cache = UserCache()

payorder_service = PayOrderService()
order_service = OrderServices()
user_address_service = UserServices()
pay_log = LOG('pay_callback_logs')
_log = LOG('all_pay_logs')


#易汇金支付跳转
# 备注：记得记录跳转地址
class EhkingPaymentHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self,order_id,order_no):
        user_id = self.get_current_user().get('id')
        order_service.set_rdb(self.rdb)
        order = order_service.get_order_no(order_no,user_id)
        recevie_address_id = order.recevie_address_id #订单收货地址
        user_address_service.set_rdb(self.rdb)
        address = user_address_service.get_address_by_id(user_id,recevie_address_id)
        name = address.name #收货人姓名
        card_type = address.card_type #证件类型
        if card_type==1:
            card_type = 'IDCARD'
        else:
            card_type = 'ORG'
        card_num  = address.card_num #证件号码
        order_service.set_rdb(self.rdb)
        items = order_service.query_item_by_order_no(order_no)
        productDetail = []
        for item in items:
            # 备注：当购买商品为一箱时，是按照一箱里的个体来算的
            amount = item.item_price*100
            buy_nums = item.buy_nums
            if item.amount>1:
               amount =  (item.item_price/item.amount)*100
               buy_nums = item.buy_nums*item.amount
            dict =  {
                'name':item.title,
                'quantity': buy_nums,#销售数量
                'amount': amount,#销售价格
                'receiver':'',
                'description': ''
            }
            productDetail.append(dict)
        payorder_service.set_rdb(self.rdb)
        pay_order = payorder_service.get_payorder_by_order_id(order_id,user_id)
        if pay_order.pay_status==0:
            order_service.set_rdb(self.rdb)
            paylogs = order_service.get_pay_logs_ehking_by_order_id(order_no,user_id)
            if not paylogs:
                payback_url = self.reverse_url('ehking_payment_payback',order_id,order_no)
                payResult = create_pay_info(pay_order.order_no,#订单号
                                            pay_order.amount,#支付金额
                                            name,#收货人真实姓名
                                            card_type,#证件类型
                                            card_num,#证件号码
                                            productDetail,
                                            callbackUrl = PAYMENT_BACK_HOST+payback_url,
                                            notify_url = PAYMENT_BACK_HOST+payback_url
                                         )
                if payResult:
                    order_service.set_db(self.db)
                    order_service.add_pay_logs_ehking(order_id,order_no,user_id,payResult)
                    self.redirect(payResult['redirectUrl'])
                else:
                    self.echo('pay/error.html',{'info':'请核对您的填写的收货人姓名和身份证信息真实有效！'})
            else: #如果存在，再次支付，判断该支付是否失效，默认时间为24小时
                self.redirect(paylogs.redirectUrl)
        else:
            self.redirect(self.reverse_url('member_order_detail',pay_order.order_no))

#易汇金支付回调
class EhkingBackHandler(BaseHandler):

    def check_xsrf_cookie(self):
        pass

    @tornado.web.authenticated
    def get(self,order_id,order_no, **kwargs):
        self.redirect(self.reverse_url('member_order_detail',order_no))
        # json_data = self.request.body
        # data = ujson.loads(json_data)
        # logger.info(json_data)
        # self.qdict = data
        # is_ok,info = checkHmac(self.qdict)
        # order_no = self.qdict.get('requestId')
        # try:
        #     LogsServices(db=self.db).new_api_logs(
        #         logs_type=3,
        #         key_params=order_no,
        #         reqeust_url=self.request.host,
        #         params=ujson.dumps(self.qdict),
        #         action='post',
        #         result='',
        #         status=1,
        #         error=''
        #     )
        # except:
        #     pass
        # if is_ok:#签证通过
        #     payAmount = self.qdict.get('orderAmount')
        #     other_payment_id = self.qdict.get('requestId')
        #     payment_time = self.qdict.get('completeDateTime')
        #     payorder_service.set_rdb(self.rdb)
        #     pay_order = payorder_service.get_payorder_by_order_no(order_no)
        #     order_id = pay_order.order_id
        #     if int(payAmount)==int(pay_order.amount*100):
        #         payorder_service.set_db(self.db)
        #         if pay_order.pay_status!=1:
        #             is_success,info = payorder_service.set_paysuccess(pay_order.id,pay_order.order_no,1,pay_type=8,
        #                                                               other_payment_id=other_payment_id,
        #                                                               payment_time=payment_time)
        #             if is_success:
        #                 try:
        #                     order_service.set_rdb(self.rdb)
        #                     express_service = ExpressServices(db=self.db)
        #                     items = order_service.query_item_by_order_id(order_id=order_id)
        #                     order = order_service.get_order_by_order_id(order_id)
        #                     express_service._add(order)
        #                 except Exception,e:
        #                     self.captureMessage('物流信息:')
        #                     self.captureException(sys.exc_info())
        #                 try:
        #                     yh_order_obj = YhOrderApi(self.db)
        #                     yh_order_obj.create_order_params(pay_order,order,items)
        #                     yh_order_obj.start()
        #                 except:
        #                     self.captureException(sys.exc_info())
        #                 self.redirect(self.reverse_url('member_order_detail',pay_order.order_no))
        #             else:
        #                 pay_log.warning('支付成功修改状态失败 人工处理:'+ujson.dumps(self.qdict))
        #                 LogsServices(db=self.db).create_task(
        #                     task_type=3,
        #                     key_params=order_no,
        #                     reqeust_url=self.request.host+self.request.uri,
        #                     params=ujson.dumps(self.qdict),
        #                     action='post',
        #                     result='',
        #                     status=0,
        #                     error=info
        #                 )
        #                 self.captureException(info)
        #                 self.captureMessage('支付成功修改状态失败 人工处理:'+ujson.dumps(self.qdict))
        #         self.redirect(self.reverse_url('member_order_detail',pay_order.order_no))
        #     else:
        #         pay_log('pay_callback_logs').error('支付金额不匹配')
        #         self.captureMessage('支付金额不匹配:'+ujson.dumps(self.qdict))
        #         raise tornado.web.HTTPError(400)
        # else:
        #     pay_log('pay_callback_logs').error(info)
        #     self.captureMessage( info + ':' + ujson.dumps(self.qdict))
        #     raise tornado.web.HTTPError(400)

    def post(self,*args, **kwargs):
        json_data = self.request.body
        data = ujson.loads(json_data)
        _log.info(json_data)
        self.qdict = data

        payorder_service.set_rdb(self.rdb)
        order_service.set_rdb(self.rdb)
        order_service.set_db(self.db)
        payorder_service.set_db(self.db)


        is_ok,info = checkHmac(self.qdict)
        order_no = self.qdict.get('requestId')
        try:
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
        if is_ok:#签证通过
            payAmount = self.qdict.get('orderAmount')
            other_payment_id = self.qdict.get('serialNumber')
            payment_time = self.qdict.get('completeDateTime')

            pay_order = payorder_service.get_payorder_by_order_no(order_no)
            order_id = pay_order.order_id
            if int(payAmount)==int(pay_order.amount*100):
                if pay_order.pay_status!=1:
                    order = order_service.get_order_by_order_id(order_id)
                    is_success,info = payorder_service.set_paysuccess(pay_order.id,pay_order.order_no,1,pay_type=8,
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
                        self.write('ok')
                    else:
                        pay_log.warning('支付成功修改状态失败 人工处理:'+ujson.dumps(self.qdict))
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
                        self.write('ok')
            else:
                pay_log('pay_callback_logs').error('支付金额不匹配')
                self.captureMessage('支付金额不匹配:'+ujson.dumps(self.qdict))
                raise tornado.web.HTTPError(400)
        else:
            pay_log('pay_callback_logs').error(info)
            self.captureMessage( info + ':' + ujson.dumps(self.qdict))
            raise tornado.web.HTTPError(400)