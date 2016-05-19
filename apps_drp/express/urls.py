#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'gaoaifei'

from tornado.web import url
from handlers import ExpressHandler,ExpressCheckHandler

_handlers=[
        url(r'/drp/orders/express.html', ExpressHandler,name='drp_express'),
        url(r'/drp/express_detail.html', ExpressCheckHandler,name='drp_express_detail'),
]
