#encoding:utf-8
__author__ = 'binpo'

from services.base_services import BaseService
from models.admin_do import AdminUser,UserRoles
from utils.md5_util import create_md5
import uuid

class AdminServices(BaseService):

    def _add(self,**kwargs):
        '''
        添加后台用户
        :param kwargs:
        :return:
        '''
        admin_user = AdminUser()
        admin_user.uid = self.user_uid()
        admin_user.phone = kwargs.get('tel').strip()
        admin_user.real_name = kwargs.get('real_name').strip()
        admin_user.user_name = kwargs.get('user_name').strip()
        admin_user.user_pwd = self.user_passed(kwargs.get('newpassword')).strip()
        admin_user.sex = kwargs.get('sex')               #
        self.db.add(admin_user)
        self.db.flush()
        roles = kwargs.get('roles')
        for r in roles:
            user_role = UserRoles()
            user_role.user_id = admin_user.id
            user_role.role_id = r
            self.db.add(user_role)
        self.db.commit()

    def user_passed(self,passowrd):
        '''
        生成密码
        :param uid:
        :param passowrd:
        :return:
        '''
        return create_md5(create_md5(create_md5(passowrd)))


    def user_uid(self,**kargs):
        """
        :todo 生成uuid
        :param name 用户名 如果是手机注册用手机号  微信注册用微信号
        """
        uuid_str = uuid.uuid4()
        return str(uuid_str)

    def add_roles(self):
        pass

    def _list(self,**kwargs):
        '''
        查询
        :param kwargs:
        :return:
        '''
        query = self.rdb.query(AdminUser).filter(AdminUser.deleted==0)
        if kwargs.get('order_by'):
            query = query.order_by(kwargs.get('order_by'))
        else:query = query.order_by('gmt_created desc')
        return query


    def _login(self,**kargs):
        '''
            用户登录
        '''
        from sqlalchemy import or_
        username = kargs.get('username')
        password = kargs.get('password')
        user = self.rdb.query(AdminUser).filter(AdminUser.deleted==0,AdminUser.user_pwd==self.user_passed(password),AdminUser.user_name==username).scalar()

        return user

    def check_user_passwd(self,username,password):
        pass

    def to_dict(self,user):
        keys=['id','nick','email','real_name','phone','nick']
        cookies={key:getattr(user,key) for key in keys}
        return cookies


    #def to_dict(self,user,**kwargs):
