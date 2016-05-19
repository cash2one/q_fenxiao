#encoding:utf-8
__author__ = 'binpo'
from ..base_services import BaseService
from models.coupon_do import CouponChannel,CouponType,Coupon
import uuid

class CouponService(BaseService):

    def coupon_channel_list(self):
        return self.rdb.query(CouponChannel).filter(CouponChannel.deleted==0).order_by('gmt_modified desc')

    def coupon_type_list(self):
        return self.rdb.query(CouponType).filter(CouponType.deleted==0).order_by('gmt_modified desc')

    def coupon_list(self,**kargs):
        return self.rdb.query(Coupon).filter(Coupon.deleted==0).order_by('gmt_modified desc')

    def update_conpon_channel(self,name,code):
        pass
        # coupon_channel = self.db.query(CouponChannel).filter(CouponChannel.id==id).scalar()
        # if not coupon_channel:
        #     CouponChannel = CouponChannel()


    def query_coupon_by_id(self,id):
        '''
        根据ID查询单个优惠券
        :param id:
        :return:
        '''
        return self.rdb.query(Coupon).filter(Coupon.deleted==0,Coupon.id==id).scalar()

    def query_channel_by_id(self,id):
        return self.rdb.query(CouponChannel).filter(CouponChannel.deleted==0,CouponChannel.id==id).scalar()

    def query_coupon_type_by_id(self,id):
        return self.rdb.query(CouponType).filter(CouponType.deleted==0,CouponType.id==id).scalar()

    def edit_channel(self,name,code,description,id=None):
        '''
        编辑优惠卷渠道
        :param name:名称
        :param code:代码
        :param description:描述
        :param id:
        :return:
        '''
        if id:
            coupon_channel = self.db.query(CouponChannel).filter(CouponChannel.deleted==0,CouponChannel.id==id).scalar()
        else:
            coupon_channel = CouponChannel()
        coupon_channel.name = name
        coupon_channel.code = code
        coupon_channel.description = description
        self.db.add(coupon_channel)
        self.db.commit()

    def edit_coupon_type(self,name,code,description,id=None):
        '''
        编辑优惠卷渠道
        :param name:名称
        :param code:代码
        :param description:描述
        :param id:
        :return:
        '''
        if id:
            coupon_type = self.db.query(CouponType).filter(CouponType.deleted==0,CouponType.id==id).scalar()
        else:
            coupon_type = CouponType()
        coupon_type.name = name
        coupon_type.code = code
        coupon_type.description = description
        self.db.add(coupon_type)
        self.db.commit()

    def edit_coupon(self,**kwargs):
        if kwargs.get('id'):
            coupon = self.db.query(Coupon.id==kwargs.get('id')).scalar()
            coupon.coupon_type_id = kwargs.get('coupon_type_id')
            coupon.name = kwargs.get('name')
            coupon.code = kwargs.get('code')
            # coupon.description = kwargs.get('')
            coupon.effective_time = kwargs.get('effective_time')
            coupon.expired_time = kwargs.get('expired_time')
            coupon.total_amount = kwargs.get('total_amount')
            coupon.coupon_channel_id = kwargs.get('coupon_channel_id')
            coupon.channel = kwargs.get('channel')
            coupon.member_grade = kwargs.get('member_grade')
            coupon.limit_category_id = kwargs.get('limit_category_id')
            coupon.is_claim = kwargs.get('is_claim')
            coupon.is_used = kwargs.get('is_used')
            coupon.limit_item = kwargs.get('limit_item')
            coupon.item_id = kwargs.get('item_id')
            coupon.limit_min_amount = kwargs.get('limit_min_amount')
            self.db.add(coupon)
            self.db.commit()
        else:
            uid = str(uuid.uuid4())
            for x in xrange(int(kwargs.get('count'))):
                coupon = Coupon()
                coupon.uid = uid
                id,name = kwargs.get('coupon_type_id').split('__')
                coupon.coupon_type_id = id
                coupon.name = name
                coupon.code = str(uuid.uuid4())
                # coupon.description = kwargs.get('')
                coupon.effective_time = kwargs.get('effective_time')
                coupon.expired_time = kwargs.get('expired_time')
                coupon.total_amount = kwargs.get('total_amount')
                channel_id,channel_name = kwargs.get('coupon_channel_id').split('__')
                coupon.coupon_channel_id =channel_id
                coupon.channel = channel_name
                coupon.member_grade = kwargs.get('member_grade')
                coupon.limit_category_id = kwargs.get('category_id')
                # coupon.is_claim = kwargs.get('is_claim')
                # coupon.is_used = kwargs.get('is_used')
                # coupon.limit_item = kwargs.get('limit_item')
                coupon.item_id = kwargs.get('item_id')
                coupon.limit_min_amount = kwargs.get('limit_min_amount')
                self.db.add(coupon)
            self.db.commit()

