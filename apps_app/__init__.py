#encoding:utf-8
__author__ = 'wangjinkuan'

from apps_app.home import HomeHandler
# from apps_app.common_handler import AppLocationHandler
from tornado.web import url

handlers = [
    url(r"/api/json",HomeHandler,name="app_ios_handler"),

    # url(r"/api/json/locations",AppLocationHandler,name="app_locations_handler"),
]

from apps_app.items.urls import _handlers as items_handlers
handlers.extend(items_handlers)

from apps_app.member.urls import _handlers as member_handlers
handlers.extend(member_handlers)

from apps_app.orders.urls import _handlers as order_handlers
handlers.extend(order_handlers)

from apps_app.reg.urls import _handlers as reg_handlers
handlers.extend(reg_handlers)

from apps_app.payment.urls import _handlers as payment_handlers
handlers.extend(payment_handlers)