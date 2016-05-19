#encoding:utf-8
__author__ = 'wangjinkuan'

from apps_admin.payment.handlers import *
from apps_admin.payment.refund_handlers import *
from tornado.web import url

_handlers = [
    url(r'/admin/payment',PaymentHandler,name="payment"),
    url(r'/admin/refund/list.html',AllinPayRefundHandlers,name="refund_list"),
    url(r'/admin/refund/order_refund/(\d*).html',OrderRefundHandler,name="refund_payment"),
    url(r'/admin/refund/refund_apply/(\d*).html',RefundDealHandler,name="refund_payment_deal"),
    url(r'/admin/pay/excel',PaymentExcelHandler,name="pay_excel"),

]