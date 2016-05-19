#encoding:utf-8

__author__ = 'sunlifeng'

import urllib2
import json

AppID='wxcf5a92893add3554'
AppSecret='b455aeaac27ed1e5f159ea8f2a3681bf'

WX_ACCESS_URL = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"   #含两个参数
WX_JSAPI_TICKET = "https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=%s&type=jsapi"

def getAccessToken(app_id, app_secret):
    '''
    获取令牌
    :param app_id:微信分配的应用id
    :param app_secret:微信分配的应用密钥
    :return:微信服务器返回的结果json
    '''
    f = urllib2.urlopen(WX_ACCESS_URL %(AppID, AppSecret))
    access_j = f.read().decode("utf-8")
    access_Token = json.loads(access_j)
    return access_Token

def get_jsapi_ticket(access_Token):
    '''
    获取jsapi_ticket
    :param app_id:微信分配的access_Token
    :return:微信服务器返回的结果json
    '''
    f = urllib2.urlopen(WX_JSAPI_TICKET %(access_Token))
    jsapi_ticket = f.read().decode("utf-8")
    jsapi_ticket = json.loads(jsapi_ticket)
    return jsapi_ticket


import time
import random
import string
import hashlib

class sign(object):
    def __init__(self, appId, jsapi_ticket, url):
        self.ret = {
            'nonceStr': self.__create_nonce_str(),
            'jsapi_ticket': jsapi_ticket,
            'timestamp': self.__create_timestamp(),
            'url': url
        }
        self.appId = appId

    def __create_nonce_str(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))

    def __create_timestamp(self):
        if not int(time.time()):
            return ''
        return int(time.time())

    def get_sign(self):
        string = '&'.join(['%s=%s' % (key.lower(), self.ret[key]) for key in sorted(self.ret)])
        #print string
        self.ret['signature'] = hashlib.sha1(string).hexdigest()
        self.ret['appId'] = self.appId
        return self.ret
