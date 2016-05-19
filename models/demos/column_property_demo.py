#encoding:utf-8
__author__ = 'binpo'

from models.base_do import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import column_property
from ..demos import session

class AdminUser(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    firstname = Column(String(50))
    lastname = Column(String(50))
    fullname = column_property(firstname + " " + lastname)


admin_user = AdminUser()
admin_user.firstname = '赵文鹏'
admin_user.lastname = 'python工程师'
session.add(admin_user)
session.commit()