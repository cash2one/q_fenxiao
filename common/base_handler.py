#encoding:utf-8
import timeit
import logging
import tornado.web
import ujson
from tornado.options import options
from services.pagination.page import Paginator
import urlparse
import urllib
from tornado.web import HTTPError
from tornado import httputil
from tenjin_base import WebTenjinBase
from models.user_do import Users
from tornado.web import decode_signed_value

from data_cache.key_cache import KeyCache
from utils.wx_util import sign
AppID='wxcf5a92893add3554'

import sys,traceback
import random

from utils.logs import LOG
log = LOG('qqqg_logs.log')
stat_time = 0.0
CACHE_SECONDE=24*3600*2

from application import engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
# self.db = session_factory()
# from sqlalchemy import exc
# from sqlalchemy import select
#
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.orm import scoped_session
# engine = create_engine(options.ENGINE,echo=False,
#                                     poolclass=QueuePool,
#                                        pool_size=200,
#                                        max_overflow=300,
#                                        pool_recycle=3600,
#                                        pool_timeout=3600)
#
# Session = scoped_session(sessionmaker(bind=engine, autoflush=True, autocommit=False))
Session = None

class BaseHandler(WebTenjinBase):

    def __init__(self, *argc, **argkw):
        global Session
        Session = scoped_session(sessionmaker(bind=engine, autoflush=True, autocommit=False))
        super(BaseHandler, self).__init__(*argc, **argkw)

    STATIC_DOMAIN = ''
    parent_category_id = 0
    @property
    def db(self):
        return Session()

    @property
    def rdb(self):
        return self.db
        #self.db = session_factory()
        # if self.application.rdb:
        #     return self.application.rdb
        # else:
        #     return None

    @property
    def mcache(self):
        return self.application.mcache

    # @property
    # def rcache(self):
    #     return self.application.rcache

    def echo(self, template, context=None, globals=None, layout='base.html'):
        data = self.render(template, context, globals, layout)
        self.write(data)

    def get_current_user(self):
        user_json = self.get_secure_cookie("loginuser",None)

        if user_json:
            user_info = ujson.loads(user_json)
            user_id = user_info.get('id')
            user_cache_key = 'user_login_cookie_'+str(user_id)
            user = self.mcache.get(user_cache_key)
            if user:
                pass
            else:
                user = self.db.query(Users).filter(Users.deleted==0,Users.id==user_id).scalar()
                user = ujson.dumps(user.user_format(user))
                self.mcache.set(user_cache_key,user,18000)
            return ujson.loads(user)
        else:
            return None
        #return user_json and ujson.loads(user_json) or None

    stat_time = 0.0

    def prepare(self):

        # super(BaseHandler, self).prepare()
        # 如果请求是GET方法,而且不是请求后台
        self.unread_msg = False
        self.cart_count = self.get_cart_count()
        self.STATIC_DOMAIN = options.STATIC_FILE_DOMAIN
        #self.STATIC_FILE_PREFIX = options.STATIC_FILE_PREFIX
        global stat_time
        stat_time = timeit.default_timer()

    def _handle_request_exception(self, e):

        try:
            log.info(traceback.format_exc())
            if self.db:
                self.db.close()
            if self.rdb:
                self.rdb.close()
            Session.remove()
            self.captureException(sys.exc_info())
            if isinstance(e, TypeError):
                self.echo('500.html')

            if isinstance(e, HTTPError):
                if e.status_code not in httputil.responses and not e.reason:
                    self.echo('500.html')
                else:
                    self.echo(str(e.status_code)+'.html',info=sys.exc_info())
            else:
                self.echo('500.html')
            # if isinstance(e, HTTPError):
            #     if e.status_code not in httputil.responses and not e.reason:
            #         self.echo('500.html')
            #     else:
            #         self.send_error(e.status_code, exc_info=sys.exc_info())
            # else:
            #     self.echo('500.html')
            self.finish()
        except:
            self.echo('500.html')
            self.finish()


    def on_finish(self):
        try:
            if self.db:
                self.db.close()
                self.db.remove()

            if self.rdb:
                self.rdb.remove()
                self.rdb.close()
            Session.remove()

            global stat_time

            if not stat_time:
                stat_time = timeit.default_timer()
            response_time = (timeit.default_timer() - stat_time) % 1000

            if response_time > 0:
                print '---------------------------RT---------------------------------'
                print '-> Current url   : ', self.request.uri
                print '-> Response time : ', response_time, ' s'
                print '--------------------------------------------------------------'
        except:
            pass
        #global stat_time

        # """ 重写结束请求前的方法函数 """
        # if self.request.method == "POST":
        #     # 如果遇到POST提交则清空缓存
        #     self.mcache.flush()

        # response_time = 0
        # response_time = (timeit.default_timer() - stat_time) % 1000
        # if response_time > 0:
        #     print '---------------------------RT---------------------------------'
        #     print '-> Current url   : ', self.request.uri
        #     print '-> Response time : ', response_time, ' s'
        #     print '--------------------------------------------------------------'


    def get_page_data(self, query, page_size = 0):
        if not page_size:
            page_size = int(self.get_argument("page_size",20))
        page = int(self.get_argument("page", 1))
        offset = (page - 1) * page_size
        result = query.limit(page_size).offset(offset)
        page_data = Paginator(self.get_page_url, page, query.count(), page_size)
        page_data.result = result
        return page_data

    def get_page_dict(self,query):
        page_data = self.get_page_data(query)
        page_dict = page_data.to_dict()
        page_dict['results'] = [{key:getattr(d,key) for key in d.columns()} for d in page_data.result],
        return page_dict

    def get_page_url(self, page,form_id=None):
        if form_id:
            return "javascript:goto_page('%s',%s);" %(form_id.strip(),page)
        path = self.request.path
        query = self.request.query
        qdict = urlparse.parse_qs(query)
        for k, v in qdict.items():
            if isinstance(v, list):
                qdict[k] = v and v[0] or ''
        qdict['page'] = page
        return path + '?' + urllib.urlencode(qdict)

    def check_validate_code(self,code):
        user_ip = self.get_client_ip
        key = str(user_ip+'_img_code')
        code_value = self.mcache.get(key)
        if code and code_value:
            if code.lower()==code_value.lower():
                return True,'OK'
            else:
                return False,'验证码不正确'
        else:
            if not code_value:
                return False,'验证码过期'
            else:
                return False,'验证码不能为空'

    def check_phone_code(self,phone,code):
        key = phone
        cache_code = self.mcache.get(key)
        if code and cache_code:
            if code==cache_code:
                return True,''
        return False,'动态验证码错误'

    def set_user_cookies(self,cookies,days=7):
        # self.set_secure_cookie('loginuser',cookies,domain=self.cookie_domain,expires_days=days)
        self.set_secure_cookie('loginuser',cookies,expires_days=days)

    def get_cart_count(self):
        '''
        获取购物车
        :return:
        '''
        item_carts = self.get_cookie('item_carts')
        cart_count=0
        if item_carts:
            carts = ujson.loads(item_carts)
            cart_count = sum([int(c.get('item_num')) for c in carts])
        return cart_count

    def get_site_nav(self):
           # def get_site_nav(self):
        from services.sites.nav_services import NavServices

        sit_nav_html = self.mcache.get('site_nav_html')
        if not sit_nav_html:
            nav_service = NavServices(rdb=self.db)
            navs = nav_service.query_all()
            sit_nav_html= self.render('include/cache_nav.html',{'navs':navs})
            self.mcache.set('site_nav_html',sit_nav_html,7*24*36)
        return sit_nav_html

