#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'gaoaifei'

from common.base_handler import BaseHandler
from services.item.comments_services import CommentsServies
from services.item.item_services import ItemService
from services.orders.orders_services import OrderServices
from ..common_handler import CommonHandler
from models.item_do import ItemComment
from utils.cache_manager import MemcacheManager
from services.member.collection_service import MemberCollectionsServices
from conf.cache_key import COLLECTION_CACHE_KEY
from common.permission_control import authenticated
from services.item.brand_service import BrandService
from services.attributes.attributes_service import AttributesService
from services.sites.nav_services import NavServices
import ujson
import sys
import datetime
import tornado.web

item_service = ItemService()
comment_service = CommentsServies()
order_service = OrderServices()
collection_service = MemberCollectionsServices()
brand_service = BrandService()
attributes_service = AttributesService()
sitenav_Services = NavServices()

class DomesticItemsDetailHandler(BaseHandler,CommonHandler):

    def get(self,show_id, *args, **kwargs):
        item_id = self.get_id_by_show_id(show_id)
        item_service.set_rdb(self.rdb)
        item = item_service.get_by_id(item_id)
        self.set_user_view_cookie(item)
        item_carts = self.get_cookie('item_carts')
        self.set_item_views(item_id)
        cart_count=0
        if item_carts:
            carts = ujson.loads(item_carts)
            cart_count = sum([int(c.get('item_num')) for c in carts])
        comment_service.set_rdb(self.rdb)
        comment_count = comment_service.get_comment_count_by_item_id(item_id)
        # 是否收藏
        user = self.get_current_user()
        is_collection = 0
        if user:
            if self.mcache:
                pass
            else:
                self.mcache = MemcacheManager().get_conn()
            user_id = user.get('id')
            collection = self.check_item_is_collection_on_cache(item_id,user_id)
            if collection:
                is_collection = 1
            else:
                is_collection = 0

        self.title = item.seo_title
        self.keywords = item.seo_keywords
        self.description = item.seo_description
        self.parent_category_id = item.top_category_id
        self.echo('items/detail.html',{'item':item,'cart_count':cart_count,'comment_count':comment_count,'is_collection':is_collection})