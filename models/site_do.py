#encoding:utf-8
__author__ = 'binpo'
from base_do import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, SmallInteger,Text

class SiteNav(Base):

    __tablename__ = 'site_nav'

    name = Column(String(64),doc='名称')
    category_id = Column(Integer,doc='一级类目ID',default='')
    show_id = Column(Integer,doc='',default='')
    link = Column(String(256),doc='链接',default='')
    enable = Column(Boolean,doc='可用',default=20)
    sort = Column(SmallInteger,doc='排序')
    open_type = Column(SmallInteger,doc='打开方式')  #0.当前页面  1.新页面
    is_app_start = Column(Boolean, default=False) #是否在app页面开启 0:关闭  1:开启

class SiteFeedback(Base):
    '''用户反馈'''

    __tablename__ = 'site_feedback'

    user_id = Column(Integer,doc="用户ID")
    title = Column(String(50))
    description = Column(Text)               #权限描述
    status = Column(SmallInteger)                   #状态


class AboutType(Base):
    __tablename__='site_about_type'

    type_name=Column(String(100))
    code_name = Column(String(128))

class About(Base):

    AboutType=[(3,'网站条款'),(2,'加入我们'),(1,'联系我们'),(0,'关于我们')]

    __tablename__ = 'site_about'

    code_name = Column(String(128))
    about_type_id=Column(Integer)
    description = Column(Text)                      #内容


class Job(Base):

    __tablename__ = 'site_job'

    HOT_CHOICE=[(1,'热门职位'),(0,'普通职位')]
    JOBTYPE=[(3,'销售类'),(2,'服务类'),(1,'研发设计类'),(0,'产品运营类')]#研发设计类；产品运营类，服务类

    department = Column(String(128),doc='部门')
    job_type = Column(String(128),doc='工作类型')
    jobname = Column(String(128),doc='职位名称')
    city = Column(String(32),doc='城市')
    description = Column(Text,doc='职位介绍')#="部门和职位介绍")
    jobrequire = Column(String(2000),doc='职位要求')#m odels.TextField(verbose_name="我合适吗")
    start_at = Column(DateTime)#models.DateField(verbose_name="开始时间")
    end_at = Column(DateTime)#models.DateField(verbose_name="截止时间")

class Links(Base):

    __tablename__ = 'links'

    name = Column(String(128))
    link = Column(String(256))       #链接
    desc = Column(String(256))      #描述

class SiteNoticePosition(Base):
    '''
    站点公告位置表
    '''
    __tablename__ = 'site_notice_position'

    name = Column(String(250),doc='位置名称')
    code_name = Column(String(250),doc='位置code')
    description = Column(String(255),doc='描述')

class SiteNotice(Base):
    '''
    站点公告表
    '''
    __tablename__ = 'site_notice'

    position_id = Column(Integer,doc='位置ID')
    name = Column(String(255),doc='公告名称')
    start_time =  Column(DateTime,doc='公告开始时间')
    end_time = Column(DateTime,doc='公告结束时间')
    is_open = Column(Integer,doc='公告是否开启 0开启 1关闭 默认开启状态',default=0)
    content = Column(Text,doc='公告描述')




















