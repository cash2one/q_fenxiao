#encoding:utf-8
__author__ = 'binpo'

from common.base_handler import BaseHandler
from utils.message import send_msg
from conf.sms_conf import LOGIN_CODE_TEMPLATE
from utils.random_utils import create_random_digit
from services.users.user_services import UserServices
import time
import ujson
import tornado
import datetime
# mclient = MemcacheManager.get_sigle_conn()

class RegHandlers(BaseHandler):

    def get(self, *args, **kwargs):

        self.get_paras_dict()
        if not self.qdict:
            self.echo('reg.html',layout='')
        else:
            phone_code = self.qdict.get('phonecode').strip()
            phone = self.qdict.get('phone').strip()
            if phone_code and phone_code:
                code_value = self.mcache.get(phone)
                if code_value == phone_code:
                    self.write_json({'state':200,'info':'验证成功'})
                else:
                    self.write_json({'state':400,'info':'短信验证码错误'})

    def post(self, *args, **kwargs):

        if self.get_argument('option',None):
            self.get_paras_dict()
            keys = ['phone','pwd','smskey']
            for key in keys:
                if not self.qdict.has_key(key) or not self.qdict.has_key(key) :
                    return self.write_json({'state':400,'info':'参数不全'})
            phone = self.qdict.get('phone').strip()
            pwd = self.qdict.get('pwd').strip()
            mgs_key = self.qdict.get('smskey').strip()
            validate,info = self.check_phone_code(phone,mgs_key)
            if not validate:
                return self.write_json({'state':400,'info':'请求超时'})
            user_service = UserServices()
            user_service.set_db(self.db)
            user = user_service.create_user_by_phone(phone,pwd)
            cookies = user_service.user_format(user)
            self.set_secure_cookie('loginuser',ujson.dumps(cookies),domain=self.cookie_domain,expires_days=10)
            self.write_json({'state':200,'info':'登录成功'})
        else:
            tel = self.get_argument('phone').strip()
            code = self.get_argument('code').strip()
            user_ip = self.get_client_ip
            key = str(user_ip+'_img_code')
            code_value = self.mcache.get(key)
            if code and code_value:
                if code.lower()==code_value.lower():
                    phone_code = create_random_digit(2)
                    self.mcache.set(str(tel),phone_code,180)
                    self.mcache.set(str(tel+'_send'),int(time.time()),180)
                    content = LOGIN_CODE_TEMPLATE.format(phone_code)
                    send_msg(tel,content)
                    data="<p>我们已经发送一条验证短信至 <span class='address-place'>"+tel+"</span></p><p>请输入短信中的验证码</p>"
                    self.write_json({'state':200,'info':data})
                else:
                    self.write_json({'state':400,'info':'验证码不正确'})
            else:
                if not code_value:
                    self.write_json({'state':400,'info':'验证码已过期'})
                elif not code:
                    self.write_json({'state':400,'info':'验证码不能为空'})

    def put(self, *args, **kwargs):
        phone = self.get_argument('phone_code')
        self.write_json({'state':200,'info':'登录成功'})


class LoginHandler(BaseHandler):

    def get(self, *args, **kwargs):
        if self.get_current_user():
            self.redirect(self.get_argument('next','/'))
        else:self.echo('login.html',layout='')

    def post(self, *args, **kwargs):
        self.get_paras_dict()
        login_type = self.qdict.get('login_type')
        next = self.qdict.get('next','/')
        content='{0},全球抢购欢迎你! <a class="login" id="loginout" href="javascript:void(0)">退出</a>'
        if login_type=='phone':
            phone = self.qdict.get('phone').strip()
            code = self.qdict.get('code').strip()
            if not phone or not code:
                return self.write_json({'state':400,'info':'输入参数错误'})
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
                self.set_secure_cookie('loginuser',ujson.dumps(cookies),domain=self.cookie_domain,expires_days=10)#(ujson.dumps(user.user_format(user)))
                content = content.format(cookies.get('nick'))
                self.write_json({'state':200,'info':next,'header':content})
            else:
                self.write_json({'state':400,'info':info})
        elif login_type=='usename':
            phone = self.qdict.get('usename')
            passwd = self.qdict.get('password')
            if not phone or not  passwd:
                return self.write_json({'state':400,'info':'输入参数错误'})
            user_service = UserServices()
            user_service.set_rdb(self.rdb)
            user = user_service.login_with_phone(phone,passwd)
            if user:
                self.set_secure_cookie('loginuser',ujson.dumps(user.user_format(user)),domain=self.cookie_domain,expires_days=10)#(ujson.dumps(user.user_format(user)))
                content = content.format(user.nick)
                self.write_json({'state':200,'info':next,'header':content})
            else:
                self.write_json({'state':400,'info':'用户或者密码错误'})


class AjaxLoginHandler(BaseHandler):

    def get(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        self.get_paras_dict()
        user_name = self.qdict.get('user_name').strip()
        password = self.qdict.get('password').strip()
        _code = self.qdict.get('validate_code').strip()
        is_validate,info = self.check_validate_code(_code)
        if not is_validate:
            self.write_json({'state':400,'info':info})
        else:
            pass


class LoginOutHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        # expires = datetime.datetime.utcnow() - datetime.timedelta(days=365)
        # self.set_secure_cookie("loginuser",'',domain=self.cookie_domain,expires=expires)
        self.clear_all_cookies()
        next = self.get_argument('next','/')
        self.redirect(next)

    def post(self, *args, **kwargs):
        pass


class FindBackPasswordHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.echo('getpwd/getpwd.html',layout='')

class CheckLoginHander(BaseHandler):
    '''
    判断用户是否登录
    '''
    def get(self, *args, **kwargs):
        loginuser = self.get_cookie('loginuser')
        if not loginuser:
            self.write_json({'state':200,'info':'no login','is_login':0})
        else:
            self.write_json({'state':200,'info':'no login','is_login':1})



