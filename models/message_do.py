#encoding:utf-8
__author__ = 'zhaowenpeng'

from base_do import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, SmallInteger,Text
from sqlalchemy.sql.functions import now


class Message(Base):
    '''消息'''
    __tablename__='message'

    TEXT_TYPE = {0:'公共消息',1:'评论',2:'私信',3:'赞'}                                                              #内容定义

    message_type = Column(String(128), default='private')                   #消息类型
    content = Column(String(2048),default='消息内容')
    refer_id = Column(Integer,doc='相关ID')
    sender = Column(Integer,doc='发送者')                      #发送者
    receiver = Column(Integer,doc='消息接受者')                #消息接受者

    is_read = Column(Boolean,default=False)              #消息状态  0.为未读  1.已读
    is_pending = Column(Boolean,default=False)             #是否打开
