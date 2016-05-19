# -*- coding: utf-8 -*-
'''
Created on 2013-12-30

@author: qiuyan.zwp
'''
import sso
from common.base import BaseHandler
from tornado import gen
import json
import logging
import tornado.web
import urllib
import urlparse
from services.users.user_services import *
import ujson
from tornado.options import options
import datetime
login_allow_count = 4
from datacache.datacache import PageDataCache
from utils.message.action_message import send_action_msg
from common.mweixin_oauth.m_weixin_handler import get_oauth_user_info
from common.mweixin_oauth.wx_mobile_info import get_wx_login_redirect_url,get_wx_user_info,get_wx_login_redirect_url_with_none_access
from setting import WX_ZMZ_AppID,WX_ZMZ_AppSecret
data_catch = PageDataCache()
from utils.md5_util import create_md5
class LoginPageHandler(BaseHandler):


    def get(self,**kargs):

        next = self.get_argument('next', '/')
        info = self.get_argument('info', '')
        self.get_paras_dict()
        change_user = True  if self.get_argument('change_user', '') else False
        if 'admin' in next:
            return self.redirect('/admin/login?next='+next)
        if self.current_user and self.current_user.get('id') and not change_user:
            return self.redirect(urlparse.urljoin(self.request.full_url(), next))
        count = self.mcache.get(self.get_client_ip+'_login_page_count')
        #self.headers['User-Agent']
        #----------------------微信绑定-----------------------
        if self.get_argument('type','') == 'm':
            self.set_secure_cookie('login_redirect_url',next,domain=self.cookie_domain,expires_days=1)
            try:
                self.get_paras_dict()
                if not self.qdict.has_key('code'):
                    raise
                    #self.echo('cards/index.html')
                else:
                    #raise
                    code = self.qdict.get('code') #self.get_argument('code',None)
                    code = code.strip()
                    #print 'code:',code
                    content = urllib.urlopen('https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code'%(WX_ZMZ_AppID,WX_ZMZ_AppSecret,code)).read()
                                           #('https://api.weixin.qq.com/sns/oauth2/access_token?appid=APPID&secret=SECRET&code=CODE&grant_type=authorization_code')
                    token_info = ujson.loads(content)
                    openid = token_info.get('openid')
                    access_token = token_info.get('access_token')
                    user_info = urllib.urlopen('https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s'%(access_token,openid)).read()
                    user = ujson.loads(user_info)
                    nick=user.get('nickname')
                    photo=user.get('headimgurl')
                    #                           #'https://api.weixin.qq.com/sns/userinfo?access_token=ACCESS_TOKEN&openid=OPENID&lang=zh_CN

                    #user = ujson.loads(user_info)
                    #user_service = UserServices(self.db)
                    #exist_user = user_service.get_user_by_weixin(openid)
                    #print ':',openid
                    #new_user = user_service.create_user_by_weixin(user=exist_user,nick=user.get('nickname'),photo=user.get('headimgurl'),weixin=openid,sex=user.get('sex'))
                    self.set_secure_cookie('wx_login_open_id',openid,domain=self.cookie_domain,expires_days=1)
                    self.set_secure_cookie('nick',nick,domain=self.cookie_domain,expires_days=1)
                    self.set_secure_cookie('photo',photo,domain=self.cookie_domain,expires_days=1)

                    #cookies = user_service.user_format(new_user)
                    #self.set_secure_cookie('loginuser',ujson.dumps(cookies),domain=self.cookie_domain,expires_days=1)
                    # self.echo('cards/index.html')
                    self.echo('web/weixin/login/login.html' if self.get_argument('type', '') and self.get_argument('type') == 'm' else 'view/login/login_page.html', {
                    'next':next,
                    'img_check': True if count >= login_allow_count else '',
                    'change_user': change_user
                    }, layout='')
                    return
            except Exception,e:
                # if change_user:
                #     _url='http://m.zenmez.com/login/page?type=m&change_user=change_user'
                # else:
                params = urllib.urlencode(self.qdict)
                _url='http://m.zenmez.com/login/page?'+params
                #direct_url = get_wx_login_redirect_url_with_none_access(_url)
                direct_url = get_wx_login_redirect_url(_url)
                self.redirect(direct_url)
        else:
            #----------------------微信绑定-----------------------
            self.echo('web/weixin/login/login.html' if self.get_argument('type', '') and self.get_argument('type') == 'm' else 'view/login/login_page.html', {
            'next': next,
            'img_check': True if count >= login_allow_count else '',
            'change_user': change_user
            }, layout='')

    def post(self):
        login_count = self.mcache.get(self.get_client_ip+'_login_page_count')
        user_agent = self.request.headers.get('User-Agent')
        print user_agent
        rsp = {
            'stat': 'err',
            'msg': '',
            'img_check': 'ok' if login_count and login_count >= login_allow_count else 'err',
        }
        username = self.get_argument('username','')           # 用户名
        passwd = self.get_argument('passwd','')                # 密码
        if not username or not passwd:
            rsp['msg'] = '账号和密码不能为空'
            return self.write(ujson.dumps(rsp))
        if login_count > login_allow_count:
            code = self.mcache.get(self.get_client_ip+'_login_page')
            if not code:
                rsp['msg'] = '验证码已过期'
                return self.write(ujson.dumps(rsp))
            if code.lower() != self.get_argument('img_check_code', '').lower():
                rsp['msg'] = '验证码不正确'
                return self.write(ujson.dumps(rsp))
        # m_key = self.get_client_ip+'_login_count'
        # self.mcache.set(m_key, self.mcache.get(m_key)+1 if self.mcache.get(m_key) else 1, 120)
        user_service = UserServices(self.db)
        status, user = user_service.check_user_login_pwd(username,passwd)
        if status:
            user.last_visit = datetime.datetime.now()
            user.last_visit_ip = self.get_client_ip
            user.visit_times = user.visit_times+1
            wx_open_id = self.get_secure_cookie('wx_login_open_id',None)
            if wx_open_id:
                user.weixin = wx_open_id
            if self.get_secure_cookie('nick'):
                if user.nick=='' or user.nick.startswith('user'):
                    user.nick = self.get_secure_cookie('nick')
            if self.get_secure_cookie('photo'):
                if user.photo=='http://img.zenmez.com/common/user_photo.png':
                    user.photo = self.get_secure_cookie('photo')
            cookies = user_service.user_format(user)
            self.set_secure_cookie('loginuser', ujson.dumps(cookies),domain=self.cookie_domain,expires_days=1000, httponly=True)
            self.set_cookie('check_loginuser', create_md5(create_md5(ujson.dumps(cookies))),domain=self.cookie_domain,expires_days=1000)

            self.db.add(user)
            self.db.commit()
            rsp['stat'] = 'ok'
            return self.write(ujson.dumps(rsp))
        else:
            rsp['msg'] = user
            m_key = self.get_client_ip+'_login_page_count'
            self.mcache.set(m_key, self.mcache.get(m_key)+1 if self.mcache.get(m_key) else 1, 120)
            return self.write(ujson.dumps(rsp))

