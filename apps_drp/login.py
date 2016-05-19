#encoding:utf-8
__author__ = 'binpo'
from tenjin_base import WebTenjinBase
from services.users.distributor_user_services import DistributorUserServices
from tornado.options import options
from utils.db_connection import DB
import ujson

class LoginHandler(WebTenjinBase):

    def get(self, *args, **kwargs):
        next = self.get_argument('next', '/drp/index.html')
        info=''
        self.echo('admin_drp/login.html',locals())

    def post(self, *args, **kwargs):

        user_name = self.get_argument('username')
        password = self.get_argument('password')
        if not user_name or not password:
            self.echo('admin_drp/login.html',{'info':'用户名和密码不能为空'})
        else:
            next = self.get_argument('next',None)# '/drp/index.html')
            drp_services = DistributorUserServices(rdb=DB(options.READ_ENGINE).get_session())
            user = drp_services._login(username = user_name,password = password)
            if user:
                cookies = user.to_dict()
                self.set_secure_cookie('login_distributor_user',ujson.dumps(cookies),expires_days=10)
                if user.role_type==0:
                    self.redirect('/drp/index.html')
                elif user.role_type==1:
                    self.redirect('/supply/index.html')
            else:
                self.echo('admin_drp/login.html',{'info':'用户名或密码不存在'},layout='')


class LoginOutHandler(WebTenjinBase):
    def get(self, *args, **kwargs):
        self.clear_all_cookies('login_distributor_user')
        self.redirect('/drp/login.html')