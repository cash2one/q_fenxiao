#encoding:utf-8
__author__ = 'binpo'
from common.base_handler import AdminBaseHandler
from services.users.admin_services import AdminServices
from services.users.role_services import RoleServices
admin_service = AdminServices()
role_service = RoleServices()

class AccountHandler(AdminBaseHandler):

    def get(self,operation=None, *args, **kwargs):
        if operation == 'add':
            role_service.set_rdb(self.rdb)
            roles = role_service._list()
            self.echo('admin/account/add.html',{'roles':roles})
        else:
            admin_service.set_rdb(self.rdb)
            query = admin_service._list()
            data = self.get_page_data(query)
            self.echo('admin/account/_list.html',{'data':data})

    def post(self,operation=None, *args, **kwargs):
        self.get_paras_dict()
        admin_service.set_db(self.db)
        admin_service._add(**self.qdict)
        self.write('ok')
