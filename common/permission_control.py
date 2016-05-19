#encoding:utf-8
__author__ = 'binpo'

import functools
from urllib import urlencode
import urlparse
from tornado.log import gen_log as log
import tornado
import ujson
from models.user_do import *

def admin_permission_control(role_code):
    """
    check user's rule
    :param role_code  like 'admin,shigong,' 多个用都好隔开
    """
    def control(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            user = self.get_current_user()#ujson.loads(self.current_user)
            # if not user:
            #     log.error('user are not login')
            #     if self.request.method in ("GET", "HEAD"):
            #         url = self.get_login_url()
            #         if "?" not in url:
            #             if urlparse.urlsplit(url).scheme:
            #                 next_url = self.request.full_url()
            #             else:
            #                 next_url = self.request.uri
            #             url += "?" + urlencode(dict(next=next_url))
            #         self.redirect(url)
            #         return
            #     raise tornado.web.HTTPError(403)
            # else:
            x = [ r for r in role_code.split(',') if r in user.get('role_codes', '')]
            if x:
                return method(self, *args, **kwargs)
            else:
                self.redirect('/404')
        return wrapper
    return control

def weixin_authenticated(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            user = self.get_current_user()#ujson.loads(self.current_user)
            if not user:
                log.error('user are not login')
                if self.request.method in ("GET", "HEAD"):
                    url = self.get_login_url()
                    if "?" not in url:
                        if urlparse.urlsplit(url).scheme:
                            next_url = self.request.full_url()
                        else:
                            next_url = self.request.uri
                        url += "?" + urlencode(dict(next=next_url,type='m'))
                    self.redirect(url)
                    return
                raise tornado.web.HTTPError(403)
            return method(self, *args, **kwargs)
        return wrapper

def weixin_not_allowed_to_enter(code):
    """
    禁止某些角色权限进入
    :param role_code  like 'admin,shigong,' 多个用都好隔开
    """
    def control(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            user = self.get_current_user()#ujson.loads(self.current_user)
            if user:
                codes = [ x for x in code.split(',') if x in user['role_codes']]
                if codes:
                    return self.redirect('/weixin/merchant/detail/%s' % user['id'])
            return method(self, *args, **kwargs)
        return wrapper
    return control

def login_control():
    """
    登录控制
    :param
    """
    def control(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            user = self.get_current_user()
            if user:
                return method(self, *args, **kwargs)
            else:
                return self.write(ujson.dumps({'stat':'1002','data':{},'info':'You haven\'t log on the system!'}))
        return wrapper
    return control

def mobile_login_control(method):
    """
    app登录控制
    :param
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        user = self.get_current_user()
        if user:
            return method(self, *args, **kwargs)
        else:
            return self.write(ujson.dumps({'stat':403,'data':'','info':'没有登录'}))
    return wrapper

from tornado.web import HTTPError
def authenticated(method):
    """Decorate methods with this to require that the user be logged in.

    If the user is not logged in, they will be redirected to the configured
    `login url <RequestHandler.get_login_url>`.

    If you configure a login url with a query parameter, Tornado will
    assume you know what you're doing and use it as-is.  If not, it
    will add a `next` parameter so the login page knows where to send
    you once you're logged in.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            if self.request.method in ("GET","HEAD","POST","PUT","DELETE"):
                url = self.get_login_url()
                if "?" not in url:
                    if urlparse.urlsplit(url).scheme:
                        # if login url is absolute, make next absolute too
                        next_url = self.request.full_url()
                    else:
                        next_url = self.request.uri
                    url += "?" + urlencode(dict(next=next_url))
                self.redirect(url)
                return
            raise HTTPError(403)
        return method(self, *args, **kwargs)
    return wrapper

def distributor_user_authenticated(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            if self.request.method in ("GET","HEAD","POST","PUT","DELETE"):
                url = '/drp/login.html'
                if "?" not in url:
                    if urlparse.urlsplit(url).scheme:
                        next_url = self.request.full_url()
                    else:
                        next_url = self.request.uri
                    url += "?" + urlencode(dict(next=next_url))
                self.redirect(url)
                return
            raise HTTPError(403)
        return method(self, *args, **kwargs)
    return wrapper



#    role_type = Column(Integer,nullable=False,default=0,doc='用户角色类型 0分销商 1供应商 默认为分销商')

def drp_user_authenticated(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        user = self.get_current_user()
        if user.get('role_type') in ('0',0):
            return method(self, *args, **kwargs)
        else:
            self.write('<html><center><h1>权限不足</h1></center></html>')
            self.finish()
    return wrapper

def supply_user_authenticated(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        user = self.get_current_user()
        if user.get('role_type') in ('1',1):
            return method(self, *args, **kwargs)
        else:
            self.write('<html><center><h1>权限不足</h1></center></html>')
            self.finish()

    return wrapper

def mobile_user_authenticated(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            if self.request.method in ("GET","HEAD","POST","PUT","DELETE"):
                url = '/login.html'
                if "?" not in url:
                    if urlparse.urlsplit(url).scheme:
                        next_url = self.request.full_url()
                    else:
                        next_url = self.request.uri
                    url += "?" + urlencode(dict(next=next_url))
                self.redirect(url)
                return
            raise HTTPError(403)
        return method(self, *args, **kwargs)
    return wrapper

def mobile_role_authenticated(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        user = self.get_current_user()
        if (user.has_key('role_type') and user.get('role_type') in ('0',0)) \
                or (user.has_key('belong_id') and
                        self.rdb.query(DistributorUser).filter(DistributorUser.deleted == 0,
                                                               DistributorUser.id == user.get('belong_id')).scalar()):
            return method(self, *args, **kwargs)
        else:
            self.write('<html><h1>404</h1></html>')
            self.finish()
    return wrapper

def mobile_order_authenticated(method):
    @functools.wraps(method)
    def wrapper(self,*args,**kwargs):
        user = self.get_current_user()
        if user.has_key('belong_id') and self.rdb.query(DistributorUser).filter(DistributorUser.deleted == 0,
                                                               DistributorUser.id == user.get('belong_id')).scalar():
            return method(self,*args,**kwargs)
        else:
            self.write('<html><h1>请使用会员账号购买!</h1></html>')
            self.finish()
    return wrapper

def admin_authenticated(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            if self.request.method in ("GET","HEAD","POST","PUT","DELETE"):
                url = self.get_login_url()
                if "?" not in url:
                    if urlparse.urlsplit(url).scheme:
                        # if login url is absolute, make next absolute too
                        next_url = self.request.full_url()
                    else:
                        next_url = self.request.uri
                    url += "?" + urlencode(dict(next=next_url))
                self.redirect(url)
                return
            raise HTTPError(403)
        return method(self, *args, **kwargs)
    return wrapper