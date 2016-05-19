#encoding:utf-8
__author__ = 'binpo'

from common.pyoauth2 import Client

import ujson

from tornado.options import options, define
from utils.oauth_user_util import get_oauth_user_info
import urllib
from services.users.user_services import UserServices
from utils.md5_util import create_md5
from common.base_handler import BaseHandler

class QQLoginHandler(BaseHandler):
    def post(self):
        client = Client(options.QQ_KEY, options.QQ_SECRET,
                        site='https://graph.qq.com',
                        authorize_url='https://graph.qq.com/oauth2.0/authorize',
                        token_url='https://graph.qq.com/oauth2.0/token')

        authorize_url = client.auth_code.authorize_url(redirect_uri=options.QQ_CALLBACK,
                            scope='get_user_info,list_album,upload_pic,do_like')
        self.redirect(authorize_url)

    def get(self, *args, **kwargs):
        self.post()

class QQloginHandlerCallback(BaseHandler):

    def get(self, *args, **kwargs):
        code = self.get_argument('code')
        code = code.strip()
        client = Client(options.QQ_KEY, options.QQ_SECRET,
                site='https://graph.qq.com',
                authorize_url='https://graph.qq.com/oauth2.0/authorize',
                token_url='https://graph.qq.com/oauth2.0/token')
        access_token = client.auth_code.get_token(code, redirect_uri=options.QQ_CALLBACK, parse='query')


        # for key in access_token.params.keys():
        #     print access_token.params.get(key),'0000000000000'



        token = access_token.token
        client_id = access_token.params.get('client_id')
        content = urllib.urlopen('https://graph.qq.com/oauth2.0/me?access_token='+access_token.token).read()
        open_id = ujson.loads(content[content.find('{'):content.find('}')+1]).get('openid')
        user_info = get_oauth_user_info('https://graph.qq.com/user/get_user_info',oauth_consumer_key=options.QQ_KEY,access_token=access_token.token,format='json',openid=open_id)
        user = ujson.loads(user_info)

        user_service = UserServices(self.db)
        exist_user = user_service.get_user_by_qq(open_id)

        if not exist_user:
            user_service.create_user_by_qq(nick=user.get('nickname'),photo=user.get('figureurl_qq_2'),qq=open_id,sex=user.get('gender'))
            user = user_service.get_user_by_qq(open_id)
        else:
            user = exist_user
            
        print user.id   #!!!����ɾ�� by qiuyan
            
        if not user:
            self.redirect('/')
        cookies = user_service.user_format(user)
        self.set_secure_cookie('loginuser',ujson.dumps(cookies),domain=self.cookie_domain,expires_days=10)
        self.set_cookie('check_loginuser', create_md5(create_md5(ujson.dumps(cookies))),domain=self.cookie_domain,expires_days=1000)
        self.redirect('/')


    def post(self, *args, **kwargs):
        self.get()

    # def get_qq_user_info(self):
    #     https://graph.qq.com/user/get_user_info?
    #     import urllib
    #     try:
    #         import urlparse
    #     except ImportError:
    #         import urllib.parse as urlparse
    #     try:
    #         import urllib.parse as urllib_parse
    #     except ImportError:
    #         import urllib as urllib_parse
    #     weibo_user_url = options.WEIBO_USER_SHOW_URL+'?'+urllib_parse.urlencode(kwargs)
    #     response = urllib.urlopen(options.WEIBO_USER_SHOW_URL,urllib_parse.urlencode(kwargs))
    #     #print weibo_user_url
    #     response = urllib.urlopen(weibo_user_url)
    #     return  response.read()
# client = Client(KEY, SECRET,
#                 site='https://graph.qq.com',
#                 authorize_url='https://graph.qq.com/oauth2.0/authorize',
#                 token_url='https://graph.qq.com/oauth2.0/token')
#
# print '-' * 80
# authorize_url = client.auth_code.authorize_url(redirect_uri=CALLBACK,
#                     scope='get_user_info,list_album,upload_pic,do_like')
# print 'Go to the following link in your browser:'
# print authorize_url
# print '-' * 80
#
# code = raw_input('Enter the verification code and hit ENTER when you\'re done:')
# code = code.strip()
# access_token = client.auth_code.get_token(code, redirect_uri=CALLBACK, parse='query')
#
# print 'token', access_token.headers
# print access_token.expires_at