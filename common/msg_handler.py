#encoding:utf-8
__author__ = 'binpo'

from common.base_handler import BaseHandler
from utils.regular import Regular
import ujson
import random
import sys

# from utils.cache_manager import MemcacheManager
from utils.random_utils import create_random_digit
from utils.message import send_msg
from conf.sms_conf import LOGIN_CODE_TEMPLATE
import time

class MsgSendHandler(BaseHandler):

    def post(self,*args, **kwargs):

        pass

class PhoneCodeHandler(BaseHandler):

    def get(self, *args, **kwargs):
        phone = self.get_argument('phone')
        client = self.mcache
        if client.get(str(phone+'_send')) and int(time.time())-client.get(str(phone+'_send'))<30:
            self.write_json({'state':400,'info':'发送太频繁,稍后重试'})
        else:
            code = create_random_digit(2)
            print code
            phone = str(phone)
            client.set(phone,code,180)
            client.set((phone+'_send'),int(time.time()),180)
            content = LOGIN_CODE_TEMPLATE.format(code)
            send_msg(phone,content)
            self.write_json({'state':200,'info':'发送成功'})
