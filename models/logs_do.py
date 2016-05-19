#encoding:utf-8
__author__ = 'zhaowenpeng'
"""
 访问日志
 操作日志
 错误日志
 异常定义
"""

from base_do import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, SmallInteger,Text

class ApiLogs(Base):

    __tablename__ = 'api_logs'

    logs_type = Column(SmallInteger,doc='日志类型')     #1.悦华清关接口  2.物流接口
    key_params = Column(Text,doc='关键参数',default='')
    reqeust_url = Column(String(512),doc='请求URL')
    params = Column(Text,doc='请求参数')
    action = Column(String(32),doc='方法类型')      #post  get
    result = Column(String(2048),doc='返回值')
    status = Column(SmallInteger,doc='状态值')     #1.正常，0:错误需要人工处理 2:部分错误需要处理
    error = Column(String(1024),doc='错误信息')    #执行错误信息记录 做容错处理


class OperationLogs(Base):

    '''操作日志'''

    __tablename__ = 'operation_logs'
    reqeust_url = Column(String(512),doc='请求URL')
    params = Column(String(2048),doc='请求参数')
    action = Column(String(32),doc='方法类型')      #post  get
    content = Column(String(2048),doc='返回值')
    opration_name = Column(String(128),doc='操作名称')
    opration_user = Column(Integer,doc='操作用户名单',default=0)


class Tasks(Base):

    __tablename__ = 'tasks'

    task_type = Column(SmallInteger,doc='任务类型')     #1.悦华清关接口  2.物流接口 3.回调接口
    key_params = Column(Text,doc='关键参数',default='')
    _url = Column(String(512),doc='请求URL')
    params = Column(Text,doc='请求参数')
    action = Column(String(32),doc='方法类型')      #post  get
    result = Column(Text,doc='返回值')
    status = Column(SmallInteger,doc='状态值')     #0:待执行 1.自动执行， 2:手动执行
    error = Column(String(2048),doc='错误信息')    #执行错误信息记录 做容错处理
