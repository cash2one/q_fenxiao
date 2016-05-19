#encoding:utf-8
__author__ = 'jinkuan'

from common.base_handler import MobileBaseHandler,WebTenjinBase
from services.users.user_services import UserServices
from conf.sms_conf import LOGIN_CODE_TEMPLATE
from utils.random_utils import create_random_digit
from tornado.web import create_signed_value
from utils.message import send_msg
import ujson
import tornado
from utils.db_connection import DB
from tornado.options import options
import time
user_service = UserServices()

class RegHandlers(MobileBaseHandler):

    def get(self, *args, **kwargs):

        self.get_paras_dict()
        if not self.qdict:
            self.echo('mobile/reg.html',layout='')
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

            user_service.set_db(self.db)
            user = user_service.create_user_by_phone(phone,pwd)
            cookies = user_service.user_format(user)
            self.set_secure_cookie('loginuser',ujson.dumps(cookies),domain=self.cookie_domain,expires_days=10)
            self.write_json({'state':200,'info':'登录成功'})
        else:

            tel = str(self.get_argument('phone').strip())
            user_service.set_rdb(self.rdb)
            user = user_service.check_user_by_phone(tel)
            if not user:
                self.write_json({'state':400,'info':'该用户不存在'})
                return
            code = self.get_argument('code').strip()
            user_ip = self.get_client_ip
            key = str(user_ip+'_img_code')
            code_value = self.mcache.get(key)
            if code and code_value:
                if code.lower()==code_value.lower():
                    phone_code = create_random_digit(2)
                    self.mcache.set(tel,phone_code,180)
                    self.mcache.set(tel+'_send',int(time.time()),180)
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

class LoginHandler(WebTenjinBase):

    def get(self, *args, **kwargs):
        self.echo('mobile/login.html',layout='')

    def post(self, *args, **kwargs):
        self.get_paras_dict()
        next = self.qdict.get('next','/')
        content='{0},全球抢购欢迎你! <a class="login" id="loginout" href="javascript:void(0)">退出</a>'
        phone = self.qdict.get('usename')
        passwd = self.qdict.get('password')
        if not phone or not passwd:
            self.write_json({'state':400,'info':'输入参数错误'})
            return

        user_service = UserServices(rdb=DB(options.READ_ENGINE).get_session())
        # user_service.set_rdb(self.rdb)
        user = user_service.login_with_phone(phone,passwd)
        drp_user = user_service.login_with_drp_username(phone,passwd)
        if user:
            self.set_secure_cookie('fenxiao_loginuser',ujson.dumps(user.user_format(user)),expires_days=10)#(ujson.dumps(user.user_format(user)))
            content = content.format(user.nick)
            self.write_json({'state':200,'info':next,'header':content})
            return
        elif drp_user:
            self.set_secure_cookie('fenxiao_loginuser',ujson.dumps(drp_user.user_format(drp_user)),expires_days=10)
            content = content.format(drp_user.nick)
            self.write_json({'state':200,'info':next,'header':content})
            return
        else:
            self.write_json({'state':400,'info':'用户或者密码错误'})

class AjaxLoginHandler(WebTenjinBase):

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

class GetUserinfoHandler(MobileBaseHandler):
    def get(self, *args, **kwargs):
        '''
        获取当前用户信息
        :param args:
        :param kwargs:
        :return:
        '''
        user = self.get_current_user()
        if user:
            nick_name = user.get('nick')
            self.write_json({'state':200,'nick_name':nick_name})
        else:
            self.write_json({'state':400,'info':'no login'})

    def post(self, *args, **kwargs):
        pass

class LoginOutHandler(MobileBaseHandler):

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.clear_all_cookies()
        next = self.get_argument('next','/')
        self.redirect(next)

    def post(self, *args, **kwargs):
        pass


class FindBackPasswordHandler(MobileBaseHandler):
    def get(self, *args, **kwargs):
        self.echo('mobile/member/getpwd.html')