#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'binpo'

from tornado.web import url
from base_handler import *


handlers = [
    url(r'/supply/index.html', SupplyHomeHandler,name='supply_index_html'),
    url(r'/supply/orders/index.html', OrdersHandler,name='supply_orders'),
    url(r'/supply/orders/detail.html', OrderDetailHandler,name='supply_order_detail'),
    url(r'/supply/orders/express.html', ExpressHandler,name='supply_express'),
    url(r'/supply/express_detail.html', ExpressCheckHandler,name='supply_express_detail'),
]