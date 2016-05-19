#encoding:utf-8
__author__ = 'binpo'
from ..base_handler import DrpBaseHandler
from services.locations.location_services import LocationServices
from services.item.item_services import ItemService
from services.orders.orders_services import OrderServices
from services.item.brand_service import BrandService
from services.merchant.merchant_services import MerchantService
from models.item_do import ItemDetail,ItemCategory
from conf.item_conf import DRP_ITEM_STATUS
import datetime
import sys


location_service = LocationServices()
item_service = ItemService()
order_service = OrderServices()
brand_service = BrandService()
merchant_services = MerchantService()

class ItemsHandler(DrpBaseHandler):
    def get(self, *args, **kwargs):
        self.get_paras_dict()
        status = self.qdict.get('status',None)
        is_drp_item = bool(self.qdict.get('is_drp_item',False))
        item_service.set_rdb(self.rdb)
        html_data = {}
        if is_drp_item:
            user_id = self.get_current_user().get('id')
            query = item_service.get_items_by_drp_id(user_id)
            html_data['count'] = query.count()
            url = 'admin_drp/items/drp_item_list.html'
        else:
            query = item_service.query_drp_sales_items(self.current_user.get('id'),status)
            url = 'admin_drp/items/item_list.html'
            html_data['DRP_ITEM_STATUS'] = DRP_ITEM_STATUS
        data = self.get_page_data(query)
        html_data['data'] = data
        self.echo(url,html_data)

    def post(self, *args, **kwargs):
        self.get_paras_dict()
        item_id = self.qdict.get('id')
        item_service.set_rdb(self.rdb)
        item = item_service.get_itemDetail_by_id(item_id)
        item_service.set_db(self.db)
        item_service._update_item_detail(item_id,is_online = self.qdict.get('is_online'))
        user_id = self.get_current_user().get('id')
        item_service._update_drpItem_by_id(user_id,item_id,status = self.qdict.get('is_online'))
        self.write_json({'stat':'success','info':''})

    def get_category_name_by_id(self,category_id):
        '''
        查询类目名称
        :param category_id:
        :return:
        '''
        return self.rdb.query(ItemCategory.name).filter(ItemCategory.id==category_id).scalar()

class ItemsOnlineHandler(DrpBaseHandler):
    def get(self,show_id,*args, **kwargs):
        self.get_paras_dict()
        item_id = self.get_id_by_show_id(show_id)
        item_service.set_rdb(self.rdb)
        query = item_service.query_drp_sales_items(self.current_user.get('id'),item_id=item_id)
        item = query[0]
        self.echo('admin_drp/items/add_item.html',{'item':item,'msg':self.qdict.get('msg','')})

    def post(self,show_id,*args, **kwargs):
        self.get_paras_dict()
        price = float(self.qdict.get('sale_price'))
        drp_item_id = self.qdict.get('drp_item_id')
        item_service.set_rdb(self.rdb)
        query = item_service.query_drp_sales_items(self.current_user.get('id'),drp_item_id=drp_item_id)
        item = query[0]
        #DrpTraderItems,ItemDetail
        #if item.DrpTraderItems.status==0:
        if item.ItemDetail.drp_max_price>=int(price)>=item.ItemDetail.drp_min_price:
            #_drp_item = item_service.
            item.DrpTraderItems.status=1
            item.DrpTraderItems.item_price=int(price)
            self.db.add(item.DrpTraderItems)
            self.db.commit()
            self.redirect(self.reverse_url('drp_items'))
        else:
             self.redirect(self.reverse_url('drp_item_online',item.ItemDetail.show_id)+'?msg=修改参数不正确')

class ItemCreatHandler(DrpBaseHandler):

    def get(self, operation,*args, **kwargs):
        item_service.set_rdb(self.rdb)
        units = item_service._list_unit()
        drp_user_id = self.get_current_user().get('id')
        if operation == 'edit':
            item_id = self.get_argument('item_id')
            item = item_service.get_itemDetail_by_id(item_id)
            self.echo('admin_drp/items/_add.html',{'item':item,'units':units,'drp_user_id':drp_user_id})
        else:

            self.echo('admin_drp/items/_add.html',{'item':'','units':units,'drp_user_id':drp_user_id})


    def post(self, operation,*args, **kwargs):
        self.get_paras_dict()
        drp_user_id = self.get_current_user().get('id')
        if self.qdict.get('is_online') == 'on':
            self.qdict['is_online'] = 1
            status = 1
        else:
            self.qdict['is_online'] = 0
            status = 0

        img_obj = self.qdict.get('imgs_url',None)
        if isinstance(img_obj,list):
            self.qdict['main_pic'] = ';'.join(img_obj)
        else:
            self.qdict['main_pic'] = img_obj

        item_service.set_db(self.db)
        if operation =='edit':
            item_id = self.get_argument('item_id')
            self.qdict.pop('item_id')
            self.qdict.pop('imgs_url')
            self.qdict.pop('_xsrf')
            item_service._update_item_detail(item_id,**self.qdict)
        else:
            self.qdict['is_drp_item'] = 1
            self.qdict['drp_user_id'] = drp_user_id
            item_id = item_service._add(**self.qdict)
            show_id = self.set_show_id_by_id(item_id)
            item_service.update_item_detail_show_id_by_id(item_id,show_id)

        item_service.add_drpTraderItems(item_id,drp_user_id,self.qdict.get('price'),status=status)
        self.write('<h1>添加成功<h1>')


