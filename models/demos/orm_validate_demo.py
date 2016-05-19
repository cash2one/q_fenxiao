#encoding:utf-8
__author__ = 'binpo'
from sqlalchemy.orm import validates
from models.base_do import Base
from sqlalchemy import Column, Integer, String

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
    nick = Column(String(128))
    email = Column(String(128))
    phone = Column(String(256),default="")
    real_name = Column(String(128)) #用户真实名字
    user_name = Column(String(256))                         #用户名称。
    user_pwd = Column(String(256))                          #用户密码
    sex = Column(String(128),default=u"未知")                # 男 女 未知
    photo = Column(String(256),default="")                #用户头像

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

    @validates('email', include_removes=True)
    def validate_email(self, key, email, is_remove):
        if is_remove:
            raise ValueError("not allowed to remove items from the collection")
        else:
            assert '@' in email
            return email

    def user_format(self):
        user_dic={}
        keys = ['email','id', 'is_employee','nick', 'phone', 'status','user_name','user_type', 'vip_info', 'weibo', 'weixin']
        for key in keys:
            user_dic[key] = eval('self.'+key)
        return user_dic
