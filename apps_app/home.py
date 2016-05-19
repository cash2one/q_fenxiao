#encoding:utf-8
__author__ = 'wangjinkuan'

from apps_app.common_handler import CommonHandler
from services.item.item_services import ItemService

item_service = ItemService()
PAGE_SIZE=4

class HomeHandler(CommonHandler):

    def get(self, *args, **kwargs):
        user = self.get_current_user()
        banners = self.get_banner('app_banner')
        category_banners = self.get_banner('app_category')
        is_bussiness = False if not user else user.get('is_bussiness')
        selected_items = selectGoods_format(self,is_bussiness)
        self.write_json({'stat':200,
                         'data':{'categorys':category_banners,
                                 'banners':banners,
                                 'select_goods':selected_items
                                },
                         'info':''
                        })

def selectGoods_format(self,is_bussiness):
    '''
    todo:最新商品格式化
    :return:
    '''
    item_service.set_rdb(self.rdb)
    query = item_service.get_last_items_by_category_id(3,order_by='gmt_modified desc,sale_quantity desc')
    new_items = self.get_page_data(query,page_size=PAGE_SIZE)
    selected_items = []
    for item in new_items.result:
        dict = self.obj_to_dict(item,['id','title','inner_price','price','main_pic','bussiness_price'])
        dict['main_pic'] = dict.get('main_pic').split(';')[0]
        dict['is_bussiness'] = is_bussiness
        selected_items.append(dict)
    return selected_items