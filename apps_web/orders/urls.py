#encoding:utf-8
__author__ = 'binpo'

from tornado.web import url
from handlers import *

_handlers = [
    url(r'/order/order_(\d*).html',OrdersHandler,name='item_orders'), #确认收货
    url(r'/order/order.html',OrdersHandler,name='orders_submit'),

    url(r'/order/cart.html',ShoppingCartHandler,name='shopping_cart'),#添加购物车
    url(r'/order/cart/caculate.html',ShoppingCartCaculateHandler,name='shopping_cart_caculate'),#订单提交页
    url(r'/order/dailybuy/check.html',UserDailyBuyCheck,name='shopping_order_check'),

]
