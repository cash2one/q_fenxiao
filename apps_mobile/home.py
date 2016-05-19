#encoding:utf-8
__author__ = 'binpo'

from services.advertising.advertising_position_service import AdvertisingPositionService
from services.advertising.Advertising_service import AdvertisingService
from services.item.item_services import ItemService

from apps_mobile.common_handler import CommonHandler
from services.sites.nav_services import NavServices
import traceback
PAGE_SIZE = 4

advertising_position_service = AdvertisingPositionService()
advertising_service = AdvertisingService()
item_service = ItemService()


class TmsHandler(CommonHandler):

    def get(self,path,**kwargs):
        # path = 'mobile/' + path
        self.echo(path)
        # self.redirect('/')

class HomeHandler(CommonHandler):

    def get(self, *args, **kwargs):
        try:
            nav_service = NavServices(rdb=self.db)
            navs = nav_service.query_all()
            self.echo('mobile/index.html',{'navs':navs})
        except Exception,e:
            self.echo('mobile/member/info.html',{'info':'程序错误:' + traceback.format_exc()})


class ShopSiteHandler(CommonHandler):

    def get(self,shop_id, **kwargs):
        try:
            nav_service = NavServices(rdb=self.db)
            navs = nav_service.query_all()
            self.echo('mobile/index.html',{'navs':navs})
        except Exception,e:
            self.echo('mobile/member/info.html',{'info':'程序错误:' + traceback.format_exc()})


class SelectGoodHandler(CommonHandler):

    def get(self,*args, **kwargs):
        try:
            drp_user_id = self.get_drp_user_id()
            selected_items = selectGoods_format(self,drp_user_id)
            self.write_json({'state':200,'data':selected_items,'info':''})
        except Exception,e:
            self.echo('mobile/member/info.html',{'info':'程序错误:' + traceback.format_exc()})

def selectGoods_format(self,drp_user_id):
    '''
    todo:商品格式化
    :return:
    '''
    item_service.set_rdb(self.rdb)
    query = item_service.get_drpTraderItems_by_user_id(drp_user_id)
    data = self.get_page_data(query,page_size=PAGE_SIZE)
    selected_items = []
    for item in data.result:
        selected_items.append({'id':item.item_id,
                               'show_id':item.show_id,
                               'title':item.title,
                               'price':item.item_price,
                               'inner_price':item.item_price,
                               'main_pic':item.main_pic and item.main_pic.split(';')[0] or '',
                               'issoldOut':item.sale_quantity<=item.warning_quantity and 1 or 0
                             })
    return selected_items