class MobileLoginHandler(BaseHandler):
    def get(self, *args, **kwargs):
        pass

class LoginCheckHandler(BaseHandler):
    def get(self, *args, **kwargs):
        return self.write_json({
            'stat': 'ok' if self.current_user else 'err'
        })

class LoginHandler(BaseHandler):


    def get(self,**kargs):
        # next = self.get_argument('next', '/')
        # if 'admin' in next:
        #     return self.redirect('admin/login?next='+next)
        # if self.current_user and self.current_user.get('id'):
        #     return self.redirect(urlparse.urljoin(self.request.full_url(), '/'))
        # count = self.mcache.get(self.get_client_ip+'_login_count')
        # self.echo('web/login.html', {
        #     'next': next,
        #     'img_check': True if count > 3 else False
        # })
        count = self.mcache.get(self.get_client_ip+'_login_count')
        rsp = {
            'stat': 'ok' if count and count >= login_allow_count else 'err',
            'src': options.img_check_url+'login?987654321',
            'is_login': 'ok' if self.current_user and self.current_user.get('id') else 'err'
        }
        return self.write(ujson.dumps(rsp))
    
    def post(self):
        user_service = UserServices(self.db)
        self.get_paras_dict()
        login_count = self.mcache.get(self.get_client_ip+'_login_count')
        rsp = {
            'stat': 'err',
            'msg': '',
            'img_check': 'ok' if login_count and login_count >= login_allow_count else 'err',
            'src': options.img_check_url+'login?987654321'
        }

        if login_count > login_allow_count:
                code = self.mcache.get(self.get_client_ip+'_login')
                if not code:
                    rsp['msg'] = '验证码已过期'
                    return self.write(ujson.dumps(rsp))
                if code.lower() != self.get_argument('img_check_code', '').lower():
                    rsp['msg'] = '验证码不正确'
                    return self.write(ujson.dumps(rsp))

        if self.qdict.get('dyn_pwd'): #手机动态登录
            stat, info = self.check_dynamic_pwd()
            if not stat:
                rsp['msg'] = info
                return self.write(ujson.dumps(rsp))

            status,user = True, user_service.get_user_by_phone(self.qdict['phone'])
            if not user:
                rsp['msg'] = '用户不存在'
                return self.write(ujson.dumps(rsp))

        else:#普通登录
            username = self.get_argument('username','')           # 用户名
            passwd = self.get_argument('passwd','')                # 密码
            if not username or not passwd:
                rsp['msg'] = '账号和密码不能为空'
                return self.write(ujson.dumps(rsp))

            status, user = user_service.check_user_login_pwd(username,passwd)
        if status:
            user.last_visit = datetime.datetime.now()
            user.last_visit_ip = self.get_client_ip
            user.visit_times = user.visit_times+1
            cookies = user_service.user_format(user)
            # self.set_cookie('loginuser', ujson.dumps(cookies), expires_days=999 if self.get_argument('login_forever', '') else None, httponly=True, secure=True)
            # print 999 if int(self.get_argument('login_forever', '')) else None
            # print '11111'
            # print self.get_argument('login_forever', '')
            self.set_secure_cookie('loginuser', ujson.dumps(cookies),domain=self.cookie_domain,expires_days=100 if int(self.get_argument('login_forever', 0)) else 0.1, httponly=True )
            self.set_cookie('check_loginuser', create_md5(create_md5(ujson.dumps(cookies))),domain=self.cookie_domain,expires_days=1000)

            data_catch.set_db(self.db)
            user_cache_key='user_'+str(user.id)
            data_catch.cache_user_info(user_cache_key,cookies)

            self.db.add(user)
            self.db.commit()
            rsp['stat'] = 'ok'
            return self.write(ujson.dumps(rsp))
        else:
            rsp['msg'] = user
            m_key = self.get_client_ip+'_login_count'
            self.mcache.set(m_key, self.mcache.get(m_key)+1 if self.mcache.get(m_key) else 1, 120)
            return self.write(ujson.dumps(rsp))

    def check_dynamic_pwd(self):
        passwd = self.qdict.get('dyn_pwd','').strip()                # 密码
        key = str(self.qdict.get('phone')+'_dyn_login')
        code = self.mcache.get(key)
        if code:
            if code == passwd:
                return True, ''
            else:
                return False, '短信验证码错误'
        else:
            return False, '短信验证码已过期'



