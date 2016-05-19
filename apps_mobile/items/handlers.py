#encoding:utf-8
__author__ = 'wangjinkuan'

from services.item.item_services import ItemService
from services.sites.nav_services import NavServices
from services.item.brand_service import BrandService
from apps_mobile.common_handler import CommonHandler
from models.item_do import ItemCategory
import ujson
from bs4 import BeautifulSoup

PAGE_SIZE = 4
item_service = ItemService()
nav_service = NavServices()
brand_service = BrandService()

class ItemListHandler(CommonHandler):

    def get(self,show_id):
        category_id = self.get_id_by_show_id(show_id)
        nav_service.set_rdb(self.rdb)
        category_name = self.rdb.query(ItemCategory.name).filter(ItemCategory.id==category_id).scalar()
        categories = nav_service.query_all()
        data = {'category_id':category_id,'nav_sites':categories,'category_name':category_name}
        self.echo('mobile/item/list.html',data)


class ItemsAsyncHandler(CommonHandler):

    def get(self): #page作为参数传来
        drp_user_id = self.get_drp_user_id()
        category_id = self.get_argument('category_id','')
        items,has_next = items_format(self,drp_user_id,category_id)
        self.write_json({'state':200,
                         'data':{'items':items,
                                 'has_next':has_next
                                },
                         'info':''
                        })

def items_format(self,drp_user_id,category_id):
    '''
    todo:根据类目得到格式化items数据
    :param category_id:
    :return:
    '''
    item_service.set_rdb(self.rdb)
    query = item_service.get_drpTraderItems_by_user_id(drp_user_id,category_id)
    data = self.get_page_data(query,page_size=PAGE_SIZE)
    items = []
    for item in data.result:
        items.append({'id':item.item_id,
                       'show_id':item.show_id,
                       'title':item.title,
                       'price':item.item_price,
                       'inner_price':item.item_price,
                       'main_pic':item.main_pic.split(';')[0],
                       'issoldOut':item.sale_quantity<=item.warning_quantity and 1 or 0
                     })
    page = data.page
    has_next = data.page_num-page > 0 and 1 or 0
    return items,has_next

from models.item_do import ItemDetail

class ItemsDetailHandler(CommonHandler):

    def get(self,show_id, *args, **kwargs):
        try:
            item_id = self.get_id_by_show_id(show_id)
            item_service.set_rdb(self.rdb)
            item = self.rdb.query(ItemDetail).filter(ItemDetail.deleted==0,ItemDetail.id==item_id).scalar()
            drp_user_id = self.get_drp_user_id()
            drp_trade_item = item_service.get_drpTraderItems_by_id(drp_user_id,item_id)
            item.price = drp_trade_item.item_price

            item_carts = self.get_cookie('fenxiao_item_carts')
            cart_count=0

            if item_carts:
                carts = ujson.loads(item_carts)
                cart_count = sum([int(c.get('item_num')) for c in carts])

            result = item.content.replace('<br />','').replace('\n','').replace(' &nbsp;','').replace('<br/>','').replace('<br>','').replace('\t','').replace('\r','').replace('\'','\\\'')
            soup = BeautifulSoup(result)
            result = unicode(soup)
            # share_url = 'http://'+self.request.host+self.request.uri
            # dic_sign= self.share_weixin(share_url)
            # dic_sign.update({'title':'今天在传说中最靠谱的全球抢购海淘发现了一件不错的东东','url':share_url,'img':item.main_pic.split(';')[0],'desc':item.summary})

            self.echo('mobile/item/detail.html',{'item':item,
                                                 'content':result,
                                                 'cart_count':cart_count,
                                                 'dic_sign':{},
                                                })

        except Exception,e:
            self.write_json({'stat':400,'info':e.message})

