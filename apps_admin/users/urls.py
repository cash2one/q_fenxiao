#encoding:utf-8
__author__ = 'gaoaifei'

from apps_admin.users.user_handlers import *
from tornado.web import url

_handlers = [
    url(r'/admin/users/list/([\w\W]*)',Userhandlers,name="users"),
    url(r'/admin/users/address', Addresshandlers,name='addresses'),
    url(r'/admin/batch/business/([\w\W]*)',BusinessHandler,name='batch_business')
]

_mobile_handlers = [
    url(r'/admin/users/mobile/list/([\w\W]*)',Userhandlers,name="admin_mobile_users"),
]

_handlers.extend(_mobile_handlers)