class AdminLoginHandler(BaseHandler):

    @property
    def db(self):
        return self.application.db

    def get(self,**kargs):
        back_url = urlparse.urljoin(self.request.full_url(), self.get_argument('next', '/admin/index'))
        if self.get_secure_cookie('loginuser'):
            self.redirect(back_url)

        self.echo('ops/login.html',layout='')


    def post(self):

        username = self.get_argument('username',None)           # 用户名
        passwd = self.get_argument('passwd',None)                # 密码
        user_service = UserServices(self.db)
        user = user_service.check_user_passwd(username,passwd)
        back_url = urlparse.urljoin(self.request.full_url(), self.get_argument('next', '/admin/index'))
        if user:
            cookies  = user_service.user_format(user)
            self.set_secure_cookie('loginuser',ujson.dumps(cookies),domain=self.cookie_domain,expires_days=1 )
            self.set_cookie('check_loginuser', create_md5(create_md5(ujson.dumps(cookies))),expires_days=1000)
            user.last_visit = datetime.datetime.now()
            user.last_visit_ip = ''
            user.visit_times = user.visit_times+1
            try:
                send_action_msg(method='post',action='admin/login',data='',user_id=user.get('id'),nick=user.get('nick'),action_name='登陆系统')
            except Exception,e:
                pass

            self.db.add(user)
            self.db.commit()
            self.redirect(back_url)
        else:
            self.echo('ops/login.html',next=next,info=u'用户名或密码错误')

class LogoutHandler(BaseHandler):

    def get(self):
        self.clear_cookie("loginuser", domain=self.cookie_domain)
        #self.clear_all_cookies("loginuser")
        if self.get_secure_cookie("check_loginuser"):
            self.clear_cookie("check_loginuser", domain=self.cookie_domain)
        #self.clear_all_cookies("check_loginuser")

        next = self.get_argument('next','/')
        if 'admin' in next:
            self.echo('admin/login.html',next=next)
        #print 'self.get_secure_cookie(loginuser)',self.get_secure_cookie('loginuser')
        self.set_secure_cookie('loginuser','',domain=self.cookie_domain)
        if not self.get_secure_cookie('loginuser'):
            print self.get_secure_cookie('loginuser')
            self.redirect('/')
        else:
            print '/t/loginout/',''
            self.redirect("/t/loginout/")

class TornadoLogoutHandler(tornado.web.RequestHandler):

    def get(self):
        if self.get_secure_cookie('loginuser',None):
            self.clear_cookie("loginuser")
            #self.clear_all_cookies("loginuser")
        next = self.get_argument('next','/')
        if 'admin' in next:
            self.echo('admin/login.html',next=next)
        self.redirect("/")

class AuthHandler(BaseHandler,sso.AuthHandler):
   
    LOGIN_URL = '/login'
#    def authenticate_redirect(self, app_name, next, callback=None):
#        self.redirect(self.LOGIN_URL + '?' + urllib.urlencode(args))
        
    @tornado.web.asynchronous
    @gen.coroutine
    def get(self):
        if self.get_secure_cookie('loginuser'):
            self.redirect(next)
        else:
            back_url = urlparse.urljoin(self.request.full_url(), self.get_argument('next', '/'))
            self.redirect(self.LOGIN_URL + '?next='+back_url)
            #self.authenticate_redirect(app_name=self.APP_NAME,next=back_url)  
    
    def post(self):
        pass
    

