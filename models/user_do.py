# -*- coding: utf-8 -*-
__author__ = 'binpo'

from models.base_do import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean,SmallInteger
from sqlalchemy.orm import validates
from sqlalchemy import event
from sqlalchemy.sql.functions import now
import ujson

# class Roles(Base):
#
#     __tablename__ = 'roles'
#
#     code = Column(String(50),nullable=False,default='')
#     name = Column(String(50),nullable=False,default='')
#     description = Column(String(200),nullable=True,default='')         #角色描述

class DistributorUser(Base):
    '''
    分销商用户表
    '''
    __tablename__ = 'users_distributor'

    STATUS={
        'normal':'正常',
        'inactive':'未激活',
        'delete':'删除',
        'reeze':'冻结'
    }
    uid = Column(String(128),doc='分销商uid唯一值')
    shop_id = Column(String(128),doc='店铺ID') #   like http://xiao.qqqg.com/shop/1234567.html 1234567为店铺ID
    parent_id = Column(Integer,nullable=True,default='0', doc='分销商父类id，默认为0，一级分销商')
    role_type = Column(Integer,nullable=True,default=0,doc='用户角色类型 0分销商 1供应商 默认为分销商')
    nick = Column(String(128),nullable=True,default='',doc='分销商昵称')
    email = Column(String(128),nullable=True,default='',doc='分销商邮箱地址')
    phone = Column(String(256),default="",doc='分销商联系电话')
    real_name = Column(String(128)) #分销商真实名字
    user_name = Column(String(256),nullable=False)                         #用户名称。
    user_pwd = Column(String(256),nullable=False)                          #用户密码
    sex = Column(String(10),default=u"未知")
    area = Column(String(512),default='',doc='分销商所属区域')
    status =  Column(String(16),default='normal')             #状态。可选值:normal(正常),inactive(未激活),delete(删除),reeze(冻结)#,supervise(监管)
    reeze_time =  Column(DateTime,nullable=True)                #冻结时间
    comments = Column(String(1024),default='',doc='备注')

    def user_format(self,user):
        keys = ['id','parent_id','shop_id','role_type','nick','email', 'phone','status','real_name','user_name','status', 'reeze_time']
        cookies={key:getattr(user,key) for key in keys}
        if not cookies.get('nick'):
            cookies['nick'] = user.phone[:3]+'****'+user.phone[7:]
        return cookies

    def _login(self,user_name,password):
        pass

    def passwd(self,passwd):
        return
class Users(Base):

    """
    用户信息
    """
    __tablename__ = 'users'
    STATUS={
        'normal':'正常',
        'inactive':'未激活',
        'delete':'删除',
        'reeze':'冻结'
    }

    uid = Column(String(128))
    belong_id = Column(Integer,nullable=True,default=0, doc='会员所属分销商id，与distributor_users表关联id')
    nick = Column(String(128))
    email = Column(String(128))
    phone = Column(String(256),default="")
    real_name = Column(String(128)) #用户真实名字
    user_name = Column(String(256))                         #用户名称。
    user_pwd = Column(String(256))                          #用户密码
    sex = Column(String(128),default=u"未知")                # 男 女 未知
    photo = Column(String(256),default="")                #用户头像
    is_bussiness = Column(Boolean,doc='是否大客户',default=False)
    weibo = Column(String(256),default="")
    weixin = Column(String(256),default="") #open_id
    taobao = Column(String(256),default="")
    qq = Column(String(256),default="")
    # role_type = Column(Integer,nullable=False,default=0,doc='用户角色类型：0普通会员 1分销商 2供应商 默认为普通会员')

    last_visit = Column(DateTime,default=now())                     #暴露
    last_visit_ip = Column(String(16),default='')
    visit_times = Column(Integer,default=0)                           #暴露 访问次数
    regist_from = Column(String(32),default='web')              # weibo qq ......
    coin = Column(Integer,default=0)                                         #(币)   like 积分之类的东西
    email_check_url = Column(String(256),default='')                   #邮件激活链接

    find_pw_url  = Column(String(256),default='')                    #找回密码url
    find_pw_expire_time = Column(DateTime,nullable=True)             #找回密码过期时间

    is_employee = Column(Boolean,default=False)             #方便操作 增加一个标识
    # role_codes = Column(String(128), nullable=True)              # 用户角色 code json字符串  冗余字段
    birthday = Column(DateTime,nullable=True)

    auto_repost = Column(Boolean,default=False)                 #是否受限制。可选值:limited(受限制),unlimited(不受限)
    promoted_type = Column(Boolean,default=False)               #有无实名认证。可选值:authentication(实名认证),not authentication(没有认证)
    status =  Column(String(16),default='inactive')             #状态。可选值:normal(正常),inactive(未激活),delete(删除),reeze(冻结)#,supervise(监管)
    reeze_time =  Column(DateTime,nullable=True)                #冻结时间

    avatar = Column(String(128),default='')
    vip_info =  Column(String(64),default='c')                             #用户的全站vip信息，可取值如下：c(普通会员),asso_vip(荣誉会员)，vip1,vip2,vip3,vip4,vip5,vip6(六个等级的正式vip会员)，共8种取值，其中asso_vip是由vip会员衰退而成，与主站上的vip0对应。
    sign_text = Column(String(256),default='')                         #个性签名
    province = Column(Integer)          #省
    city = Column(Integer)              #市
    area = Column(Integer)              #区
    detail_address = Column(String(256)) #街道详细地址
    address=Column(String(256))


    def __unicode__(self):
        return self.nick

    # @validates('email', include_removes=True)
    # def validate_email(self, key, email, is_remove):
    #     if is_remove:
    #         raise ValueError(
    #                 "not allowed to remove items from the collection")
    #     else:
    #         assert '@' in email
    #         return email

    def user_format(self,user):
        keys = ['id','belong_id','nick','phone','qq','regist_from','sex', 'sign_text','status','uid','user_name','visit_times', 'weibo', 'weixin','is_bussiness']
        cookies={key:getattr(user,key) for key in keys}
        if not cookies.get('nick'):
            cookies['nick'] = user.phone[:3]+'****'+user.phone[7:]
        return cookies

