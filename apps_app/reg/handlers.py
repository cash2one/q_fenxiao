#encoding:utf-8
__author__ = 'gaoaifei'

from common.base_handler import AppBaseHandler
from services.users.user_services import UserServices
from utils.random_utils import create_random_digit
from tornado.web import create_signed_value
import ujson
import datetime
# mclient = MemcacheManager.get_sigle_conn()

class AppRegHandler(AppBaseHandler):

    def post(self, *args, **kwargs):
        self.get_paras_dict()
        keys = ['phone','pwd','smskey']
        for key in keys:
            if not self.qdict.has_key(key) or not self.qdict.has_key(key):
                return self.write_json({'stat':201,'info':'参数不全'})
        phone = self.qdict.get('phone').strip()
        pwd = self.qdict.get('pwd').strip()
        mgs_key = self.qdict.get('smskey').strip()
        validate,info = self.check_phone_code(phone,mgs_key)
        if not validate:
            return self.write_json({'stat':201,'info':'请求超时'})
        user_service = UserServices()
        user_service.set_db(self.db)
        user = user_service.create_user_by_phone(phone,pwd)
        self.set_secure_cookie('loginuser',ujson.dumps(user.user_format(user)),expires_days=10)
        login_token = create_signed_value(self.application.settings["cookie_secret"],'loginuser',ujson.dumps(user.user_format(user)))
        self.write_json({'stat':200,'data':login_token,'is_bussiness':user.is_bussiness and 1 or 0,'info':'登录成功'})

class AppLoginHandler(AppBaseHandler):
    def post(self, *args, **kwargs):
        self.get_paras_dict()
        login_type = self.qdict.get('login_type')
        if login_type=='phone':
            phone = self.qdict.get('usename').strip()
            code = self.qdict.get('smskey').strip()
            if not phone or not code:
                return self.write_json({'stat':201,'info':'输入参数错误'})
            is_validate,info = self.check_phone_code(phone,code)
            if is_validate:
                user_service = UserServices()
                user_service.set_rdb(self.rdb)
                user = user_service.get_user_by_phone(phone)
                if not user:
                    user_service.set_db(self.db)
                    user = user_service.create_user_by_phone(phone,create_random_digit(3))
                user.last_visit = datetime.datetime.now()
                user.last_visit_ip = self.get_client_ip
                cookies = user.user_format(user)
                self.db.add(user)
                self.db.commit()
                self.set_secure_cookie('loginuser',ujson.dumps(user.user_format(user)),expires_days=10)
                login_token = create_signed_value(self.application.settings["cookie_secret"],'loginuser',ujson.dumps(cookies))
                self.write_json({'stat':200,'data':login_token,'is_bussiness':user.is_bussiness and 1 or 0,'info':''})
            else:
                self.write_json({'stat':201,'info':info})
        elif login_type=='usename':
            phone = self.qdict.get('usename')
            passwd = self.qdict.get('password')
            if not phone or not passwd:
                return self.write_json({'stat':201,'info':'输入参数错误'})
            user_service = UserServices()
            user_service.set_rdb(self.rdb)
            user = user_service.login_with_phone(phone,passwd)
            if user:
                self.set_secure_cookie('loginuser',ujson.dumps(user.user_format(user)),expires_days=10)
                login_token = create_signed_value(self.application.settings["cookie_secret"],'loginuser',ujson.dumps(user.user_format(user)))
                self.write_json({'stat':200,'data':login_token,'is_bussiness':user.is_bussiness and 1 or 0,'info':''})
            else:
                self.write_json({'stat':201,'info':'用户或者密码错误'})