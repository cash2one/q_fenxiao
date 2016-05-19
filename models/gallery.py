#encoding:utf-8
__author__ = 'binpo'

from models.base_do import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, SmallInteger,Text,Numeric,Float

class Gallery(Base):
    '''图库'''
    __tablename__ = 'gallery'

    pic_type = Column(SmallInteger,doc='类型',default=0)#晒单图,头像图  (0.商品图 2.晒单的图 3 个人头像 4.商品content图
    img_url = Column(String(256),doc='图片url,不含domain')
    full_url = Column(String(256),doc='图片全路径')
    size = Column(Integer,doc='图片大小')
