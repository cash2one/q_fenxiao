#encoding:utf-8
__author__ = 'wangjinkuan'

from common.base_handler import AdminBaseHandler
from apps_admin.common_handler import CommonHandler
from services.item.item_services import ItemService
from models.item_do import ItemCategory
import ujson
import sys
import re

item_service = ItemService()

class CategoryHandler(CommonHandler):
    def get(self, *args, **kwargs):
        '''
        todo:获取所有商品分类树
        :param args:
        :param kwargs:
        :return:
        '''
        item_service.set_rdb(self.rdb)
        self.get_paras_dict()
        try:
            parent_id = self.qdict.get('id')
            if parent_id:
                item_category = item_service._children(parent_id)
            else:
                item_category = item_service._children('0')
            zNodes = []
            for ic in item_category:
                data = {}
                data['id'] = ic.id
                data['pId'] =ic.parent_id
                data['name'] = ic.name
                if item_service._children(ic.id).count()>0:
                    data['isParent'] = True
                else:
                    data['isParent'] = False
                zNodes.append(data)

            self.write_json(zNodes)

        except Exception,e:
            print e.message

            self.write_json({'stat':'n','info':e.message})
            # self.captureMessage(sys.exc_info())

    def put(self, *args, **kwargs):
        '''
        todo:创建商品分类 & 更改showid
        :param args:
        :param kwargs:
        :return:
        '''
        item_service.set_db(self.db)
        self.get_paras_dict()
        try:
            ic = item_service.create_item_category(**self.qdict)
            self.write(ujson.dumps({'stat':'ok','id':ic.id}))
        except Exception,e:
            self.captureMessage(sys.exc_info())

    def post(self, *args, **kwargs):
        '''
        todo:更新商品分类
        :param args:
        :param kwargs:
        :return:
        '''
        item_service.set_db(self.db)
        self.get_paras_dict()

        ic_id = self.qdict.get('id')
        self.qdict.pop('id')
        try:
            item_service.update_item_category(ic_id,**self.qdict)
        except Exception,e:
            self.captureMessage(sys.exc_info())
        self.write(ujson.dumps({'stat':'ok','info':'','data':{}}))

    def delete(self, *args, **kwargs):
        '''
        todo:删除商品分类
        :param args:
        :param kwargs:
        :return:
        '''
        self.post()

class TreeHandler(CommonHandler):

    def set_default_headers(self):
        self.set_header("X-XSRFToken",self.xsrf_token)

    def post(self,operation=None):
        '''
        todo:所有父级分类元素，根据父级元素查询下级元素
        :return:
        '''
        parent_id = self.get_argument('id',None)
        item_service.set_rdb(self.rdb)
        data=[]

        if parent_id:
            categories = item_service._children(parent_id)
        else:
            if operation == 'list':
                data.append({'isParent':False,'id':'','name':u'全部'})
            categories = item_service.query_by_level(1)
        for c in categories:
            t={}
            t['id'] = int(c.id)
            t['name'] = c.name
            if item_service._children(c.id).count()>0:
                t['isParent'] = True
            else:
                t['isParent'] = False
            data.append(t)
        self.write_json(data)

class ItemCategorySearchHandler(CommonHandler):
    def get(self):
        item_service.set_rdb(self.rdb)
        self.get_paras_dict()
        search = self.qdict.get('term')
        item_category = item_service.query_item_category(category_name=search)
        zNodes = []
        for ic in item_category:
            data = {}
            data['id'] = ic.id
            data['label'] = ic.name
            data['value'] = ic.name
            zNodes.append(data)
        self.write_json(zNodes)

class ItemCategoryHandler(CommonHandler):
    def get(self,operation=None):
        type = self.get_argument('type','')
        categories = self.rdb.query(ItemCategory).filter(ItemCategory.deleted == 0,ItemCategory.parent_id=='0')
        if operation == 'add':
            self.echo('admin/item/add.html',{'type':type,'item_category':'','categories':categories})
        elif operation == 'edit':
            category_id = self.get_argument('category_id','')
            item_category = self.rdb.query(ItemCategory).filter(ItemCategory.deleted == 0,ItemCategory.id == category_id).scalar()
            self.echo('admin/item/add.html',{'item_category':item_category,'type':type,'categories':categories})
        else:
             item_service.set_rdb(self.rdb)
             category_name = self.get_argument('category_name','')
             query = item_service.query_item_category(category_name=category_name)
             data = self.get_page_data(query)
             self.echo('admin/item/item.html',{'data':data,'category_name':category_name})

    def post(self,operation=None):
        item_service.set_db(self.db)
        self.get_paras_dict()
        if operation == 'add':
            ic = item_service.create_item_category(**self.qdict)
        elif operation == 'edit':
            category_id = self.qdict.get('category_id')
            type = self.qdict.get('type')
            full_parent_id = self.qdict.get('full_parent_id')
            if type == 'children':
                self.qdict['full_parent_id'] = full_parent_id.replace(re.findall(r'\d+',full_parent_id)[0],self.qdict.get('parent_id'),1)
            self.qdict.pop('category_id')
            self.qdict.pop('type')
            item_service.update_item_category(category_id,**self.qdict)
            self.delete_category_name(category_id)
        self.write_json({'state':200,'data':'','info':''})