from common.permission_control import admin_authenticated

class AdminBaseHandler(WebTenjinBase):

    def __init__(self, *argc, **argkw):
        global Session
        Session = scoped_session(sessionmaker(bind=engine, autoflush=True, autocommit=False))
        super(AdminBaseHandler, self).__init__(*argc, **argkw)

    STATIC_DOMAIN = ''
    CDN_DOMAIN=''
    log = logging.getLogger(__name__)

    @property
    def db(self):
        return Session()

    @property
    def rdb(self):
        return self.db
        # if self.application.rdb:
        #     return self.application.rdb
        # else:
        #     return None

    @property
    def mcache(self):
        return self.application.mcache

    # @property
    # def rcache(self):
    #     return self.application.rcache

    def echo(self, template, context=None, globals=None, layout='admin/include/base.html'):
        self.write(self.render(template, context, globals, layout))

    def get_current_user(self):
        user_json = self.get_secure_cookie("admin_login",None)
        return ujson.loads(user_json) if user_json else None

    def get_photo_url(self, user, size="normal"):
        if not user:
            return self.static_url("default.png")

        photo = "photo_url" if size == "normal" else "middle_photo_url"
        if photo not in user and user[photo]:
            photo = "photo_url"

        if not user[photo]:
            return self.static_url("images/default.png")
        if "open" in user and user["open"] != "google":
            if user[photo].startswith("http"):
                return user[photo]
        return self.static_url("icons/%s" % user[photo])

    stat_time = 0.0

    @admin_authenticated
    def prepare(self):

        if not self.check_permssion():
            self.write('权限不够')
            self.finish()
        # self.STATIC_FILE_DOMAIN = options.STATIC_FILE_DOMAIN
        # self.#IMG_DOMAIN='http://img.zenmez.c# om'
        # self.operation_name=''
        # global stat_time
        # stat_time = timeit.default_timer()

    def check_permssion(self):
        return True

    # def check_permssion(self):
    #     if self.current_user.get('is_employee'):
    #         user_roles = self.current_user.get('role_codes')
    #         cur_url = self.request.uri
    #         role_cache = RolePermissionCache(self.db)
    #         roles_code = user_roles.split(',') if user_roles else []
    #         roles_code.sort()
    #         for r in roles_code:
    #             permission = role_cache.get_role_permission(r)
    #             for p in permission:
    #                 if re.match(r'^%s'%p, cur_url):
    #                     return True
    #     return False

    def on_finish(self):

        #print dir(self)
        '''

                'arguments', 'body', 'body_arguments', 'connection', 'cookies', 'files', 'finish',
                'full_url', 'get_ssl_certificate', 'headers', 'host', 'method', 'path', 'protocol', 'query',
                'query_arguments', 'remote_ip', 'request_time', 'supports_http_1_1', 'uri', 'version', 'write'
        '''
        try:
            method = self.request.method
            action = self.request.path
            self.get_paras_dict()
            if self.qdict.has_key('_xsrf'):
                self.qdict.pop('_xsrf')

            ip = self.get_client_ip
            #     Ip = self.request.headers.get("X-Real-IP",'')
            # logging.debug("_base>>ip:{0}".format(Ip))
            #
            # print Ip,'------------xclient ip --------------'

            self.qdict['ip'] = ip #self.request.remote_ip
            data = ujson.dumps(self.qdict)
            #print self.request.query
            #print type(self.request.query_arguments)
            #print self.request.full_url

            # if self.operation_name!='':
            #     try:
            #         user = self.get_current_user()
            #         #operation_log(method=method,action=action,data=data,user_id=user.get('id'),nick=user.get('nick'),action_name=self.operation_name)
            #     except Exception,e:
            #         pass

            if self.db:
                self.db.close()
            if self.rdb:
                self.rdb.close()
            Session.remove()
            global stat_time

            if not stat_time:
                stat_time = timeit.default_timer()
            response_time = (timeit.default_timer() - stat_time) % 1000

            if response_time > 0:
                print '---------------------------RT---------------------------------'
                print '-> Current url   : ', self.request.uri
                print '-> Response time : ', response_time, ' s'
                print '--------------------------------------------------------------'

        except Exception,e:
            pass

    def get_page_data(self, query):
        """
        获取分页数据
        """
        page_size = int(self.get_argument("page_size",30))
        page = int(self.get_argument("page", 1))
        if page<=0:
            page=1
        offset = (page - 1) * page_size
        result = query.limit(page_size).offset(offset)
        page_data = Paginator(self.get_page_url, page, query.count(), page_size)
        page_data.result = result
        return page_data

    def get_page_url(self, page,form_id=None):

        """参数解析
        :page 页号
        :form_id
        """
        if form_id:
            return "javascript:goto_page('%s',%s);" %(form_id.strip(),page)
        path = self.request.path
        qdict={}
        if self.request.method=='GET':
            query = self.request.query
            #qdict =
            for k, v in urlparse.parse_qs(query).items():
                if isinstance(v, list):
                    qdict[k] = v and v[0] or ''
                #else:self.qdict[k] = v and v[0] or ''
            qdict['page'] = page
        else:
            qdict={}
            query = self.request.arguments
            for key in query.keys():
                qdict[key]=len(query[key])==1 and (query[key][0] and query[key][0] or '') or query[key]
        return path + '?' + urllib.urlencode(qdict)

    def _handle_request_exception(self,e):

        log.info(traceback.format_exc())
        if self.db:
            self.db.close()
        if self.rdb:
            self.rdb.close()
        Session.remove()
        # self.captureException(sys.exc_info())
        self.echo('admin/error/error.html',{'error_info':'info'})


