#encoding:utf-8
__author__ = 'qiuyan'

from common.base_handler import AdminBaseHandler
from models.employee import *
class DepartmentHandler(AdminBaseHandler):

    def get(self, *args, **kwargs):
        departments = self.rdb.query(Department).filter(Department.deleted==0).order_by('gmt_created desc')
        if 'add' in self.request.query:
            self.echo('admin/employee/add_department.html',{'departments':departments})
        else:
            self.echo('admin/employee/department_list.html',{'departments':departments})

    def post(self, *args, **kwargs):
        pass



class EmployeeHandler(AdminBaseHandler):
    def get(self, *args, **kwargs):
        if 'add' in self.request.query:
            departments = self.rdb.query(Department).filter(Department.deleted==0).order_by('gmt_created desc')
            self.echo('admin/employee/add_employee.html',{'departments':departments})
        else:
            employees = self.rdb.query(Employee).filter(Employee.deleted==0).order_by('gmt_created desc')
            self.echo('admin/employee/employee_list.html',{'employees':employees})


    def post(self, *args, **kwargs):
        pass
