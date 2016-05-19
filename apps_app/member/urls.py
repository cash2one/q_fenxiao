#ecoding:utf-8
__author__ = 'gaoaifei'

from tornado.web import url
from apps_app.member.handlers import *

_handlers = [
    url(r'/api/json/member/center',AppMemberCenterHandler,name='app_member_center'), #app个人中心
    url(r'/api/json/member/orders',AppMemberOrdersHandler,name='app_member_orders'),#app订单
    url(r'/api/json/member/address',AppMemberAddressHandler,name='app_member_address'),#app收货地址列表

    url(r'/h5/order/express_check/(\d*).html',AppOrderExpressCheck,name='app_member_order_express_check'),#查看物流
]
