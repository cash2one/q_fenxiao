#encoing:utf-8

from common.base_handler import BaseHandler,MobileBaseHandler
import tornado.web
from tornado.options import options

class UserCenterHandler(BaseHandler):

    @tornado.web.authenticated
    def prepare(self):
        self.cart_count = self.get_cart_count()
        self.STATIC_DOMAIN = options.STATIC_FILE_DOMAIN

class MobileUserCenterHandler(MobileBaseHandler):

    @tornado.web.authenticated
    def prepare(self):
        self.cart_count = self.get_cart_count()
        self.STATIC_DOMAIN = options.STATIC_FILE_DOMAIN
