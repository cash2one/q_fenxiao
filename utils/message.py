#encoding:utf-8
__author__ = 'binpo'

import threading
import sys
import logging
import traceback
from cache_manager import MemcacheManager
LOG = logging.getLogger(__name__)
import requests
import ujson
import sys
mcache = MemcacheManager().get_conn()
API_TOKEN ='key-32ee6fa7291c1552daa5a0ebe4049be0'
def send_tel_msg(phone,content):
    if phone:
        try:
            key = 'send_tel_msg'+phone
            count = mcache.get(key)
            if not count:
                count=0
            if count>20:
                return u'每分钟只能发送'
            if not content.endswith('【全球抢购】'):
                content += '【全球抢购】'
            resp = requests.post(("https://sms-api.luosimao.com/v1/send.json"),
            auth=("api",API_TOKEN),
            data={
                "mobile": phone,
                "message": content
            },timeout=3 , verify=False)
            result = ujson.loads(resp.content)
            mcache.set(key,count+1,60)
            print result
            return result
        except Exception,e:
            print e.message
            LOG.info(sys.exc_info())

class MessageThread(threading.Thread):
    '''
        多线程发送消息
    '''
    def __init__(self,tel,content):

        threading.Thread.__init__(self)
        self.tel = tel
        self.content = content

    def run(self):
        send_tel_msg(self.tel,self.content)

def send_msg(tel,content):
    message_thread = MessageThread(tel,content)
    message_thread.start()



# if __name__=="__main__":
#     content="验证码 http://www.qqqg.com,aq3798 【怎么装】"
#     send_msg('18268802385',content)
