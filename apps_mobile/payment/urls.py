#ecoding:utf-8
__author__ = 'binpo'

from tornado.web import url
from handlers import *

_handlers = [
    url(r'/order/pay/([\w\W]*).html',PayOrdersHandler,name='pay_order'),#order_id,pay_order_id 确认支付页
    url(r'/order/(\d*)/pay/detail-([\w\W]*).html',PayOrderDetailHandler,name='pay_order_detail'),#order_id,pay_order_id

    # url(r'/order/allinpay/(\d*)/([\w\W]*).html',AllinPayPaymentHandler,name='allinpay_payment'),#通联支付
    # url(r'/order/allinpay/payback/(\d*)/([\w\W]*).html',AllinPayBackHandler,name='allinpay_payment_payback'),#通联支付回调

    url(r'/pay/jsapi/makepayment/',JsApiHandler,name='weixin_js_api'),#微信js支付
    url(r'/pay/jsapi/weixin/notify.html',WeixinPayNotifyHandler,name='mobile_weixin_notify'),#微信notify
]


# #支付宝支付
# from alipay_handler import *
# _handlers.extend([
#     url(r'/order/alipay/(\d*)/([\w\W]*).html',AliPayPaymentHandler,name='alipay_payment'),#易汇金支付
#     url(r'/order/alipay/payback/(\d*)/([\w\W]*).html',AlipayBackHandler,name='alipay_payment_payback'),#易汇金付回调
#     ]
# )