#encoding:utf-8
__author__ = 'binpo'

from cache_base import CacheBase
import ujson
from services.users.user_services import UserServices
from utils.md5_util import create_md5

class UserCache(CacheBase):

    def get_user_info(self,user_id):
        '''
        获取用户信息
        :param user_id:
        :return:
        '''
        key='users_'+str(user_id)
        user_info = self.mcache.get(key)
        if user_info:
            return ujson.loads(user_info)
        else:
            user_service = UserServices(rdb=self.db)
            user = user_service.get_user_by_id(user_id=user_id)
            user = user.user_format()
            self.mcache.set(key,ujson.dumps(user),7*24*36)
            self.db.close()
            return user

    def user_daily_buy_check(self,category_id,card_num):
        '''
        判断是否已经买过了的订单
        :param category_id:
        :param username:
        :param card_num:
        :return:
        '''
        key = create_md5(str(category_id)+str(card_num))
        value = self.mcache.get(key)
        if value:
            return False
        else:
            return True

    def set_daily_buy_cache(self,category_id,card_num):
        import datetime
        key = create_md5(str(category_id)+str(card_num))
        seconds=(datetime.datetime.strptime(datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d')+' 23:59:59','%Y-%m-%d %H:%M:%S')-datetime.datetime.now()).seconds
        self.mcache.set(key,key,seconds)

    def delete_daily_buy(self,category_id,card_num):
        '''
        判断是否已经买过了的订单
        :param category_id:
        :param username:
        :param card_num:
        :return:
        '''
        key = create_md5(str(category_id)+str(card_num))
        value = self.mcache.get(key)
        if value:
            try:
                self.mcache.delete(key)
            except Exception,e:
                print e.message
    ###############################################################
    def user_daily_pay_check(self,category_id,card_num):
        '''
        判断是否还有未支付的订单
        :param category_id:
        :param card_num:
        :return:
        '''
        key = str(category_id)+str(card_num)
        value = self.mcache.get(key)
        if value:
            return False
        else:
            return True

    def set_daily_pay_cache(self,category_id,card_num,order_id=None):
        key = str(category_id)+str(card_num)
        self.mcache.set(key,key,10800)
        order_key='order_'+str(order_id)
        value = self.mcache.get(order_key)
        if value:
            value = value+','+key
        else:
            value=key
        self.mcache.set(order_key,value,10800)

    def delete_user_daily_pay(self,order_id):
        try:
            order_key='order_'+str(order_id)
            cache_value = self.mcache.get(order_key)
            #key = str(category_id)+str(card_num)
            # cache_value = self.mcache.get(value)
            if cache_value:
                for key in cache_value.split(','):
                    self.mcache.delete(key)
        except Exception,e:
            print e.message

