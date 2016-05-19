#encoding:utf-8
__author__ = 'binpo'
from common.base_handler import BaseHandler
from services.item.item_services import ItemService
from common_handler import CommonHandler
import datetime

item_service = ItemService()

class HomeHandler(BaseHandler,CommonHandler):

    #@unblock
    #@pagecache(key='home')
    def get(self, *args, **kwargs):
        #key=self.request.host+self.request.uri
        #content = self.mcache.get(key)
        #if not content:
        item_service.set_rdb(self.rdb)
        #query = item_service._list(is_online=True)
        new_items = item_service.get_last_items_by_category_id(3,order_by='sale_quantity desc,gmt_modified desc',having=True)[:5]
        self.parent_category_id=''
        categories = item_service.qyery_category_by_level(level=1)
        # content = self.render('index.html',
        #                       {'new_items':new_items,'categories':categories,'item_service':item_service},layout='base.html')
        #self.mcache.set(key, content,30*60) # 将渲染后的内容缓存起来
        #self.write(content)
        self.echo('index.html',{'new_items':new_items,'categories':categories,'item_service':item_service})

    def get_last_by_category(self,category_id):
        items = item_service.get_last_items_by_category_id(category_id,order_by='sale_quantity desc,gmt_modified desc')
        return items.limit(10).offset(0)

class HealthCheckHandler(BaseHandler):

    #@unblock
    def get(self, *args, **kwargs):
        self.write('ok')


class TmsHandler(BaseHandler):

    def get(self,path,**kwargs):
        self.echo(path)