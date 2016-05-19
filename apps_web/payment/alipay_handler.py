#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'gaoaifei'

from common.base_handler import BaseHandler
import tornado.web
from common.alipay.alipay import *
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
from utils.exchange_rate import get_usd_exchange_rate_and_count
import rsa
import base64

user_cache = UserCache()

payorder_service = PayOrderService()
order_service = OrderServices()
item_service = ItemService()

pay_log = LOG('alipay_pay_callback_logs')
_log = LOG('ali_pay_logs')

#通联支付跳转
class AliPayPaymentHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self,order_id,order_no):
        user_id = self.get_current_user().get('id')
        payorder_service.set_rdb(self.rdb)
        pay_order = payorder_service.get_payorder_by_order_id(order_id,user_id)
        isok, amount= get_usd_exchange_rate_and_count(pay_order.amount)
        if isok:
            total_fee = amount[1]
        else:
            return  self.write('对不起，银行汇率查询接口在升级维修，请稍后再试')
        order_service.set_rdb(self.rdb)
        item_orders = order_service.get_ItemsOrder_info(order_id)
        for io in item_orders:
            id = io.item_id
        item_service.set_rdb(self.rdb)
        item = item_service.get_itemDetail_by_id(id)
        item_title = item.title
        item_content = item.product_keywords
        if pay_order.pay_status==0:
            params = create_forex_trade(pay_order.order_no,item_title,item_content, total_fee)
            url = 'https://mapi.alipay.com/gateway.do?' + urlencode(params)
            self.redirect(url)
        else:
            self.redirect(self.reverse_url('member_order_detail',pay_order.order_no))


#通联支付回调
class AlipayBackHandler(BaseHandler):

    def check_xsrf_cookie(self):
        pass

    @tornado.web.authenticated
    def get(self,order_id,order_no, **kwargs):
        self.redirect(self.reverse_url('member_order_detail',order_no))

    def post(self,*args, **kwargs):

        self.get_paras_dict()
        is_ok = notify_verify(self.qdict)
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
            # payment_time = self.qdict.get('payDatetime')
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

            else:
                pay_log.warning('支付金额不匹配')
                self.captureMessage('支付金额不匹配:'+ujson.dumps(self.qdict))
                raise tornado.web.HTTPError(400)
        else:
            pay_log.warning('验证签名不正确')
            self.captureMessage('验证签名不正确:'+ujson.dumps(self.qdict))
            raise tornado.web.HTTPError(400)
