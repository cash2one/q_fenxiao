#encoding:utf-8
__author__ = 'gaoaifei'

from common.base_handler import AdminBaseHandler
from services.item.item_services import ItemService
from services.item.brand_service import BrandService
from conf.user_conf import USER_STATUS
import sys
import json
import ujson
from common.asyn_wrap import unblock

item_service = ItemService()
brand_service = BrandService()

class BrandHandler(AdminBaseHandler):
    def get(self, operation=None, *args, **kwargs):
        if operation=='add':
            self.echo('admin/brand/add.html',{
                'data':''
            })
        elif operation == 'edit':
            self.get_paras_dict()
            id = self.qdict.get('id','')
            brand_service.set_rdb(self.rdb)
            data = brand_service.get_brand_by_id(id)
            self.echo('admin/brand/add.html',{
                      'data':data,
            })
        elif operation == 'checkBrandName':
             self.get_paras_dict()
             category_id = self.qdict.get('category_id')
             brand_name = self.qdict.get('name')
             brand_service.set_rdb(self.rdb)
             data = brand_service.check_brand_name_is_exist(category_id,brand_name)
             if data:
                return json.dumps({"state":"200","info":"success"})
             else:
                return json.dumps({"state":"400","info":"success"})
        else:
            self.get_paras_dict()
            start_date = self.qdict.get('start_date','')
            end_date = self.qdict.get('end_date','')
            status = self.qdict.get('status','0')
            reorder = self.qdict.get('reorder','')
            name = self.qdict.get('name','')
            category_id = self.qdict.get('category_id','')
            category_name = self.qdict.get('category_name',u'全部')
            description = self.qdict.get('description','')
            item_service.set_rdb(self.rdb)
            category = item_service.query_item_category(**self.qdict)
            brand_service.set_rdb(self.rdb)

            query = brand_service._list(**self.qdict)
            data = self.get_page_data(query)
            self.echo('admin/brand/list.html',{
                'data':data,
                'category':category,
                'category_id':category_id,
                'category_name':category_name,
                'start_date':start_date,
                'end_date':end_date,
                'status':status,
                'reorder':reorder,
                'name':name,
                'description':description,
                'USER_STATUS':USER_STATUS,
            })

    def post(self, operation=None, *args, **kwargs):
           self.get_paras_dict()
           id = self.qdict.get('id')
           if  operation=='edit':
             brand_service.set_db(self.db)
             is_success = brand_service.update_brand_by_id(id, **self.qdict)
             if is_success:
                 self.redirect('/admin/brand/')
             # self.write('ok')
           else:
             brand_service.set_db(self.db)
             is_success = brand_service._add(**self.qdict)
             if is_success:
                 self.redirect('/admin/brand/')
             # self.echo('admin/brand/add.html',{'data':''})

    def get_category_name_by_id(self,category_id):
        '''
        todo:通过id获取商品类目
        :param category_id:
        :return:
        '''
        item_service.set_rdb(self.rdb)
        brand = item_service.get_category_name_by_id(category_id)
        brand_name = brand and brand.name or ''
        return brand_name

    def delete(self,operation=None, *args, **kwargs):
        self.get_paras_dict()
        id = self.qdict.get('id')
        if operation == 'renew':
            brand_service.set_db(self.db)
            brand_service.update_status_by_id(id)
            self.write_json({"state":"200","info":"success"})
        else:
            try:
                brand_service.set_db(self.db)
                brand_service.delete_by_id(id)
                self.write_json({'state':'200','info':'success'})
            except Exception,e:
                self.captureException(sys.exc_info())
                self.write_json({'state':'400','info':e.message})

class CategoryBrandHandler(AdminBaseHandler):
    def get(self, *args, **kwargs):
        brand_service.set_rdb(self.rdb)
        try:
            category_id = self.get_argument('category_id','')
            query = brand_service._list(category_id=category_id)
            brands = [{'brand_id':brand.id,'brand_name':brand.name} for brand in query]
            self.write_json({'stat':'success','data':brands,'info':''})
        except Exception,e:
            print e.message

