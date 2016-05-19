#encoding:utf-8
__author__ = 'wangjinkuan'

from models.item_do import ItemCategory

class ItemsBase(object):

    def get_category_name_by_id(self,category_id):
        '''
        查询类目名称
        :param category_id:
        :return:
        '''
        return self.rdb.query(ItemCategory.name).filter(ItemCategory.id==category_id).scalar()