from services.advertising.Advertising_service import AdvertisingService
from services.advertising.advertising_position_service import AdvertisingPositionService
import datetime

advertising_service = AdvertisingService()
advertising_position_service = AdvertisingPositionService()

class MobileBaseHandler(WebTenjinBase):

    def __init__(self, *argc, **argkw):
        global Session
        Session = scoped_session(sessionmaker(bind=engine, autoflush=True, autocommit=False))
        super(MobileBaseHandler, self).__init__(*argc, **argkw)

    STATIC_DOMAIN = ''
    parent_category_id = 0
    @property
    def db(self):
        return Session()

    @property
    def rdb(self):
        return self.db
        # if self.application.rdb:
        #     return self.application.rdb
        # else:
        #     return None

    @property
    def mcache(self):
        return self.application.mcache

    # @property
    # def rcache(self):
    #     return self.application.rcache

    def echo(self, template, context=None, globals=None, layout=''):
        data = self.render(template, context, globals, layout)
        self.write(data)

    def get_current_user(self):
        user_json = self.get_secure_cookie("fenxiao_loginuser",None)
        if user_json:
            user_info = ujson.loads(user_json)
            user_id = user_info.get('id')
            if user_info.has_key('role_type'):
                user_cache_key = 'fenxiao_drp_login_cookie_'+str(user_id)
                user_key = 'd_user'
            else:
                user_cache_key = 'fenxiao_user_login_cookie_'+str(user_id)
                user_key = 'c_user'
            user = self.mcache.get(user_cache_key)
            if user:
                return ujson.loads(user)
            else:
                if user_key == 'd_user':
                    drp_user = self.rdb.query(DistributorUser).filter(DistributorUser.deleted == 0,DistributorUser.id == user_id).scalar()
                    if drp_user:
                        user = ujson.dumps(drp_user.user_format(drp_user))
                        self.mcache.set(user_cache_key,user,18000)
                        return ujson.loads(user)

                elif user_key == 'c_user':
                    c_user = self.db.query(Users).filter(Users.deleted==0,Users.id==user_id).scalar()
                    if c_user:
                        user = ujson.dumps(c_user.user_format(c_user))
                        self.mcache.set(user_cache_key,user,18000)
                        return ujson.loads(user)

                return None
        else:
            return None

    stat_time = 0.0

    def prepare(self):

        # super(BaseHandler, self).prepare()
        # 如果请求是GET方法,而且不是请求后台
        self.unread_msg = False
        self.cart_count = self.get_cart_count()
        self.STATIC_DOMAIN = options.STATIC_FILE_DOMAIN
        #self.STATIC_FILE_PREFIX = options.STATIC_FILE_PREFIX
        global stat_time
        stat_time = timeit.default_timer()

    def _handle_request_exception(self, e):
        try:
            log.info(traceback.format_exc())
            if self.db:
                self.db.close()
            if self.rdb:
                self.rdb.close()
            Session.remove()

            if isinstance(e, TypeError):
                self.echo('mobile/include/500.html')

            if isinstance(e, HTTPError):
                if e.status_code not in httputil.responses and not e.reason:
                    self.echo('mobile/include/400.html')
                else:
                    self.echo(str(e.status_code)+'.html',info=sys.exc_info())
            else:
                self.echo('mobile/include/500.html')
            self.finish()
        except:
            self.echo('mobile/include/500.html')
            self.finish()


    def on_finish(self):
        try:
            if self.db:
                self.db.close()
            if self.rdb:
                self.rdb.close()
            global stat_time
            Session.remove()
            if not stat_time:
                stat_time = timeit.default_timer()
            response_time = (timeit.default_timer() - stat_time) % 1000

            if response_time > 0:
                print '---------------------------RT---------------------------------'
                print '-> Current url   : ', self.request.uri
                print '-> Response time : ', response_time, ' s'
                print '--------------------------------------------------------------'
        except:
            pass


    def get_page_data(self, query, page_size = 0):
        if not page_size:
            page_size = int(self.get_argument("page_size",5))
        page = int(self.get_argument("page", 1))
        offset = (page - 1) * page_size
        result = query.limit(page_size).offset(offset)
        page_data = Paginator(self.get_page_url, page, query.count(), page_size)
        page_data.result = result
        return page_data

    def get_page_dict(self,query):
        page_data = self.get_page_data(query)
        page_dict = page_data.to_dict()
        page_dict['results'] = [{key:getattr(d,key) for key in d.columns()} for d in page_data.result],
        return page_dict

    def get_page_url(self, page,form_id=None):
        if form_id:
            return "javascript:goto_page('%s',%s);" %(form_id.strip(),page)
        path = self.request.path
        query = self.request.query
        qdict = urlparse.parse_qs(query)
        for k, v in qdict.items():
            if isinstance(v, list):
                qdict[k] = v and v[0] or ''
        qdict['page'] = page
        return path + '?' + urllib.urlencode(qdict)

    def check_validate_code(self,code):
        user_ip = self.get_client_ip
        key = str(user_ip+'_img_code')
        code_value = self.mcache.get(key)
        if code and code_value:
            if code.lower()==code_value.lower():
                return True,'OK'
            else:
                return False,'验证码不正确'
        else:
            if not code_value:
                return False,'验证码过期'
            else:
                return False,'验证码不能为空'

    def check_phone_code(self,phone,code):
        key = phone
        cache_code = self.mcache.get(key)
        if code and cache_code:
            if code==cache_code:
                return True,''
        return False,'动态验证码错误'

    def set_user_cookies(self,cookies,days=7):
        # self.set_secure_cookie('loginuser',cookies,domain=self.cookie_domain,expires_days=days)
        self.set_secure_cookie('loginuser',cookies,expires_days=days)

    def get_cart_count(self):
        '''
        获取购物车
        :return:
        '''
        item_carts = self.get_cookie('fenxiao_item_carts')
        cart_count=0
        if item_carts:
            carts = ujson.loads(item_carts)
            cart_count = sum([int(c.get('item_num')) for c in carts])
        return cart_count

    def get_site_nav(self):
           # def get_site_nav(self):
        from services.sites.nav_services import NavServices

        sit_nav_html = self.mcache.get('mobile/include/site_nav_html')
        if not sit_nav_html:
            nav_service = NavServices(rdb=self.db)
            navs = nav_service.query_all()
            sit_nav_html= self.render('mobile/include/cache_nav.html',{'navs':navs})
            self.mcache.set('mobile/include/site_nav_html',sit_nav_html,7*24*36)
        return sit_nav_html

    def obj_to_dict(self,obj,keys,format='%Y-%m-%d %H:%M:%S'):
        data={}
        for key in keys:
            if obj.__dict__.get(key,None):
                data[key] = obj.__dict__.get(key,None)
                if isinstance(data[key],datetime.datetime):
                    data[key]=datetime.datetime.strftime(data[key],format)
            elif obj.__dict__.get(key) == 0:
                data[key] = 0
            else:
                data[key] = ''
        return data

    def share_weixin(self,share_url):

        page_cache = KeyCache()
        access_token = page_cache.get_access_token()
        jsapi_ticket = page_cache.get_jsapi_ticket(access_token)
        wx_sign = sign(AppID, jsapi_ticket, share_url)
        dic_sign = wx_sign.get_sign()
        return dic_sign


