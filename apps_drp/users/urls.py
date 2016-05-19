#encoding:utf-8
__author__ = 'gaoaifei'

from apps_drp.users.user_handlers import *
from tornado.web import url

_handlers = [
    url(r'/drp/users/list.html',Userhandlers,name="drp_users"),
    url(r'/drp/users/add.html',UserAddHandler,name="drp_add_user"),

]
