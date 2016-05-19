#!/usr/bin/env python
#国内电商
# -*- coding: utf-8 -*-
__author__ = 'gaoaifei'

import tornado.web
from common.base_handler import BaseHandler
from services.item.comments_services import CommentsServies
from services.item.item_services import ItemService
from services.users.user_services import UserServices
from services.orders.orders_services import OrderServices
import ujson
import sys
from ..common_handler import CommonHandler
from data_cache.user_cache import UserCache
from utils.logs import LOG
import datetime
_log = LOG('order_address_logs')

comment_service = CommentsServies()
item_service = ItemService()
order_services = OrderServices()
user_cache = UserCache()

class CnOrdersHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self,item_id, *args, **kwargs):
        '''
        直接购买页面
        :param item_id:
        :param args:
        :param kwargs:
        :return:
        '''
        user_id = self.get_current_user().get('id')
        user = self.get_current_user()
        num = self.get_argument('item_account')
        item_service = ItemService(rdb=self.rdb)
        item = item_service.get_by_id(item_id)
        if item.sale_quantity<=item.warning_quantity:
            return self.echo('order/info.html',{'info':'库存不足'})
        user_service = UserServices(rdb=self.rdb)
        #default_address = user_service.get_address(user_id=user_id,is_default=True).scalar()
        addresses = user_service.get_address(user_id=user_id)
        item.num = int(num)

        item.bussiness_buy=False
        if user.get('is_bussiness'):
            item.bussiness_buy=True
            if item.bussiness_price and item.bussiness_price>0:
                total_account = item.total_price = int(num)*item.bussiness_price
            else:
                total_account = item.total_price = int(num)*item.price
        else:
            total_account = item.total_price = int(num)*item.price
        total_tax = float(item.total_price*item.tax_rate)/100
        if total_tax<=50:
            pass
        else:
            total_account = total_account + total_tax
        self.echo('order/order.html',{'addresses':addresses,
                                      'items':[item],'total_account':total_account,'is_cart':False,'total_tax':total_tax},layout='order/order_base.html')