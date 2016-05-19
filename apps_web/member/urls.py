#ecoding:utf-8
__author__ = 'binpo'

from tornado.web import url
from ..member.handlers import  *

_handlers = [
    url(r'/member/index.html',MemberOrdersHandler,name='member'),
    url(r'/member/address_list.html',AddressHandler,name='address_list'),
    url(r'/member/address.html',MemberAddressHandler,name='member_address'),
    url(r'/member/collections.html',MemberCollectionHandler,name='member_collection'),#我的收藏品
    url(r'/member/([\w\W]*)/detail.html',MemberOrderDetailHandler,name='member_order_detail'),#订单详情 参数订单号
    url(r'/member/order/cancle/(\d*).html',OrderCancleHandler,name='member_order_cancle'),
    url(r'/member/order/express_check/(\d*).html',OrderExpressCheck,name='member_order_express_check'),
]