#encoding:utf-8

__author__ = 'gaoaifei'

from tornado.web import url
from handlers import *

_handlers = [
    url(r'/admin/advertis/position/([\w\W]*)',AdvertisingPositionHandler,name='advertising_position'),
    url(r'/admin/advertis/advertising/([\w\W]*)',AdvertisingHandler,name='advertising'),
]

