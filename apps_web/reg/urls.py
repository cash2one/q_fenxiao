#ecoding:utf-8
__author__ = 'binpo'

from tornado.web import url
from handlers import *

_handlers = [
    url(r'/reg.html',RegHandlers,name='reg'),
    url(r'/login.html',LoginHandler,name='login'),
    url(r'/ajax/login.login',AjaxLoginHandler,name='ajax_login'),
    url(r'/logout.html',LoginOutHandler,name='login_out'),
    url(r'/getpwd.html',FindBackPasswordHandler,name='findbackpwd'),
    url(r'/checklogin.html',CheckLoginHander,name='check_login')#判断用户是否登录
]