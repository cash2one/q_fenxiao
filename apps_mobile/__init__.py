#encoding:utf-8
__author__ = 'binpo'
from tornado.web import url
from home import *

handlers=[
     url(r"/",HomeHandler, name="home_handler"),
     url(r'/selected_items.html',SelectGoodHandler,name='selected_goods'),
     url(r'/drp/shop/([\w\W]*).html',ShopSiteHandler,name='shop_site')
]

from reg.urls import _handlers as reg_handlers
handlers.extend(reg_handlers)

from items.urls import _handlers as item_handlers
handlers.extend(item_handlers)

from member.urls import _handlers
handlers.extend(_handlers)

from orders.urls import _handlers as order_handlers
handlers.extend(order_handlers)

from payment.urls import _handlers
handlers.extend(_handlers)

from help.urls import _handlers
handlers.extend(_handlers)


handlers.append(url(r"/([\w\W]*)",TmsHandler, name="tms_handler"),)
