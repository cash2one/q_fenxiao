#encoding:utf-8
__author__ = 'wangjinkuan'

from tornado.web import url
from apps_app.payment.allinpay_handler import *
from apps_app.payment.alipay_handler import *

_handlers = [
    url(r'/h5/order/allinpay/(\d*)/(\d*)/([\w\W]*).html',AllinPayPaymentHandler,name='app_allinpay_payment'),#通联支付
    url(r'/api/json/order/alipay/payback/',AppAlipayBackHandler,name='app_alipay_back')
]
