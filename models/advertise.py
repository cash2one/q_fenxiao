#encoding:utf-8
__author__ = 'binpo'
from models.base_do import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, SmallInteger,Text,Numeric,Float
from sqlalchemy.sql.functions import now
from sqlalchemy import event



class AdvertisingPosition(Base):
    '''广告位置表'''
    __tablename__ = 'advertising_position'

    name = Column(String(250),doc='广告位置名称')
    code_name = Column(String(250),doc='广告位置code')
    width = Column(Integer,doc='广告位宽度')
    height = Column(Integer,doc='广告位高度')
    category_id = Column(Integer,doc='类目页滑动banner',nullable=True,default=0)
    description = Column(String(255),doc='广告位描述')

class Advertising(Base):

    '''广告表'''
    __tablename__ = 'advertising'

    position_id = Column(Integer,doc='广告位ID')
    name = Column(String(50),doc='广告名称，并非显示在广告中')
    media_types = Column(Integer,doc='媒介类型:1图片；2文字；3:FLASH；4代码；5视频；6语音；7其他')
    ad_img = Column(String(256),doc='广告图片路径')
    ad_link = Column(String(256),doc='广告目标链接')
    sort = Column(SmallInteger,doc='多个滑动banner排序',default=0)
    start_time =  Column(DateTime,doc='开始时间')
    end_time = Column(DateTime,doc='结束时间')
    is_open = Column(Integer,doc='广告是否开启 0开启 1关闭 默认开启状态',default=0)
    contact = Column(String(128),doc='广告联系人')
    phone = Column(String(256),default="广告联系人电话")
    email = Column(String(128),default='联系人邮箱')
    description = Column(String(255),doc='广告描述')

class AdvertisingStatistics(Base):
    '''
    广告统计表
    '''
    __tablename__ = "advertising_statistics"

    ad_id = Column(Integer,doc='广告ID')
    page_view = Column(Integer,doc='广告点击次数',default=0)
    order_count = Column(Integer,doc='订单量',default=0)



@event.listens_for(Advertising, 'before_update')
def receive_before_update(mapper, connection, target):
    target.gmt_modified = now()

@event.listens_for(AdvertisingPosition, 'before_update')
def receive_before_update(mapper, connection, target):
    target.gmt_modified = now()

