#encoding:utf-8
__author__ = 'binpo'

from tornado.web import url
from handlers import *

_handlers = [
    url(r'/admin/img/upload/([\w\W]*)',FileManagerHandler,name='img_upload'),

]