# -*- coding: utf-8 -*-

from sqlalchemy import Integer, Column, String, DateTime, Boolean
from models.base_do import Base

class Country(Base):
    """
        国家信息表
    """
    __tablename__ = 'country'

    code = Column(Integer)
    name_chinese = Column(String(128),default='')
    name_english = Column(String(128))
    national_flag = Column(String(256),doc='国旗')
    yh_code = Column(String(128),default='')

    def to_dict(self):
        dic = {}
        dic["id"] = self.id
        dic["code"] = self.key_name
        dic["name_chinese"] = self.name_chinese
        dic["name_english"] = self.name_english
        return dic

class Province(Base):
    """
        省份信息
    """
    __tablename__ = 'province'

    province_id = Column(Integer)
    name = Column(String(128))                 #省份名称
    yh_code = Column(String(128),default='')

    def to_dict(self):
        dic = {}
        dic["province_id"] = self.province_id
        dic["province_name"] = self.province_name
        return dic


class City(Base):
    """
    城市信息
    """
    __tablename__ = 'city'

    city_id = Column(Integer)
    name = Column(String(128))                 #城市名称
    zip_code = Column(String(10))
    father = Column(Integer)
    yh_code = Column(String(128),default='')

    def to_dict(self):
        dic = {}
        dic["province_id"] = self.father
        dic["city_id"] = self.city_id
        dic["city_name"] = self.city_name
        return dic


class Area(Base):
    """
        区域信息
    """
    __tablename__ = 'area'

    area_id = Column(Integer)
    name = Column(String(128))                 #区域名称
    father = Column(Integer)
    zipcode = Column(String(10),doc='邮编')          #区域邮编
    yh_code = Column(String(128),default='')

    def to_dict(self):
        dic = {}
        dic["area_id"] = self.area_id
        dic["city_id"] = self.father
        dic["area_name"] = self.area_name
        return dic


# class Community(Base):
#     __tablename__ = 'community'
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String(128))
#     address = Column(String(128))
#     area = Column(Integer)
#     city = Column(Integer)
#     province = Column(Integer)
#     gmt_created = Column(DateTime, default=now())
#     gmt_modified = Column(DateTime, default=now())
#     deleted = Column(Boolean, default=0)
#
#
# class UserLocation(Base):
#     """
#         用户位置信息
#     """
#     __tablename__="user_location"
#
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer)
#     area_id = Column(Integer,nullable=True)
#     city_id = Column(Integer,nullable=True)
#     province_id = Column(Integer,nullable=True)
#
#     gmt_created = Column(DateTime,default=now())
#     gmt_modified = Column(DateTime,default=now())
#     deleted = Column(Boolean,default=0)
#
