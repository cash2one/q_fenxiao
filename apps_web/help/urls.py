#encoding:utf-8
__author__ = 'binpo'

from tornado.web import url
from handlers import *

_handlers = [
    url(r'/help/([\w\W]*).html',HelpHandlers,name='site_help'),
]