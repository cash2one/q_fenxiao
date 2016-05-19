#encoding:utf-8
__author__ = 'binpo'
from common.base_handler import AdminBaseHandler
from services.users.permission_services import PermissonServices
from services.users.role_services import RoleServices
permission_serice = PermissonServices()
role_service = RoleServices()
class PermissionHandler(AdminBaseHandler):

    def get(self,operation=None,*args, **kwargs):
        if operation:
            if operation=='add':
                self.echo('admin/permission/add_permission.html')
            else:
                role_service.set_db(self.db)
                permission = role_service.get_permission_by_id(operation)
                self.echo('admin/permission/add_permission.html',{'permission':permission})
        else:
            role_service.set_rdb(self.rdb)
            query = role_service._permission_list()
            data = self.get_page_data(query)
            self.echo('admin/permission/_list.html',{'data':data})

    def post(self, *args, **kwargs):
        #update
        self.get_paras_dict()
        role_service.set_db(self.db)
        role_service.create_permission(**self.qdict)
        self.write('添加成功')


    def put(self, *args, **kwargs):
        #创建
        self.write('添加成功')


    def delete(self, *args, **kwargs):
        pass
        # pass


class GroupHandler(AdminBaseHandler):
    def get(self,operation=None, *args, **kwargs):
        if operation:
            if operation=='add':
                role_service.set_rdb(self.rdb)
                permissions = role_service._permission_list()
                self.echo('admin/permission/add_group.html',{'permissions':permissions})
        else:
            role_service.set_rdb(self.rdb)
            groups = role_service._group_list()
            self.echo('admin/permission/_group_list.html',{'groups':groups})


    def post(self, *args, **kwargs):
        pass


class RolesHandler(AdminBaseHandler):

    def get(self,operation=None,*args, **kwargs):
        if operation:
            if operation=='add':
                role_service.set_rdb(self.rdb)
                permissions = role_service._permission_list()
                self.echo('admin/permission/add_roles.html',{'permissions':permissions})
        else:
            role_service.set_rdb(self.rdb)
            roles = role_service._list()
            self.echo('admin/permission/_role_list.html',{'roles':roles})

    def get_permisson_name_by_role(self,id):
        #self.db.query(Or)
        pass

class RolesPermissionHandler(AdminBaseHandler):

    def get(self, *args, **kwargs):
        pass


    def post(self, *args, **kwargs):
        pass