class AppBaseHandler(WebTenjinBase):

    def __init__(self, *argc, **argkw):
        global Session
        Session = scoped_session(sessionmaker(bind=engine, autoflush=True, autocommit=False))
        super(AppBaseHandler, self).__init__(*argc, **argkw)

    STATIC_DOMAIN = ''
    parent_category_id = 0
    @property
    def db(self):
        return Session()

    @property
    def rdb(self):
        return self.db
        # if self.application.rdb:
        #     return self.application.rdb
        # else:
        #     return None

    @property
    def mcache(self):
        return self.application.mcache

    def echo(self, template, context=None, globals=None, layout=''):
        data = self.render(template, context, globals, layout)
        self.write(data)

    def get_current_user(self):
        self.get_paras_dict()
        login_token = self.qdict.get('login_token')
        if login_token:
            user_json = decode_signed_value(self.application.settings["cookie_secret"],'loginuser',login_token) #判断token合法性
            if user_json:
                user_info = ujson.loads(user_json)
                user_id = user_info.get('id')
                if user_id:
                    user_cache_key = 'user_login_cookie_'+str(user_id)
                    user = self.mcache.get(user_cache_key)
                    if user:
                        pass
                    else:
                        user = self.db.query(Users).filter(Users.deleted==0,Users.id==user_id).scalar()
                        user = ujson.dumps(user.user_format(user))
                        self.mcache.set(user_cache_key,user,18000)
                    return ujson.loads(user)
        else:
            user_json = self.get_secure_cookie("loginuser",None)
            if user_json:
                user_info = ujson.loads(user_json)
                user_id = user_info.get('id')
                user_cache_key = 'user_login_cookie_'+str(user_id)
                user = self.mcache.get(user_cache_key)
                if user:
                    pass
                else:
                    user = self.db.query(Users).filter(Users.deleted==0,Users.id==user_id).scalar()
                    user = ujson.dumps(user.user_format(user))
                    self.mcache.set(user_cache_key,user,18000)
                return ujson.loads(user)
        return None

    stat_time = 0.0

    def prepare(self):

        # super(BaseHandler, self).prepare()
        # 如果请求是GET方法,而且不是请求后台
        self.unread_msg = False
        self.cart_count = self.get_cart_count()
        self.STATIC_DOMAIN = options.STATIC_FILE_DOMAIN
        #self.STATIC_FILE_PREFIX = options.STATIC_FILE_PREFIX
        global stat_time
        stat_time = timeit.default_timer()

    def _handle_request_exception(self, e):
        try:

            if self.db:
                self.db.close()
            if self.rdb:
                self.rdb.close()
            Session.remove()
            if isinstance(e, TypeError):
                self.echo('mobile/include/500.html')

            if isinstance(e, HTTPError):
                if e.status_code not in httputil.responses and not e.reason:
                    self.echo('mobile/include/500.html')
                else:
                    self.echo(str(e.status_code)+'.html',info=sys.exc_info())
            else:
                self.echo('mobile/include/500.html')
            # if isinstance(e, HTTPError):
            #     if e.status_code not in httputil.responses and not e.reason:
            #         self.echo('500.html')
            #     else:
            #         self.send_error(e.status_code, exc_info=sys.exc_info())
            # else:
            #     self.echo('500.html')
            self.finish()
        except:
            self.echo('mobile/include/500.html')
            self.finish()


    def on_finish(self):
        try:
            if self.db:
                self.db.close()
            if self.rdb:
                self.rdb.close()
            global stat_time
            Session.remove()
            if not stat_time:
                stat_time = timeit.default_timer()
            response_time = (timeit.default_timer() - stat_time) % 1000

            if response_time > 0:
                print '---------------------------RT---------------------------------'
                print '-> Current url   : ', self.request.uri
                print '-> Response time : ', response_time, ' s'
                print '--------------------------------------------------------------'
        except:
            pass


    def get_page_data(self, query, page_size = 0):
        if not page_size:
            page_size = int(self.get_argument("page_size",5))
        page = int(self.get_argument("page", 1))
        offset = (page - 1) * page_size
        result = query.limit(page_size).offset(offset)
        page_data = Paginator(self.get_page_url, page, query.count(), page_size)
        page_data.result = result
        return page_data

    def get_page_dict(self,query):
        page_data = self.get_page_data(query)
        page_dict = page_data.to_dict()
        page_dict['results'] = [{key:getattr(d,key) for key in d.columns()} for d in page_data.result],
        return page_dict

    def get_page_url(self, page,form_id=None):
        if form_id:
            return "javascript:goto_page('%s',%s);" %(form_id.strip(),page)
        path = self.request.path
        query = self.request.query
        qdict = urlparse.parse_qs(query)
        for k, v in qdict.items():
            if isinstance(v, list):
                qdict[k] = v and v[0] or ''
        qdict['page'] = page
        return path + '?' + urllib.urlencode(qdict)

    def check_validate_code(self,code):
        user_ip = self.get_client_ip
        key = str(user_ip+'_img_code')
        code_value = self.mcache.get(key)
        if code and code_value:
            if code.lower()==code_value.lower():
                return True,'OK'
            else:
                return False,'验证码不正确'
        else:
            if not code_value:
                return False,'验证码过期'
            else:
                return False,'验证码不能为空'

    def check_phone_code(self,phone,code):
        key = phone
        cache_code = self.mcache.get(key)
        if code and cache_code:
            if code==cache_code:
                return True,''
        return False,'动态验证码错误'

    def set_user_cookies(self,cookies,days=7):
        # self.set_secure_cookie('loginuser',cookies,domain=self.cookie_domain,expires_days=days)
        self.set_secure_cookie('loginuser',cookies,expires_days=days)

    def get_cart_count(self):
        '''
        获取购物车
        :return:
        '''
        item_carts = self.get_cookie('item_carts')
        cart_count=0
        if item_carts:
            carts = ujson.loads(item_carts)
            cart_count = sum([int(c.get('item_num')) for c in carts])
        return cart_count

    def obj_to_dict(self,obj,keys,format='%Y-%m-%d %H:%M:%S'):
        data={}
        for key in keys:
            if obj.__dict__.get(key,None):
                data[key] = obj.__dict__.get(key,None)
                if isinstance(data[key],datetime.datetime):
                    data[key]=datetime.datetime.strftime(data[key],format)
            elif obj.__dict__.get(key) == 0:
                data[key] = 0
            else:
                data[key] = ''
        return data


