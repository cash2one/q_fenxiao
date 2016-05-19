#encoding:utf-8
__author__ = 'binpo'

from sqlalchemy.sql.functions import now
from models.base_do import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean,SmallInteger

class AdminUser(Base):

    __tablename__ = 'admin_users'

    uid = Column(String(128))
    nick = Column(String(128),nullable=True,default='')
    email = Column(String(128),nullable=True,default='')
    phone = Column(String(256),default="")
    real_name = Column(String(128)) #用户真实名字
    user_name = Column(String(256),nullable=False)                         #用户名称。
    user_pwd = Column(String(256),nullable=False)                          #用户密码
    sex = Column(String(10),default=u"未知")
    # type = Column(Integer,nullable=False,default=0,doc='用户类型：0管理员 1分销商 2供应商 默认为管理员用户')
    #photo = Column(String(256),default="")                #用户头像

    def to_dict(self):
        keys=['id','nick','email','real_name','phone','nick']
        cookies={key:getattr(self,key) for key in keys}
        return cookies




class Permission(Base):

    __tablename__ = 'permission'

    path = Column(String(256),nullable=False,default='',doc='访问路径')
    name = Column(String(50),nullable=False,default='')
    description = Column(String(200),nullable=True,default='')               #权限描述

class Roles(Base):

    __tablename__ = 'roles'

    code = Column(String(50),nullable=False,default='')
    name = Column(String(50),nullable=False,default='')
    description = Column(String(200),nullable=True,default='')         #角色描述

class Group(Base):
    __tablename__ = 'group'

    name = Column(String(50),nullable=False,default='')
    description = Column(String(200),nullable=True,default='')         #分组描述

class GroupPermission(Base):

    __tablename__ = 'group_permision'

    permission_id = Column(Integer,nullable=False)
    group_id = Column(Integer,nullable=False)


class RolePermissions(Base):

    """角色的权限"""

    __tablename__ = 'role_permissions'

    permission_id = Column(Integer,nullable=False)
    role_id = Column(Integer,nullable=False)


class UserRoles(Base):

    """用户角色"""
    __tablename__ = 'user_roles'

    user_id = Column(Integer,nullable=False)
    role_id = Column(Integer,nullable=False)