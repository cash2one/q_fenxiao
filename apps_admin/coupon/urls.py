#encoding:utf-8
__author__ = 'qiuyan'

from handlers import CouponHandler,CouponChannelHandler,CouponTypeHandler
from tornado.web import url

_handlers = [
    url(r'/admin/coupon/index.html',CouponHandler,name='coupon_handler'),
    url(r'/admin/coupon/channel/index.html',CouponChannelHandler,name='coupon_channel'),
    url(r'/admin/coupon/type/index.html',CouponTypeHandler,name='coupon_type')

]