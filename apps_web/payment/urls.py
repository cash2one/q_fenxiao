#ecoding:utf-8
__author__ = 'binpo'

from tornado.web import url
from handlers import *
#通联支付
_handlers = [
    url(r'/order/pay/([\w\W]*).html',PayOrdersHandler,name='pay_order'),#order_id,pay_order_id＃提交订单后跳转的选择支付页
    url(r'/order/(\d*)/pay/detail-([\w\W]*).html',PayOrderDetailHandler,name='pay_order_detail'),#order_id,pay_order_id

    url(r'/order/allinpay/(\d*)/([\w\W]*).html',AllinPayPaymentHandler,name='allinpay_payment'),#通联支付
    url(r'/order/allinpay/payback/(\d*)/([\w\W]*).html',AllinPayBackHandler,name='allinpay_payment_payback'),#通联支付回调
]
#易汇金支付
from ehking_handler import *
_handlers.extend([
    url(r'/order/ehking/(\d*)/([\w\W]*).html',EhkingPaymentHandler,name='ehking_payment'),#易汇金支付
    url(r'/order/ehking/payback/(\d*)/([\w\W]*).html',EhkingBackHandler,name='ehking_payment_payback'),#易汇金付回调
    ]
)


#微信支付
from weixin_handler import *
_handlers.extend([
    url(r'/order/weixin/qrpay/notify/', WeixinPayNotify,name='weixin_pay_back'),  #微信支付回调等待回调
    url(r'/order/weixin/pay/get_accesstoken/([\w\W]*)',WeixinAccessToken,name='weixin_access_token'),
    url(r'/order/weixin/pay/startpayment/([\w\W]*).html',WeixinPayment,name='weixin_pament'),
    url(r'/order/weixin/qcode/pay/([\w\W]*)',WeixinQcodeHandler,name='weixin_qcode_pay'),

    ])

#支付宝支付
from alipay_handler import *
_handlers.extend([
    url(r'/order/alipay/payback/',AlipayBackHandler,name='alipay_payment_payback'),#支付宝回调
    url(r'/order/alipay/(\d*)/([\w\W]*).html',AliPayPaymentHandler,name='alipay_payment'),#支付宝回到哦
    ]

)