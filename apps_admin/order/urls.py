#encoding:utf-8
__author__ = 'wangjinkuan'

from apps_admin.order.handlers import *
from tornado.web import url

_handlers = [
    url(r'/admin/orders',OrderHandler,name='orders'),
    url(r'/admin/order/detail/([\w\W]*)',OrderDetailHandler,name='detail_orders'),
    url(r'/admin/orders/excel',BuildHandler,name='orders_excel'),
    url(r'/admin/express/check',ExpressCheckHandler,name='express_check'),
    url(r'/admin/edit/order/([\d]*)/([\d]*)/([\d]*)',EditOrderHandler,name='edit_order'),
    url(r'/admin/sold_items',SoldItemsHandler,name='sold_items'),
]

_mobile_handlers = [
    url(r'/admin/mobile/orders',OrderHandler,name='admin_mobile_orders'),
    url(r'/admin/mobile/order/detail/([\w\W]*)',OrderDetailHandler,name='admin_mobile_order_detail'),
    url(r'/admin/mobile/edit/order/([\d]*)/([\d]*)/([\d]*)',EditOrderHandler,name='admin_mobile_edit_order'),
    url(r'/admin/mobile/express/check',ExpressCheckHandler,name='admin_mobile_express_check'),
]

_handlers.extend(_mobile_handlers)