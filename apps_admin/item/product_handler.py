#encoding:utf-8
__author__ = 'binpo'

from common.base_handler import AdminBaseHandler
from apps_admin.common_handler import CommonHandler
from services.locations.location_services import LocationServices
from services.item.item_services import ItemService
from services.orders.orders_services import OrderServices
from services.item.brand_service import BrandService
from services.merchant.merchant_services import MerchantService
from services.distributor.distributor_service import DistributorUserservice
from services.users.user_services import UserServices
from models.item_do import ItemDetail
from conf.item_conf import IS_ABROAD
import datetime
import sys

from ..item import ItemsBase


location_service = LocationServices()
item_service = ItemService()
order_service = OrderServices()
brand_service = BrandService()
merchant_services = MerchantService()
distributor_services = DistributorUserservice()
user_services = UserServices()

class ItemsHandler(CommonHandler):
    def get(self,operation=None,*args, **kwargs):
        item_service.set_rdb(self.rdb)
        brand_service.set_rdb(self.rdb)
        order_service.set_rdb(self.rdb)
        vendors = UserServices(rdb=self.rdb).get_vendors()
        distributor_services.set_rdb(self.rdb)
        distributors =  distributor_services.get_all_distributor_users(type=0)
        if operation=='add': #新增商品
            units = item_service._list_unit()
            brands = brand_service._list()
            self.echo('admin/items/add_item.html',
                      {
                       'item':'',
                       'units':units,
                       'brands':brands,
                       'vendors':vendors,
                       'distributors':distributors
                      })
        elif operation == 'edit':#商品编辑
            self.get_paras_dict()
            units = item_service._list_unit()
            item = item_service.get_itemDetail_by_id(self.qdict.get('id'))
            brands = brand_service._list(category_id=item.category_id)
            distributor_services.set_rdb(self.rdb)
            distributors =  distributor_services.get_all_distributor_users()
            item_service.set_rdb(self.rdb)
            distributorItems = item_service.get_distributors_by_item_id(self.qdict.get('id'))

            self.echo('admin/items/add_item.html',
                      {'item':item,
                       'item_service':item_service,
                       'units':units,
                       'brands':brands,
                       'vendors':vendors,
                       'distributors':distributors,
                       'distributorItems':distributorItems
                      })
        elif operation == 'product_quantity': #库存
            item_id = self.get_argument('id')
            item = self.rdb.query(ItemDetail).filter(ItemDetail.deleted==0,ItemDetail.id==item_id).scalar()
            if self.request.uri.startswith('/admin/mobile'):
                self.echo('admin/mobile/items/item_count.html',{'item':item,'is_sku':0},layout='')
            else:
                self.echo('admin/items/item_count.html',{'item':item,'is_sku':0})
        else:
            is_drp_item = int(self.get_argument('is_drp_item',0))
            is_online = self.get_argument('is_online','')
            category_name = self.get_argument('category_name',u'全部')
            category_id = self.get_argument('category_id','')
            content = self.get_argument('content','')
            is_ab = self.get_argument('is_abroad','')
            query = item_service.query_items_detail(is_online=is_online,
                                                    category_id=category_id,
                                                    content=content,
                                                    is_abroad=is_ab,
                                                    is_drp_item=is_drp_item)
            data = self.get_page_data(query)
            html_data = {'data':data,
                         'content':content,
                         'is_online':is_online,
                         'category_name':category_name,
                         'category_id':category_id,
                         'IS_ABROAD':IS_ABROAD,
                         'is_ab':is_ab,
                         'count':query.count()
                        }
            if is_drp_item:

                self.echo('admin/items/drp_item_list.html',html_data)
            else:
                self.echo('admin/items/item_list.html',html_data)

    def get_drp_by_id(self,id):
        '''
        todo
        :param id:
        :return:
        '''
        distributor_services.set_rdb(self.rdb)
        distributor_user = distributor_services.get_distributor_by_id(id)
        return distributor_user.user_name

    def post(self,operation=None,*args, **kwargs):
        self.get_paras_dict()
        item_id = self.qdict.get('id')
        # try:
        if operation == 'edit':
            item_service.set_rdb(self.rdb)
            item_category = item_service.query_item_category(category_id=self.qdict.get('category_id')).scalar()
            top_category_id = item_category.full_parent_id.split('/')[1]
            self.qdict['top_category_id'] = top_category_id
            if self.qdict.get('is_online') == 'on':
                self.qdict['is_online'] = 1
            else:
                self.qdict['is_online'] = 0

            img_obj = self.qdict.get('imgs_url',None)
            if isinstance(img_obj,list):
                self.qdict['main_pic'] = ';'.join(img_obj)
            else:
                self.qdict['main_pic'] = img_obj

            if 'item_imgs' in self.qdict:
                self.qdict.pop('item_imgs')
            if 'imgs_url' in self.qdict:
                self.qdict.pop('imgs_url')

            self.qdict['gmt_modified'] = datetime.datetime.now()
            self.qdict.pop('_xsrf')
            # 更改分销商关系表
            drp_trader_ids = self.qdict.get('distributor_id')
            item_price = '0.00'
            item_service.set_db(self.db)
            if drp_trader_ids:
                exist_drp_ids = [ str(e_drp_id[0]) for e_drp_id in item_service.get_exist_drp_ids(item_id).all()]
                new_drp_ids = [drp_id for drp_id in drp_trader_ids if drp_id not in exist_drp_ids]
                delete_drp_ids = [ex_drp_id for ex_drp_id in exist_drp_ids if ex_drp_id not in drp_trader_ids]

                if new_drp_ids:
                    for n_drp_id in new_drp_ids:
                        item_service.add_drpTraderItems(item_id,n_drp_id,item_price,status=0)

                if delete_drp_ids:
                    for d_drp_id in delete_drp_ids:
                        item_service.delete_drp_id(d_drp_id,item_id)
                        
            self.qdict.pop('distributor_id')
            item_service._update_item_detail(item_id,**self.qdict)

            self.write('<h1>更新成功</h1>')

        elif operation == 'online':
            self.qdict.pop('id')
            item_service.set_db(self.db)
            item_service._update_item_detail(item_id,**self.qdict)
            self.write_json({'stat':'success','info':''})

        elif operation == 'product_quantity':
            item_no = self.qdict.get('item_no')
            quantity = self.qdict.get('quantity',0)
            sale_quantity = self.qdict.get('sale_quantity',0)
            warning_quantity = self.qdict.get('warning_quantity',0)
            item_service.set_db(self.db)

            item_service._update_item_detail(
                                             item_id=int(item_id),
                                             item_no=item_no,
                                             quantity=int(quantity),
                                             sale_quantity=int(sale_quantity),
                                             warning_quantity=int(warning_quantity)
                                            )
            self.write('<h1>更新成功</h1>')
        else:
            item_service.set_db(self.db)
            if self.qdict.get('is_online') == 'on':
                self.qdict['is_online'] = 1
            else:
                self.qdict['is_online'] = 0
            # 商品表插入数据
            item_id = item_service._add(**self.qdict)
            show_id = self.set_show_id_by_id(item_id)
            item_service.update_item_detail_show_id_by_id(item_id,show_id)
            # 分销商关系表
            drp_trader_ids = self.qdict.get('distributor_id')
            item_price = self.qdict.get('item_price')
            for drp_trader_id in drp_trader_ids:
                item_service.add_drpTraderItems(item_id,drp_trader_id,item_price,status=0)
            self.write('<h1>添加成功</h1>')

        # except Exception,e:
            # self.captureMessage(sys.exc_info())
            # self.write_json({'stat':'n','info':e.message})

    # def delete(self,item_id,*args, **kwargs):
    #     try:
    #         item_service.set_db(self.db)
    #         item_service._delete(item_id)
    #         self.write_json({'state':200,'info':'删除成功'})
    #     except Exception,e:
    #         self.write_json({'state':400,'info':e.message})

class ItemsAjaxHandler(AdminBaseHandler,ItemsBase):

    def get(self, *args, **kwargs):
        self.get_paras_dict()
        item_service.set_rdb(self.rdb)
        query = item_service._list(**self.qdict)
        data = self.get_page_data(query)
        content = self.render('admin/items/items_table.html',{'data':data})
        self.write(content)

class ItemsSearchHandler(AdminBaseHandler,ItemsBase):

    def get(self, *args, **kwargs):
        search = self.get_argument('term','')
        if not search.strip():
            self.write_json([])
        else:
            item_service.set_rdb(self.rdb)
            items = item_service.items_like_search(search)
            self.write_json([{'id':item.id,'label':item.title,'value':item.title}for item in items])