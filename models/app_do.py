# -*- coding: utf-8 -*-

__author__ = 'zhaowenpeng'

from models.base_do import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, SmallInteger, Float
from sqlalchemy.sql.functions import now

class AppVersion(Base):
    """
    app 版本控制
    """
    __tablename__ = 'app_version'

    app_type = Column(String(32),doc='app类型')             # 3:ios app. 1:andrido app. 2: pc client.
    app_version = Column(String(128),doc='版本')           #app版本
    md5string = Column(String(128),doc="md5验证")             #md5验证
    app_url = Column(String(128),doc="下载地址")               #下载地址
    file_name = Column(String(128),doc='文件名称')              #文件名称
    app_size = Column(Integer,doc="大小")                  #大小
    app_desc = Column(String(1024),doc="描述")             #描述
