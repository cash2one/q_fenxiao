#encoding:utf-8
__author__ = 'binpo'
from tenjin_base import WebTenjinBase
from services.users.admin_services import AdminServices
from tornado.options import options
from utils.db_connection import DB
import ujson

class LoginHandler(WebTenjinBase):

    def get(self, *args, **kwargs):
        next = self.get_argument('next', '/admin/')
        info=''
        self.echo('admin/login.html',locals())

    def post(self, *args, **kwargs):

        user_name = self.get_argument('username')
        password = self.get_argument('password')
        if not user_name or not password:
            self.echo('admin/login.html',{'info':'用户名和密码不能为空'})
        else:
            next = self.get_argument('next', '/admin/')
            admin_services = AdminServices(rdb=DB(options.READ_ENGINE).get_session())
            user = admin_services._login(username = user_name,password = password)
            if user:
                cookies = user.to_dict()
                self.set_secure_cookie('admin_login',ujson.dumps(cookies),expires_days=10)
                self.redirect(next)
            else:
                self.echo('admin/login.html',{'info':'用户名或密码不存在'})


class LoginOutHandler(WebTenjinBase):

    def get(self, *args, **kwargs):
        self.clear_all_cookies('admin_login')
        self.redirect('/admin/login')