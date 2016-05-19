#encoding:utf-8
__author__ = 'binpo'

from apps_api.api_express_handler import *
from tornado.web import url


_handlers = [
    url(r'/api/express',ExpressHandler,name='express'),
    url(r'/api/batch_express',BatchExpressHandler,name='batch_express'),

]
