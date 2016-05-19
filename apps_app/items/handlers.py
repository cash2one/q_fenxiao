#encoding:utf-8
__author__ = 'wangjinkuan'

from services.item.item_services import ItemService
from services.sites.nav_services import NavServices
from services.item.brand_service import BrandService
from apps_app.common_handler import CommonHandler
from models.item_do import ItemCategory
from bs4 import BeautifulSoup
import sys

PAGE_SIZE = 4
item_service = ItemService()
nav_service = NavServices()
brand_service = BrandService()

class APPItemsListHandler(CommonHandler):
    def get(self,category_id,*args, **kwargs):
        user = self.get_current_user()
        is_bussiness = False if not user else user.get('is_bussiness')
        items,has_next = items_format(self,category_id,is_bussiness,'app')
        parent_id = self.rdb.query(ItemCategory.parent_id).filter(ItemCategory.deleted==0,ItemCategory.id==category_id).scalar()
        if parent_id == '0':
            query = item_service._children(category_id)
            top_category_id = category_id
        else:
            query = item_service._children(parent_id)
            top_category_id = parent_id
        category_names = [{'id':category.id,'name':category.name} for category in query]
        self.write_json({'stat':200,
                         'data':{'items':items,
                                 'has_next':has_next,
                                 'category_names':category_names,
                                 'top_category_id':top_category_id
                                },
                         'info':''
                        })

class AppCategoryHandler(CommonHandler):
    def get(self, *args, **kwargs):
        nav_service.set_rdb(self.rdb)
        item_service.set_rdb(self.rdb)
        top_categories = nav_service.query_all(is_app_start=1)
        lst_categories =[]
        for tc in top_categories:
            lst_children_categories = []
            for c in item_service._children(tc.category_id):
                    lst_children_categories.append({'id':c.id,'name':c.name})
            lst_categories.append({'top_name':tc.name,'children':lst_children_categories})
        self.write_json({'stat':200,'data':lst_categories,'info':''})

class ItemsDetailHandler(CommonHandler):
    def get(self,item_id, *args, **kwargs):
        # user = self.get_current_user()
        item_service.set_rdb(self.rdb)
        item = item_service.get_by_id(item_id)
        if self.request.uri.startswith('/h5'):
            result = item.content.replace('<br />','').replace('\n','').replace(' &nbsp;','').replace('<br/>','').replace('<br>','').replace('\t','').replace('\r','').replace('\'','\\\'')
            soup = BeautifulSoup(result)
            result = unicode(soup)
            self.echo('h5/items/detail.html',{'item':item,'content':result,'cart_count':0}) #,'is_bussiness':False if not user else user.get('is_bussiness')
        else:
            try:
                # price = item.price
                # if user.get('is_bussiness') and item.bussiness_price and item.bussiness_price>0:
                #     price = item.bussiness_price
                self.write_json({'stat':200,
                                 'data':{
                                         'id':item.id,
                                         'img':item.main_pic.split(';')[0],
                                         'title':item.title,
                                         'price':item.price,
                                         'inner_price':item.inner_price,
                                         'tax_rate':item.tax_rate,
                                         'cart_count':0,
                                         'is_abroad':item.is_abroad,
                                         'min_limit_quantity':item.min_limit_quantity,
                                         'max_limit_quantity':item.max_limit_quantity,
                                         'quantity_stat':item.sale_quantity <= item.warning_quantity and '库存不足' or '库存充足',
                                        }
                                })
            except Exception,e:
                self.captureException(sys.exc_info())

def items_format(self,category_id,is_bussiness,type=None):
    '''
    todo:根据类目得到格式化items数据
    :param category_id:
    :return:
    '''
    item_service.set_rdb(self.rdb)
    query = item_service._list(is_online=True,category_id=category_id,order_by='sort desc')
    data = self.get_page_data(query,page_size=PAGE_SIZE)
    items = []
    for item in data.result:
        dict = self.obj_to_dict(item,['id','title','inner_price','price','main_pic','bussiness_price'])
        dict['main_pic'] = dict.get('main_pic').split(';')[0]
        dict['is_bussiness'] = is_bussiness
        items.append(dict)
    page = data.page
    has_next = data.page_num-page > 0 and 1 or 0
    return items,has_next
