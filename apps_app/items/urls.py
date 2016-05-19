#encoding:utf-8
__author__ = 'wangjinkuan'

from apps_app.items.handlers import *
from tornado.web import url

_handlers = [
    url(r'/api/json/item/list/(\d*).html',APPItemsListHandler,name='app_item_list'),
    url(r'/api/json/category',AppCategoryHandler,name='app_category'),
    url(r'/h5/item/detail/(\d*).html',ItemsDetailHandler,name='h5_item_detail'),

    url(r'/api/json/item/detail/(\d*)',ItemsDetailHandler,name='app_item_detail'),
]