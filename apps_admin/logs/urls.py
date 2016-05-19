#encoding:utf-8
__author__ = 'wangjinkuan'

from tornado.web import url
from .api_handlers import *
from .operation_handlers import *

_handlers = [
    url(r'/admin/logs/api/',ApiHandlers,name='api_logs'),
    url(r'/admin/logs/operation/',OperationHandlers,name='operation_logs'),
]

