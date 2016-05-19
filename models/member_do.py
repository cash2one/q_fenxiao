#encoding:utf-8
__author__ = 'gaoaifei'

from base_do import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, SmallInteger,Text,Date,Float
from sqlalchemy import event
from sqlalchemy.sql.functions import now

class MemberCollections(Base):
    '''我的收藏表'''
    __tablename__ = 'member_collections'

    item_id = Column(Integer,doc='商品ID')
    user_id = Column(Integer,doc='用户id')

class MemberBrands(Base):
    '''关注的品牌'''
    __tablename__ = 'member_brands'

    brand_id = Column(Integer,doc='品牌ID')
    user_id = Column(Integer,doc='用户id')

class MemberSeachhistorys(Base):
    '''搜索历史记录'''
    __tablename__ = 'member_search_historys'
    search_key = Column(String(128),nullable=False)  #搜索关键字
    user_id = Column(Integer,doc='用户id')


