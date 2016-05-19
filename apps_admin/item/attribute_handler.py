#encoding:utf-8
__author__ = 'wangjinkuan'

from apps_admin.common_handler import CommonHandler
from services.attributes.attributes_service import AttributesService
from models.item_do import ItemAttribute,ItemDetail,ItemSKU,ItemAttributeValue
import collections

attribute_service = AttributesService()

class ProductAttributeHandler(CommonHandler):
    def get(self,item_id,category_id,type):
        attribute_service.set_rdb(self.rdb)
        query = attribute_service.get_attribute_by_category_id(category_id)
        dict = collections.OrderedDict()
        if type == 'sku':
            for attribute in query.filter(ItemAttribute.is_sku==1):
                values = []
                for attribute_value in attribute_service.get_attribute_value(attribute.id):
                    values.append(attribute_value)
                dict[attribute] = values
            if dict:
                self.echo('admin/items/_add_sku_attribute.html',{'dict':dict})
            else:
                self.write('该商品没有sku属性')
        else:
            for attribute in query.filter(ItemAttribute.is_filter==1):
                values = []
                for attribute_value in attribute_service.get_attribute_value(attribute.id):
                    values.append(attribute_value)
                dict[attribute] = values
            if dict:
                self.echo('admin/items/_add_filter_attribute.html',{'dict':dict})
            else:
                self.write('该商品没有查询属性')

    def post(self,item_id,category_id,type):
        attribute_service.set_db(self.db)
        self.get_paras_dict()
        item = self.rdb.query(ItemDetail).filter(ItemDetail.deleted==0,ItemDetail.id==item_id).scalar()
        if type == 'sku':
            info = attribute_service._add_item_sku(item,
                                            self.qdict.get('attribute_ids'),
                                            self.qdict.get('attribute_value_ids'),
                                            self.qdict.get('attribute_names'),
                                            self.qdict.get('attribute_values'))

        else: #查询属性
            for key in self.qdict:
                info = attribute_service._add_item_attribute_filter(item_id=item.id,
                                                             attribute_id=key,
                                                             attribute_value_id=self.qdict.get(key),
                                                             is_sku=0)
        self.write(info)

class ListAttributeHandler(CommonHandler):
    def get(self,operation,*args, **kwargs):
        if operation == 'item_count':
            sku_id = self.get_argument('sku_id','')
            item_sku = self.rdb.query(ItemSKU).filter(ItemSKU.deleted==0,ItemSKU.id==sku_id).scalar()
            self.echo('admin/attributes/item_count.html',{'sku_id':sku_id,'item_sku':item_sku,'is_sku':1})
        else:
            attribute_service.set_rdb(self.rdb)
            attribute_type = self.get_argument('attribute_type','sku')
            item_id = self.get_argument('item_id')
            item_name = self.get_argument('item_name')
            item_price = self.get_argument('item_price')
            query = attribute_service._list_item_attribute(item_id,attribute_type)
            attributes = self.get_page_data(query)
            self.echo('admin/items/attribute_list.html',{'data':attributes,
                                                         'attribute_type':attribute_type,
                                                         'item_id':item_id,
                                                         'item_name':item_name,
                                                         'item_price':item_price
                                                        })
    def post(self,operation,*args, **kwargs):
        if operation == 'item_count':
            self.get_paras_dict()
            attribute_service.set_db(self.db)
            attribute_service._update_sku(self.qdict.get('sku_id'),
                                          self.qdict.get('item_count'),
                                          self.qdict.get('sale_quantity'),
                                          self.qdict.get('warning_quantity'))
            self.write('更新库存成功')

    def get_attribute_value(self,attribute_id,attribute_value_id):
        '''
        todo:获取属性值或者属性value
        :param type:
        :param attribute_id:
        :return:
        '''
        attribute_value = self.rdb.query(ItemAttributeValue).\
            filter(ItemAttributeValue.deleted==0,ItemAttributeValue.attribute_id==attribute_id,ItemAttributeValue.id==attribute_value_id).scalar()
        return attribute_value.attribute_name,attribute_value.attribute_value