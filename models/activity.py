#encoding:utf-8
__author__ = 'binpo'
from models.base_do import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, SmallInteger,Text,Numeric,Float,Date

class ActivityType(Base):

    __tablename__='activity_type'
    code = Column(String(32),doc='代码',default='')
    name = Column(String(32),doc='活动名称',default='')             #满减，立减，折扣，现金券，返现，积分抵现，赠送积分 满减，满赠，满购，满加，搭配，等好多的
    description = Column(String(2048),doc='活动规则描述',default='')


class ActivityItems(Base):

    __tablename__='activity_items'

    activity_type_id = Column(Integer,doc='活动类型ID')

    item_id = Column(Integer,doc='商品id')
    category_id = Column(Integer,doc='商品类目ID')
    #full_category_id = Column(String,doc='商品类目ID')
    start_date = Column(Date,doc='活动开始日期')
    end_date = Column(Date,doc='活动开始日期')