# class RoleHandler(BaseHandler):

from permission_control import distributor_user_authenticated
from models.user_do import DistributorUser

class DistributorHandler(WebTenjinBase):

    def __init__(self, *argc, **argkw):
        global Session
        Session = scoped_session(sessionmaker(bind=engine, autoflush=True, autocommit=False))
        super(DistributorHandler, self).__init__(*argc, **argkw)

    STATIC_DOMAIN = ''
    parent_category_id = 0
    @property
    def db(self):
        return Session()

    @property
    def rdb(self):
        return self.db
        #self.db = session_factory()
        # if self.application.rdb:
        #     return self.application.rdb
        # else:
        #     return None

    @property
    def mcache(self):
        return self.application.mcache

    # @property
    # def rcache(self):
    #     return self.application.rcache

    def echo(self, template, context=None, globals=None, layout=''):
        data = self.render(template, context, globals, layout)
        self.write(data)

    def get_current_user(self):
        user_json = self.get_secure_cookie("login_distributor_user",None)

        if user_json:
            user_info = ujson.loads(user_json)
            user_id = user_info.get('id')
            user_cache_key = 'login_distributor_user_'+str(user_id)
            user = self.mcache.get(user_cache_key)
            if user:
                return ujson.loads(user)
            else:
                user = self.db.query(DistributorUser).filter(DistributorUser.deleted==0,DistributorUser.id==user_id,DistributorUser.status=='normal').scalar()
                if user:
                    user = ujson.dumps(user.user_format(user))
                    self.mcache.set(user_cache_key,user,18000)
                    return ujson.loads(user)
        else:
            return None
        #return user_json and ujson.loads(user_json) or None

    stat_time = 0.0

    @distributor_user_authenticated
    def prepare(self):

        # super(BaseHandler, self).prepare()
        # 如果请求是GET方法,而且不是请求后台
        self.unread_msg = False
        self.STATIC_DOMAIN = options.STATIC_FILE_DOMAIN
        global stat_time
        stat_time = timeit.default_timer()

    def _handle_request_exception(self, e):

        try:
            log.info(traceback.format_exc())
            if self.db:
                self.db.close()
            if self.rdb:
                self.rdb.close()
            Session.remove()
            self.captureException(sys.exc_info())
            if isinstance(e, TypeError):
                self.echo('500.html')
            if isinstance(e, HTTPError):
                if e.status_code not in httputil.responses and not e.reason:
                    self.echo('500.html')
                else:
                    self.echo(str(e.status_code)+'.html',info=sys.exc_info())
            else:
                self.echo('500.html')
            self.finish()
        except:
            self.echo('500.html')
            self.finish()


    def on_finish(self):
        try:
            if self.db:
                self.db.close()
                self.db.remove()
            if self.rdb:
                self.rdb.remove()
                self.rdb.close()
            Session.remove()
            global stat_time
            if not stat_time:
                stat_time = timeit.default_timer()
            response_time = (timeit.default_timer() - stat_time) % 1000

            if response_time > 0:
                print '---------------------------RT---------------------------------'
                print '-> Current url   : ', self.request.uri
                print '-> Response time : ', response_time, ' s'
                print '--------------------------------------------------------------'
        except:
            pass

    def get_page_data(self, query, page_size = 0):
        if not page_size:
            page_size = int(self.get_argument("page_size",20))
        page = int(self.get_argument("page", 1))
        offset = (page - 1) * page_size
        result = query.limit(page_size).offset(offset)
        page_data = Paginator(self.get_page_url, page, query.count(), page_size)
        page_data.result = result
        return page_data

    def get_page_dict(self,query):
        page_data = self.get_page_data(query)
        page_dict = page_data.to_dict()
        page_dict['results'] = [{key:getattr(d,key) for key in d.columns()} for d in page_data.result],
        return page_dict

    def get_page_url(self, page,form_id=None):
        if form_id:
            return "javascript:goto_page('%s',%s);" %(form_id.strip(),page)
        path = self.request.path
        query = self.request.query
        qdict = urlparse.parse_qs(query)
        for k, v in qdict.items():
            if isinstance(v, list):
                qdict[k] = v and v[0] or ''
        qdict['page'] = page
        return path + '?' + urllib.urlencode(qdict)


    def check_phone_code(self,phone,code):
        key = phone
        cache_code = self.mcache.get(key)
        if code and cache_code:
            if code==cache_code:
                return True,''
        return False,'动态验证码错误'

    def set_user_cookies(self,cookies,days=7):
        # self.set_secure_cookie('loginuser',cookies,domain=self.cookie_domain,expires_days=days)
        self.set_secure_cookie('loginuser',cookies,expires_days=days)

    def get_id_by_show_id(self,showId):
        '''
        根据showid获取真实id值
        :param showId: type string 自动增长列id值
        :return:
        '''
        showId = str(showId)
        i = showId[len(showId)-1]
        j = showId[0:len(showId)-1]
        k = (int(j) - int(i) - 1000)/int(i)
        return k

    def set_show_id_by_id(self,id):
        '''
        设置showid
        :param id: 真实id
        :return:
        '''
        a = random.randint(1,9)
        b = a*int(id) + 1000 + a
        j = str(b) + str(a)
        return j

    def get_distributors_by_id(self,id):
        '''
        获取分销商
        :param id:
        :return:
        '''
        drp = self.rdb.query(DistributorUser).filter(DistributorUser.id==id,
                                                      DistributorUser.parent_id==0,DistributorUser.role_type==0).scalar()


        if not drp:
            return ''
        else:
            return drp.real_name


