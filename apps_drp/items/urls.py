#encoding:utf-8
__author__ = 'wangjinkuan'

from tornado.web import url
from items_handler import ItemsHandler,ItemsOnlineHandler,ItemCreatHandler

_handlers=[
     url(r'/drp/items/list.html',ItemsHandler,name='drp_items'),
     url(r'/drp/item_online/([\w\W]*).html',ItemsOnlineHandler,name='drp_item_online'),
     url(r'/drp/item/add/([\w\W]*)',ItemCreatHandler,name='drp_item_add'),
]


