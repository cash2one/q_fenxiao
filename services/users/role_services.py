#encoding:utf-8
'''
Created on 2014-5-28

@author: qiuyan.zwp
'''
from models.admin_do import *
from services.base_services import BaseService

class RoleServices(BaseService):

    def _list(self,**kwargs):

        query = self.rdb.query(Roles)
        if kwargs.has_key('id'):
            query = query.filter(Roles.id == int(kwargs.get('id')))
        if kwargs.has_key('role_permission_id'):
            query = query.filter(RolePermissions.id == int(kwargs.get('role_permission_id')),RolePermissions.role_id==Roles.id)
        if kwargs.has_key('code'):
            query = query.filter(Roles.code == kwargs.get('code'))
        if kwargs.has_key('name'):
            query = query.filter(Roles.name == kwargs.get('name'))
        if kwargs.has_key('order_by'):
            query = query.order_by(kwargs.get('order_by'))
        else:
            query = query.order_by('gmt_created desc')
        return query
        #return self.rdb.query(Roles).filter(Roles.deleted==1).order_by('gmt_created desc')

    @classmethod
    def role_format(cls,db,role_code):
        if role_code:
            role_names = db.query(Roles.name).filter(Roles.code.in_(role_code.split(',')))
            return ','.join([r.name for r in role_names])
        else:
            return ''

    def query_role(self, **kwargs):
        """
        :查询商品信息
        """
        query = self.rdb.query(Roles)

        if kwargs.has_key('id'):
            query = query.filter(Roles.id == int(kwargs.get('id')))
        if kwargs.has_key('role_permission_id'):
            query = query.filter(RolePermissions.id == int(kwargs.get('role_permission_id')),RolePermissions.role_id==Roles.id)
        if kwargs.has_key('code'):
            query = query.filter(Roles.code == kwargs.get('code'))
        if kwargs.has_key('name'):
            query = query.filter(Roles.name == kwargs.get('name'))
        if kwargs.has_key('order_by'):
            query = query.order_by(kwargs.get('order_by'))
        else:
            query = query.order_by('gmt_created desc')
        return query

    def create_role(self, **kwargs):
        self.db.execute(
            Roles.__table__.insert(),kwargs
        )
        self.db.commit()

    def update_role(self,role_id, **kwargs):
        '''
        更新角色
        :param role_id:
        :param kwargs:
        :return:
        '''
        self.db.query(Roles).filter(Roles.id==role_id).update(kwargs)
        self.db.commit()


    def _permission_list(self, **kwargs):
        """
        :权限列表
        """
        query = self.rdb.query(Permission)

        if kwargs.has_key('id'):
            query = query.filter(Permission.id == int(kwargs.get('id')))
        if kwargs.has_key('code'):
            query = query.filter(Permission.code == kwargs.get('code'))
        if kwargs.has_key('name'):
            query = query.filter(Permission.name == kwargs.get('name'))
        return query

    def _group_list(self):
        '''
        分组列表
        :return:
        '''
        return self.rdb.query(Group).filter(Group.deleted==0)

    def create_permission(self, **kwargs):
        self.db.execute(
            Permission.__table__.insert(),kwargs
        )
        self.db.commit()

    def get_permission_by_id(self,permission_id):
        '''
        根据权限id查询权限
        :param permission_id:
        :return:
        '''
        return self.rdb.query(Permission).filter(Permission.id==permission_id).scalar()

    def update_permission(self,id, **kwargs):
        '''
        更新权限
        :param id:
        :param kwargs:
        :return:
        '''
        self.db.query(Permission).filter(Permission.id==id).update(kwargs)
        self.db.commit()


    def query_role_permission(self, **kwargs):
        """
        :查询商品信息
        """
        query = self.rdb.query(RolePermissions)

        if kwargs.has_key('id'):
            query = query.filter(RolePermissions.id == int(kwargs.get('id')))
        if kwargs.has_key('role_id'):
            query = query.filter(RolePermissions.role_id == kwargs.get('role_id'))
        if kwargs.has_key('permission_id'):
            query = query.filter(RolePermissions.permission_id == kwargs.get('permission_id'))
        return query

    def create_role_permission(self, **kwargs):
        self.db.execute(
            RolePermissions.__table__.insert(),kwargs
        )
        self.db.commit()

    def update_role_permission(self,id, **kwargs):
        self.rdb.query(RolePermissions).filter(RolePermissions.id==id).update(kwargs)
        return ''

    def get_permision_name_by_role_id(self,role_id):

        self.rdb.query(Permission.name,Roles,RolePermissions).filter(Roles.id==role_id,RolePermissions.role_id==role_id,RolePermissions.permission_id==Permission.id)