@event.listens_for(Users, 'before_update')
def receive_before_update(mapper, conn, target):
    target.gmt_modified = now()


class UserAddress(Base):
    __tablename__ = 'user_address'

    user_id = Column(Integer)

    name = Column(String(64),doc='名称',default='')
    card_type = Column(SmallInteger,doc='证件类型',default=1)  #1身份证
    card_num = Column(String(32),doc='身份证号',default='')
    phone = Column(String(31),doc='电话',default='')

    province = Column(String(32),doc='省份',default='')
    city = Column(String(32),doc='城市',default='')
    area = Column(String(32),doc='区域',default='')

    province_code = Column(String(32),doc='省份code',default='')#用悦华的国家城市代码
    city_code = Column(String(32),doc='城市code',default='')#用悦华的国家城市代码
    area_code = Column(String(32),doc='区域code',default='')#用悦华的国家城市代码

    address = Column(String(256),doc='详细地址',default='')
    zipcode = Column(String(10),doc='邮编',default='')
    is_default = Column(Boolean,doc='是否默认地址',default=False)
    is_check = Column(Boolean,doc='是否实名认证',default=False)
    card_img1 = Column(String(256),doc='身份证正面图像',default='')
    card_img2 = Column(String(256),doc='身份证反面图像',default='')

    def addressed(self):
        #return ''.join([self.province,self.city,self.area,self.address,'  '+self.name, '  手机:'+self.phone])#,self.name,self.phone)
        return ujson.dumps({'province':self.province,
         'city':self.city,
         'area':self.area,
         'province_code':self.province_code,
         'city_code':self.city_code,
         'area_code':self.area_code,
         'address':self.address,
         'zipcode':self.zipcode,
         'card_num':self.card_num,
         'user_name':self.name,
         'phone':self.phone,
         'receive_user_doc_id_front_url':self.card_img1,
         'receive_user_doc_id_back_url':self.card_img2
         })

class UserInfoCheck(Base):
    '''实名认证信息'''
    __tablename__ = 'user_info_check'

    address_id = Column(Integer,doc='地址ID')
    photo = Column(String(256),doc='身份证拍照')
    card_num = Column(String(256),doc='证件号')
    real_name = Column(String(32),doc='真实名称')

class UserStatusFlow(Base):
    """
        用户状体变化跟踪
    """
    __tablename__ = 'user_status_flow'

    status = Column(Integer)
    user_id = Column(Integer)                       #操作执行者


class UserIp(Base):

    __tablename__="user_ip"

    user_id = Column(Integer)               #用户
    ip = Column(Integer)                    #登录IP
    times = Column(Boolean)                 #次数

class UserVouchers(Base):

    __tablename__ = 'user_vouchers'

    amount = Column(Integer,doc='代金券金额')
    expired_time = Column(DateTime,doc='过期时间')
    used = Column(Boolean,doc='是否使用')
    use_amount = Column(Integer,doc='使用条件')#总金额大于多少才能使用

class UserView(Base):

    __tablename__ = 'user_views'

    user_id = Column(Integer,doc='用户')
    item_id = Column(Integer,doc='商品ID')

