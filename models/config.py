#encoding:utf-8
__author__ = 'binpo'
from models.base_do import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, SmallInteger,Text,Numeric,Float

class Config(Base):

    __tablename__ = 'config'
    name = Column(String(64),doc='名称',default='')
    key = Column(String(32),doc='key',default='')
    value = Column(String(64),doc='值',default='')
    remark = Column(String(1024),doc='')
