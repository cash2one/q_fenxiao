#encoding:utf-8
__author__ = 'qiuyan'

from handlers import *
from tornado.web import url

_handlers = [

    url(r'/admin/employee/department.html',DepartmentHandler,name='departments'),
    url(r'/admin/employee/employee.html',EmployeeHandler,name='employees'),
]