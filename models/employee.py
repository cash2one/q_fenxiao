#encoding:utf-8
__author__ = 'binpo'

from models.base_do import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, SmallInteger,Text,Numeric,Float
from sqlalchemy import event
from sqlalchemy.sql.functions import now

class Department(Base):

    __tablename__= 'department'

    name = Column(String(256),doc='部门名称')
    parent_id = Column(Integer,doc='父ID')

class Employee(Base):

    __tablename__= 'employee'

    name = Column(String(256),nullable=False)
    mobile = Column(String(256),nullable=False)
    email = Column(String(256),doc='邮件')
    manager = Column(Integer,doc='主管')
    position = Column(String(256),doc='职位')

class EmployeeCustomer(Base):
    '''地推大客户'''
    __tablename__= 'employee_customer'
    user_id = Column(Integer,doc='用户ID')
    employee_id = Column(Integer,doc='员工ID')
