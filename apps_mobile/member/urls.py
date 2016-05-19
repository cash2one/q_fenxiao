#ecoding:utf-8
__author__ = 'gaoaifei'

from tornado.web import url
from handlers import *

_handlers = [
    url(r'/order/orders.html',MemberOrdersHandler,name='member'),#我的订单

    url(r'/member/address_list.html',AddressHandler,name='address_list'),#我的收货地址列表接口
    url(r'/member/address.html',MemberAddressHandler,name='member_address'),#新增／编辑地址 删除地址 设置默认地址

    url(r'/member/collections.html',MemberCollectionHandler,name='member_collection'),#我的收藏 暂时无

    url(r'/order/([\w\W]*)/detail.html',MemberOrderDetailHandler,name='member_order_detail'),#订单详情
    url(r'/order/cancle/(\d*).html',OrderCancleHandler,name='member_order_cancle'),#取消订单
    url(r'/order/express_check/(\d*).html',OrderExpressCheck,name='member_order_express_check'),#查看物流
]

_app_handlers = [
    url(r'/app/order/([\w\W]*)/detail.html',MemberOrderDetailHandler,name='app_Android_member_order_detail'),#订单详情
    url(r'/app/memmber/me.html',AppMeHandler,name='app_Android_me'),
    url(r'/app/order/express_check/(\d*).html',OrderExpressCheck,name='app_Android_member_order_express_check'),#查看物流
]

_handlers.extend(_app_handlers)
