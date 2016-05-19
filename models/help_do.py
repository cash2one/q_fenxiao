#encoding:utf-8
__author__ = 'binpo'
from base_do import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, SmallInteger,Text

class AskType(Base):
    '''问题类型'''
    __tablename__ = 'ask_type'
    name = Column(String(16),doc='名称')

class OrderAsk(Base):

    '''帮助'''
    __tablename__ = 'order_ask'

    user_id = Column(Integer,doc="用户ID",nullable=True)
    ask_type_id = Column(Integer)
    order_num = Column(String(64),doc='订单编号')
    phone = Column(String(15),doc='电话')
    description = Column(String(1024),doc='问题描述')        #权限描述
    status = Column(SmallInteger)                           #状态   0:未受理,1:已经受理,2:关闭
    admin_user_id = Column(Integer,doc='处理人')
    admin_remark = Column(String(1024),doc='处理结果')


