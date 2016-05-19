#encoding:utf-8
__author__ = 'wangjinkuan'

from apps_mobile.items.handlers import *
from tornado.web import url

_handlers = [
    url(r'/items',ItemsAsyncHandler,name='mobile_async_items'),
    url(r'/item/list/(\d*).html',ItemListHandler,name='mobile_item_list'),
    url(r'/item/detail/(\d*).html',ItemsDetailHandler,name='mobile_item_detail'),
]