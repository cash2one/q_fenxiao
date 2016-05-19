#encoding:utf-8
__author__ = 'binpo'
from models.base_do import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean,SmallInteger,Text

class WorkOrderType(Base):

    '''工单类型'''
    __tablename__ = 'work_order_type'
    name = Column(String(128),nullable=False)       #工单名称
    desc = Column(String(1024),nullable=False)      #描述


class WorkOrder(Base):

    '''工单类型'''
    __tablename__ = 'work_order'

    work_order_type_id = Column(Integer,doc='工单类型')
    title = Column(String(128),nullable=False)       #工单名称
    content = Column(Text,nullable=False,default='')      #工单内容  ps:参数说明
    keyword = Column(String(512),doc='工单关键字')
    status = Column(SmallInteger,doc='工单状态')        # 0:待处理,1:跟进中,2:已解决,3:已关闭
    handle_user_id = Column(Integer,doc='处理人id')
    handle_user = Column(String(32),doc='处理人')
    comment = Column(Text,doc='处理过程记录')


# class ApiTasks(Base):
#
#     __tablename__ = 'api_tasks'
#