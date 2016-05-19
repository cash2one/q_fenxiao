#encoding:utf-8
__author__ = 'wangjinkuan'

from apps_drp.orders.handlers import *
from tornado.web import url

_handlers = [
    url(r'/drp/orders.html',OrderHandler,name='drp_orders'),
    url(r'/drp/order/detail/([\w\W]*)',OrderDetailHandler,name='drp_detail_order'),
    url(r'/drp/payorders/index.html',PaymentHandlers,name='drp_pay_orders'),
    url(r'/drp/settlement/index.html',SettlementHandler,name='drp_settlement'),
    # url(r'/drp/edit/order/([\d]*)/([\d]*)/([\d]*)',EditOrderHandler,name='edit_order'),
    url(r'/drp/express/check',ExpressCheckHandler,name='drp_express_check'),
    url(r'/drp/sold_items.html',SoldItemsHandler,name='drp_sold_items'),
]

_mobile_handlers = [
    url(r'/drp/mobile/orders',OrderHandler,name='drp_mobile_orders'),
    url(r'/drp/mobile/order/detail/([\w\W]*)',OrderDetailHandler,name='drp_mobile_order_detail'),
    # url(r'/drp/mobile/edit/order/([\d]*)/([\d]*)/([\d]*)',EditOrderHandler,name='admin_mobile_edit_order'),
    # url(r'/drp/mobile/express/check',ExpressCheckHandler,name='admin_mobile_express_check'),
]

_handlers.extend(_mobile_handlers)