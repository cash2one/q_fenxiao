#encoding:utf-8
__author__ = 'gaoaifei'

from tornado.web import url
from handlers import *

_handlers = [
    url(r'/member/order_(\d*).html',OrdersHandler,name='item_orders'),#取消订单 确认收货
    url(r'/member/addorder.html',OrdersHandler,name='orders_submit'),#提交订单
    url(r'/member/confirm_(\d*).html',DirectOrderHandle,name = 'direct_order'),#直接购买确认页面

    url(r'/member/addcart',ShoppingCartHandler,name='shopping_cart'),#添加购物车
    url(r'/member/cart.html',ShoppingCartCaculateHandler,name='shopping_cart_caculate'),#购物车列表及购物车结算页面
]