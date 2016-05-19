#ecoding:utf-8
__author__ = 'gaoaifei'

from tornado.web import url
from handlers import *

_handlers = [
    url(r'/reg.html',RegHandlers,name='reg'),#注册
    url(r'/login.html',LoginHandler,name='login'),#登陆
    url(r'/ajax/login.login',AjaxLoginHandler,name='ajax_login'),
    url(r'/logout.html',LoginOutHandler,name='login_out'),#退出登录
    url(r'/getpwd.html',FindBackPasswordHandler,name='findbackpwd'), #找回秘密
    url(r'/getuserinfo.html',GetUserinfoHandler,name='user_info'),#取用户信息
]