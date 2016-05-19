#encoding:utf-8
__author__ = 'gaoaifei'

from tornado.web import url
from handlers import *

_handlers = [
    url(r'/elastic/search.html',ElasticsearchHandler,name='search'),
]