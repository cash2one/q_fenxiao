#encoding:utf-8
__author__ = 'binpo'

import datetime
from date_util import yyyydddddatetime
from decimal import  Decimal

def modelobj_to_dict(objlist,dateformat='%Y-%m-%d %H:%M:%S'):

    """
    :todo orm对象转字典
    :param objlist:对象结合或者对象
    :param dateformat:时间字段的格式化方式

    """
    if type(objlist) in (list,tuple):#对象集合
        temp_list = []
        for obj in objlist:
            obj.__dict__.pop('_sa_instance_state')
            for o in obj.__dict__.keys():
                if type(obj.__dict__[o])==datetime.datetime:
                    obj.__dict__.pop(o)# = yyyydddddatetime(dateformat,obj.__dict__[o])
                elif type(obj.__dict__[o]) == Decimal:
                    obj.__dict__[o] = float(obj.__dict__[o])
            temp_list.append(obj.__dict__)
        return temp_list
    else:#对象本身
        print dir(objlist)
        print type(objlist)
        objlist.__dict__.pop('_sa_instance_state')
        for o in objlist.__dict__.keys():
            if type(objlist.__dict__[o])==datetime.datetime:
                objlist.__dict__.pop(o)
            elif type(objlist.__dict__[o]) == Decimal:
                objlist.__dict__[o] = float(objlist.__dict__[o])
        return objlist.__dict__

# from sqlalchemy.sql.functions import now
# from models.decorate_do import Tags
#
#
# from models.advertise_do import *
# from models.app_do import *
#
# from models.banner_do import *
# from models.location_do import *
# from models.decoratehelp_do import *
# from models.user_do import *
# from models.config_do import *
#
# from models.decorate_do import *
#
# from sqlalchemy import create_engine, MetaData,ForeignKey
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm.session import sessionmaker
# from models.base_do import Base
#
# def add_a_tag():
#
#
#     mysql_engine = create_engine('mysql://root:111111@localhost:3306/decorate?charset=utf8',encoding = "utf-8",echo =True)
#     # Base.metadata.create_all(mysql_engine)
#
#     Session = sessionmaker(bind=mysql_engine)
#     session = Session()
#
#     tag = Tags()
#     tag.ag_type = 'hello'
#     tag_name = 'hello'
#     tag.gmt_created = now()
#     tag.gmt_modified = now()
#     tag.deleted = 0
#
#     session.add(tag)
#
#
#     ban = Banner()
#     ban.name = ''
#     ban.image = ''            #banner图片
#     ban.value = ''
#     ban.value_type = 1           #1 list 2.call back  3. h5  4.Image. 5. 自定类型拓展类型
#
#     ban.start_time = now()             #展示时间
#     ban.expire_time = now()               #展示结束时间
#     ban.gmt_created = now()
#     ban.gmt_modified = now()
#     ban.deleted = 0
#     session.add(ban)
#     session.commit()
#
#
# mysql_engine = create_engine('mysql://root:111111@localhost:3306/decorate?charset=utf8',encoding = "utf-8",echo =True)
# # Base.metadata.create_all(mysql_engine)
#
# Session = sessionmaker(bind=mysql_engine)
# session = Session()
# tag = session.query(Tags).filter(Tags.id==1).scalar()
# ban = session.query(Banner).filter(Banner.id==1).scalar()
# print dir(tag)
# print tag.__dict__
# print tag.__table__
# print dir(tag.__dict__)
# tag.__dict__.pop('_sa_instance_state')
# print tag.__dict__
#
# print dir(ban)
# print ban.__dict__
# print ban.__table__
# print dir(ban.__dict__)
#
# ban.__dict__.pop('_sa_instance_state')
# print ban.__dict__