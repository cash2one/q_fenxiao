#encoding:utf-8
__author__ = 'wangjinkuan'

from apps_admin.attributes.handlers import *
from tornado.web import url

_handlers = [
    url(r'/admin/attributes/([\w\W]*)',AttributesHandler,name='attributes'),
    url(r'/admin/attribute/value/([\w\W]*)',AttributeValueHandler,name='attribute_values')
]