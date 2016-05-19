#encoding:utf-8
__author__ = 'gaoaifei'
from sqlalchemy import Integer, Column, String, DateTime, Boolean
from models.base_do import Base
from sqlalchemy.sql.functions import now

'''
优惠券类型：
1.满减        订单满组最低金额时候使用
2.立减        无条件使用
3.现金券      现金抵用
4.折扣        订单打折  打折券

领用和使用规则
1.规则： 
①购物券帐号绑定，一次购物只能使用一次购物券； 
②每个购物券只能使用一次，如果使用礼券的订单作废，购物券同时作废； 
③使用购物券不享受打折优惠； 
④在特价商品区不得使用优惠券（特殊商品会特殊说明）。  

投放说明： 
1.全站
2.特殊渠道
3.移动端
4.支付渠道 等等

投放规则

'''
class CouponType(Base):

    __tablename__ = 'coupon_type'
    #满减，立减，折扣，现金券
    code = Column(String(32),default='',doc='优惠类型')
    name = Column(String(32),default='',doc='优惠名称')#满减，立减，折扣，现金券
    description = Column(String(1024),doc='优惠券类型描述',default='')

    def __unicode__(self):
        return self.name

class CouponChannel(Base):
    '''
    推广渠道码  车猫，天猫等特定发放的渠道码
    '''
    __tablename__ = 'coupon_channel'
    code = Column(String(32),default='',doc='优惠券渠道')
    name = Column(String(32),default='',doc='优惠券渠道名称')
    description = Column(String(1024),doc='优惠券类型描述',default='')

    def __unicode__(self):
        return self.name


class Coupon(Base):
    """商品优惠券"""

    __tablename__ = 'coupon'
    uid = Column(String(128),doc='单次生成的唯一标示',default='')
    coupon_type_id = Column(Integer,doc='优惠券类型ID')
    name = Column(String(128),default='',doc='优惠券名称')
    code = Column(String(256),default='',doc='优惠券编码')
    description = Column(String(1024),doc='优惠券描述',default='')
    effective_time = Column(DateTime, default=now())    #生效时间
    expired_time = Column(DateTime, default=now())      #过期时间
    total_amount = Column(Integer, default=0,doc='面额')           #总金额
    coupon_channel_id = Column(Integer, default=0,nullable=True)           #渠道ID
    channel = Column(String(32),doc='渠道码',default='qqqg_mobile')        #
    #限制条件及提示
    member_grade = Column(Integer,default=0,doc='享受优惠的会员等级：0注册用户 1大客户 3非会员 4其他...')
    limit_category_id = Column(Integer,default='',doc='使用范围类别ID,category_id')
    is_claim = Column(Boolean, default=False,doc='是否领取')
    is_used = Column(Boolean,doc='是否已使用',default=False)
    limit_item = Column(Boolean,doc='是否限制商品',default=False)
    item_id = Column(Integer,default=0,nullable=True) #商品ID
    limit_min_amount = Column(Integer, default=0,doc='订单使用最小限额')        #最低金额，使用场景的金额大于最低金额才能使用
    is_online = Column(Boolean,default=1,doc='是否已经投入使用 0否 1是')

    # limit_effective_time = Column(Boolean,default=0) #是否限制‘生效时间’
    # limit_effective_time_msg = Column(String(512), default='该代金券尚未生效，敬请期待。')
    # limit_floor_amount = Column(Boolean,default=0) #是否限制‘最低金额’
    # limit_floor_amount_msg = Column(String(512), default='该代金券不能满足最低使用金额要求，无法使用，谢谢。')

class UserCoupon(Base):
    __tablename__ = 'user_coupon'

    user_id = Column(Integer,doc='用户')
    order_coupon_id = Column(Integer,doc='优惠券ID')
    is_used = Column(Boolean,doc='是否已使用',default=False)
    item_id = Column(Integer,default=0,nullable=True,doc='限制商品Id')
    limit_min_amount = Column(Integer, default=0,doc='订单使用最小限额')
    effective_time = Column(DateTime, default=now())    #生效时间
    expired_time = Column(DateTime, default=now())      #过期时间