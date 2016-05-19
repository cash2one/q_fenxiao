#encoding:utf-8
__author__ = 'wangjinkuan'

from services.base_services import BaseService
from models.item_do import ItemAttribute,ItemAttributeValue,ItemSKU,ItemAttributeFilter

class AttributesService(BaseService):

    def _add_attribute(self,attribute_name,is_filter,is_sku,is_multi_select,status,sort,attribute_desc,category_id,attribute_values,attribute_id):
        '''
        todo:添加商品属性
        :return:
        '''
        if attribute_id:
            item_attribute = self.db.query(ItemAttribute).filter(ItemAttribute.deleted==0,ItemAttribute.id==attribute_id).scalar()
        else:
            item_attribute = ItemAttribute()
        item_attribute.category_id = category_id
        item_attribute.attribute_name = attribute_name
        item_attribute.is_filter = is_filter
        item_attribute.is_sku = is_sku
        item_attribute.is_multi_select = is_multi_select
        item_attribute.status = status
        item_attribute.paixu = sort
        print 'paixu:',sort
        item_attribute.attribute_desc = attribute_desc
        self.db.add(item_attribute)
        self.db.commit()
        if not attribute_id:
            for value in attribute_values.split(' '):
                self._add_attribute_value(status,attribute_id=item_attribute.id,
                                          attribute_name=item_attribute.attribute_name,value=value,paixu=1)

    def _add_attribute_value(self,status,attribute_id=None,attribute_name=None,value=None,paixu=None,attribute_v_id=None):
        '''
        todo:添加属性
        :param attribute_id:
        :param attribute_name:
        :param attribute_value:
        :param status:
        :param paixu:
        :return:
        '''
        attribute_v = self.db.query(ItemAttributeValue).filter(ItemAttributeValue.deleted==0,ItemAttributeValue.id==attribute_v_id).scalar()
        if not attribute_v:
            attribute_v = ItemAttributeValue()
            attribute_v.attribute_id = attribute_id
            attribute_v.attribute_name = attribute_name
            attribute_v.attribute_value = value
        attribute_v.paixu = paixu
        attribute_v.status = status
        self.db.add(attribute_v)
        self.db.commit()


    def _list_attribute(self,**kwargs):
        '''
        todo:获取属性list
        :param kwargs:
        :return:
        '''
        query = self.rdb.query(ItemAttribute).filter(ItemAttribute.deleted==0)
        if kwargs.get('category_id'):
            query = query.filter(ItemAttribute.category_id == kwargs.get('category_id'))
        return query

    def get_item_attribute_filters(self,attribute_value_id,attribute_id,item_ids):
        '''
        查询属性
        :param attribute_value_id:
        :param attribute_id:
        :return:
        '''
        query = self.rdb.query(ItemAttributeFilter.item_id).filter(ItemAttributeFilter.is_sku==0,
                                                           ItemAttributeFilter.attribute_value_id==attribute_value_id,
                                                           ItemAttributeFilter.attribute_id==attribute_id)
        if item_ids:
            query = query.filter(ItemAttributeFilter.item_id.in_(item_ids))

        return query

    def get_attribute_by_id(self,attribute_id):
        '''
        todo:根据ID获取属性
        :param attribute_id:
        :return:
        '''
        return self.rdb.query(ItemAttribute).filter(ItemAttribute.deleted==0,ItemAttribute.id==attribute_id).scalar()

    def _list_attribute_value(self,attribute_id):
        '''
        todo:获取属性value值
        :param attribute_id:
        :return:
        '''
        query = self.rdb.query(ItemAttributeValue).filter(ItemAttributeValue.deleted==0,ItemAttributeValue.attribute_id==attribute_id)
        return query

    def get_attribute_value_by_id(self,attribute_v_id):
        '''
        todo:获取属性值
        :param attribute_v_id:
        :return:
        '''
        return self.rdb.query(ItemAttributeValue).filter(ItemAttributeValue.deleted==0,ItemAttributeValue.attribute_id==attribute_v_id)

    def get_attrValue_by_id(self,attribute_v_id):
        '''
        todo:
        :param attribute_v_id:
        :return:
        '''
        return self.rdb.query(ItemAttributeValue).filter(ItemAttributeValue.deleted==0,ItemAttributeValue.id==attribute_v_id).scalar()

    # def _update_attribute_value(self,attribute_id,attribute_name,attribute_value,status,paixu,attribute_v_id=None):
    #     '''
    #     todo:更新属性值
    #     :param attribute_v_id:
    #     :param kwargs:
    #     :return:
    #     '''
    #     attribute_v = self.db.query(ItemAttributeValue).filter(ItemAttributeValue.deleted==0,ItemAttributeValue.id==attribute_v_id).scalar()
    #     attribute_v.attribute_id = attribute_id
    #     attribute_v.attribute_value = attribute_value
    #     attribute_v.attribute_name = attribute_name
    #     attribute_v.paixu = paixu
    #     attribute_v.status = status
    #     self.db.add(attribute_v)
    #     self.db.commit()

    def get_attribute_by_category_id(self,category_id):
        '''
        todo:获取类目下所有属性
        :param category_id:
        :return:
        '''
        return self.rdb.query(ItemAttribute).filter(ItemAttribute.deleted==0,ItemAttribute.category_id==category_id,ItemAttribute.status==1)

    def get_attribute_value(self,attribute_id):
        '''
        todo:获取属性下所有属性值
        :param attribute_id:
        :return:
        '''
        return self.rdb.query(ItemAttributeValue).filter(ItemAttributeValue.deleted==0,
                                                         ItemAttributeValue.attribute_id==attribute_id,
                                                         ItemAttributeValue.status==1)

    def _add_item_sku(self,item,attribute_name_id_list,attribute_value_id_list,attribute_name_list,attribute_value_list):
        '''
        todo:添加商品sku
        :param item:
        :param attribute_list:
        :param attribute_name:
        :param item_sku_id:
        :return:
        '''

        item_sku = self.db.query(ItemSKU).filter(ItemSKU.deleted==0,
                                                 ItemSKU.item_id==item.id,
                                                 ItemSKU.attribute_name_id_list==attribute_name_id_list,
                                                 ItemSKU.attribute_value_id_list==attribute_value_id_list).scalar() #判断同一种商品是否有相同的sku
        if item_sku:
            return '该商品已有   '+attribute_name_list+':'+attribute_value_list+'   此sku组合,请选择其他sku组合'
        item_sku = ItemSKU()
        item_sku.item_id = item.id
        item_sku.item_name = item.name
        item_sku.attribute_name_id_list = attribute_name_id_list
        item_sku.attribute_value_id_list = attribute_value_id_list
        item_sku.attribute_name_list = attribute_name_list
        item_sku.attribute_value_list = attribute_value_list
        item_sku.item_price = item.price
        item_sku.inner_price = item.inner_price
        item_sku.orgin_price = item.orgin_price
        self.db.add(item_sku)
        self.db.flush()
        self._add_item_attribute_filter(item_id=item.id,sku_id=item_sku.id,is_sku=1)
        return '添加sku属性成功!'

    def _add_item_attribute_filter(self,item_id=None,attribute_id=None,attribute_value_id=None,is_sku=None,sku_id=None):
        '''
        todo:添加商品属性关系
        :param item_id:
        :param attribute_id:
        :param attribute_value_id:
        :param is_sku:
        :param sku_id:
        :return:
        '''
        if attribute_id and attribute_value_id:
            item_attribute_filter = self.db.query(ItemAttributeFilter).filter(ItemAttributeFilter.deleted==0,
                                                                              ItemAttributeFilter.attribute_id==attribute_id,
                                                                              ItemAttributeFilter.attribute_value_id==attribute_value_id,
                                                                              ItemAttributeFilter.is_sku==0).scalar()
            if not item_attribute_filter:
                item_attribute_filter = ItemAttributeFilter()
        else:
            item_attribute_filter = ItemAttributeFilter()
        item_attribute_filter.item_id = item_id
        item_attribute_filter.attribute_id = attribute_id
        item_attribute_filter.attribute_value_id = attribute_value_id
        item_attribute_filter.is_sku = is_sku
        item_attribute_filter.sku_id = sku_id
        self.db.add(item_attribute_filter)
        self.db.commit()
        return '添加查询属性成功'

    def _list_item_attribute(self,item_id,attribute_type):
        '''
        todo:获取sku列表
        :param item_id:
        :return:
        '''
        if attribute_type == 'sku':
            query = self.rdb.query(ItemSKU.id,ItemSKU.attribute_name_list,
                                   ItemSKU.attribute_value_list,
                                   ItemSKU.item_count,
                                   ItemSKU.sale_quantity,
                                   ItemSKU.warning_quantity).filter(ItemSKU.deleted==0,ItemSKU.item_id==item_id)
        elif attribute_type == 'filter':
            query = self.rdb.query(ItemAttributeFilter).filter(ItemAttributeFilter.deleted==0,ItemAttributeFilter.item_id==item_id,ItemAttributeFilter.is_sku==0)
        return query

    def _update_sku(self,sku_id,item_count,sale_quantity,warning_quantity):
        '''
        todo:更新sku库存
        :param sku_id:
        :param kwargs:
        :return:
        '''
        item_sku = self.db.query(ItemSKU).filter(ItemSKU.deleted==0,ItemSKU.id==sku_id).scalar()
        item_sku.item_count = item_count
        item_sku.sale_quantity = sale_quantity
        item_sku.warning_quantity = warning_quantity
        self.db.add(item_sku)
        self.db.commit()







