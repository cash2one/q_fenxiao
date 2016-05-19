#encoding:utf-8
__author__ = 'binpo'

from utils.cache_manager import MemcacheManager
from utils import wx_util


AppID='wxcf5a92893add3554'
AppSecret='b455aeaac27ed1e5f159ea8f2a3681bf'

WX_ACCESS_URL = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"   #含两个参数
WX_JSAPI_TICKET = "https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=%s&type=jsapi"

from cache_base import CacheBase

class KeyCache(CacheBase):

    def refresh_cache(self,key=None):
        '''
        刷新缓存
        :param key: 缓存主键
        :return:异常信息 or 缓存结果
        '''
        if not key:
            return "Key Empty!"
        elif not self.key_func.has_key(key):
            return "Key Not Exists!"
        else:
            pass
        self.mcache.delete(key)  #清空
        return self.key_func[key]()  #刷新

    def get_access_token(self):
        app_id = AppID
        app_secret = AppSecret
        mcache_key = 'wx_access_token_'+str(app_id)
        access_token = self.mcache.get(mcache_key)
        if not access_token or access_token == '':
            dic_accessToken = wx_util.getAccessToken(app_id, app_secret)
            if dic_accessToken.has_key('errcode'):
                raise Exception("Get Access Token Error:" + dic_accessToken.get('errmsg'))
            access_token = dic_accessToken.get("access_token")
            self.mcache.set(mcache_key, access_token, 6600)
            if app_id == AppID:#全球抢购
                #同时刷新ticket
                mcache_key = 'wx_jsapi_ticket'
                dic_jsapi_ticket = wx_util.get_jsapi_ticket(access_token)
                if dic_jsapi_ticket.has_key('errcode') and dic_jsapi_ticket.get('errcode') <> 0:
                    raise Exception("Get jsapi_ticket Error:" + dic_jsapi_ticket.get('errmsg'))
                jsapi_ticket = dic_jsapi_ticket.get("ticket")
                self.mcache.set(mcache_key, jsapi_ticket, 6600)
        return access_token

    def get_jsapi_ticket(self, access_token):
        mcache_key = 'wx_jsapi_ticket'
        jsapi_ticket = self.mcache.get(mcache_key)
        if not jsapi_ticket or jsapi_ticket == '':
            dic_jsapi_ticket = wx_util.get_jsapi_ticket(access_token)
            if dic_jsapi_ticket.has_key('errcode') and dic_jsapi_ticket.get('errcode') <> 0:
                raise Exception("Get jsapi_ticket Error:" + dic_jsapi_ticket.get('errmsg'))
            jsapi_ticket = dic_jsapi_ticket.get("ticket")
            self.mcache.set(mcache_key, jsapi_ticket, 6600)
        return jsapi_ticket

