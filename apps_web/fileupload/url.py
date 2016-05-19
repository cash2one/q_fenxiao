#encoding:utf-8

__author__ = 'gaoaifei'

from tornado.web import url
from handlers import *

_handlers = [
    url(r'/item/comment/uploadimage.html',FileManagerHandler,name='img_upload'),

]