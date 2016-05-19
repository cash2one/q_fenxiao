#ecoding:utf-8
__author__ = 'gaoaifei'

from tornado.web import url
from apps_app.reg.handlers import *

_handlers = [
    url(r'/api/json/reg.html',AppRegHandler,name='app_reg'),#app注册

    url(r'/api/json/login.html',AppLoginHandler,name='app_login'),#app登陆
]