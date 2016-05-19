#encoding:utf-8
__author__ = 'gaoaifei'

from tornado.web import url
from handlers import *

_handlers = [
    url(r'/help/agreement.html',PaymentHandlers,name='payment'),
    url(r'/help/([\w\W]*).html',HelpHandlers,name='site_help'),

]