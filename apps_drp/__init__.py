#encoding:utf-8
__author__ = 'binpo'

from tornado.web import url
from apps_drp.login import *
from login import *
from base_handler import DrpHomeHandler

handlers = [
    url(r'/drp/index.html', DrpHomeHandler,name='index_html'),
    url(r'/drp/login.html', LoginHandler,name='drp_login'),
    url(r'/drp/logout', LoginOutHandler,name='drp_login_out'),
]

from shop import *
handlers.append(url(r'/drp/shop.html', Shophandler,name='drp_shop_page'))
handlers.append(url(r'/drp/qrcode.html',Qrcodehandler,name='drp_shop_qrcode'))
handlers.append(url(r'/drp/item_detail.html', ItemDetailHandler,name='drp_item_qrcode'))



from orders.urls import _handlers
handlers.extend(_handlers)

from items.urls import _handlers
handlers.extend(_handlers)

from users.urls import _handlers
handlers.extend(_handlers)

from express.urls import _handlers
handlers.extend(_handlers)