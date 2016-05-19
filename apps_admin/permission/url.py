#encoding:utf-8
__author__ = 'binpo'

from tornado.web import url
from handlers import *

_handlers = [
    url(r'/admin/permission/([\w\W]*)',PermissionHandler,name='permission'),
    url(r'/admin/permission/(\d*)',PermissionHandler,name='permission_edit'),
    url(r'/admin/group/([\w\W]*)',GroupHandler,name='group'),
    url(r'/admin/roles/([\w\W]*)',RolesHandler,name='roles'),
    url(r'/admin/permission_roles',RolesPermissionHandler,name='permission_roles'),

]