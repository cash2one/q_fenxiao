#encoding:utf-8

import os
import urlparse
import tenjin
import tornado.web

from tenjin.helpers import *
_engine = tenjin.Engine(path=[os.path.join(os.path.dirname(__file__),'templates')], cache=tenjin.MemoryCacheStorage(),preprocess=True)
_cache_engine = tenjin.Engine(path=[os.path.join(os.path.dirname(__file__),'templates')], cache=tenjin.MemoryCacheStorage(),preprocess=True)
_cache_engine.timestamp_interval = 120

import ujson
from setting import COOKIE_DOMAIN,STATIC_DOMAIN

class TenjinBase(tornado.web.RequestHandler):

    def __init__(self, *argc, **argkw):
        self.title=''
        self.description=''
        self.keywords=''
        self.cookie_domain = COOKIE_DOMAIN
        self.static_domain = STATIC_DOMAIN
        super(TenjinBase, self).__init__(*argc, **argkw)

    @property
    def get_client_ip(self):
        ip = self.request.headers.get("X-Client-Ip",'')
        if ip==None or ip=='':
            ip = self.request.headers.get("X-Real-IP",'')
        if ip==None or ip=='':
            ip = self.request.headers.get("X-Forwarded-For",None)
        if ip==None or ip=='':
            ip = self.request.remote_ip
        return ip.split(',')[0]

    def get_paras_dict(self):
        """
        :todo 获取请求参数 字典
        """
        if self.request.method=='GET':
            query = self.request.query
            self.qdict = urlparse.parse_qs(query)
            for k, v in self.qdict.items():
                self.qdict[k] = v and v[0] or ''
        elif self.request.method in ('POST','PUT','DELETE'):
            self.qdict={}
            query = self.request.arguments
            for key in query.keys():
                self.qdict[key]=len(query[key])!=1 and query[key] or (query[key][0] and query[key][0] or '')

    def get_show_img_url(self,img_url,width):
        _url = ''
        if img_url:
            img_list = img_url.split('@')
            if len(img_list)<=1:
                _url = img_list[0]+'@'+str(width)+'h.jpg'
            else:
                tmp_list = img_list[:-1]
                tmp_list.append('@')
                tmp_list.append(str(width)+'h_')
                tmp_list.append(img_list[-1])
                _url = ''.join(tmp_list)
        return _url

    def set_cache(self, seconds, is_privacy=None):
        if seconds <= 0:
            self.set_header('Cache-Control', 'no-cache')
            #self.set_header('Expires', 'Fri, 01 Jan 1990 00:00:00 GMT')
        else:
            if is_privacy:
                privacy = 'public, '
            elif is_privacy is None:
                privacy = ''
            else:
                privacy = 'private, '
            self.set_header('Cache-Control', '%smax-age=%s' % (privacy, seconds))


class WebTenjinBase(TenjinBase):

    def render(self, template, context=None, globals=None, layout=False):
        if context is None:
            context = {}
        args = dict(
            handler=self,
            request=self.request,
            current_user=self.current_user,
            xsrf_form_html=self.xsrf_form_html(),
            xsrf_token=self.xsrf_token,
        )
        context.update(args)
        return _engine.render(template, context, globals, layout)


    def cache_render(self, template, context=None, globals=None, layout=False):
        '''页面缓存'''
        if context is None:
            context = {}
        args = dict(
            handler=self,
            request=self.request,
            current_user=self.current_user,
            xsrf_form_html=self.xsrf_form_html(),
            xsrf_token=self.xsrf_token,
        )
        context.update(args)
        return _cache_engine.render(template, context, globals, layout)

    def echo(self, template, context=None, globals=None, layout=False):

        if context is None:
            context = {}
        args = dict(
            handler=self,
            request=self.request,
            current_user=self.current_user,
            xsrf_form_html=self.xsrf_form_html,
            xsrf_token=self.xsrf_token,
        )
        context.update(args)
        self.write(self.render(template, context, globals,layout))


    def cache_echo(self, template, context=None, globals=None, layout=False):

        if context is None:
            context = {}
        args = dict(
            handler=self,
            request=self.request,
            current_user=self.current_user,
            xsrf_form_html=self.xsrf_form_html,
            xsrf_token=self.xsrf_token,
        )
        context.update(args)
        self.write(self.cache_render(template, context, globals,layout))

    def write_json(self,data):
        '''
        :todo 返回json数据
        :param data:
        :return:
        '''
        return self.write(ujson.dumps(data))
