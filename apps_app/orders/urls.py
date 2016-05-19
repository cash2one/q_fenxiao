#encoding:utf-8
__author__ = 'jinkuan'

from tornado.web import url
from apps_app.orders.handlers import *

_handlers = [
    url(r'/api/json/add/order',AppCreateOrderHandler,name='app_create_order'),#生成订单
    url(r'/api/json/shopping/cart',AppShoppingCartHandler,name='app_shopping_cart'),#购物车列表及购物车结算页面
    url(r'/api/json/cart/calculate',ShoppingCartCalculateHandler,name='app_shopping_cart_calculate'),#购物车列表及购物车结算页面
    url(r'/api/json/orders',AppOrdersHandler,name='app_orders'),
    url(r'/api/json/default/address',AppDefaultAddressHandler,name = 'app_default_address'),#直接购买确认页面

]
