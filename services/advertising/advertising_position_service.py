#encoding:utf-8

__author__ = 'gaoaifei'

from services.base_services import BaseService
from models.advertise import *

class AdvertisingPositionService(BaseService):
    def _list(self,**qdict):
        """
        :todo 查询用户
        :param qdict 请求参数集合
        """
        if qdict.get('status')=='1':
            query = self.rdb.query(AdvertisingPosition).filter(AdvertisingPosition.deleted == 1)
        else:
            query = self.rdb.query(AdvertisingPosition).filter(AdvertisingPosition.deleted == 0)
        if qdict.get('start_date',''):
            query = query.filter(AdvertisingPosition.gmt_created >= qdict.get('start_date') + ' 00:00:00')
        if qdict.get('end_date',''):
           query = query.filter(AdvertisingPosition.gmt_created <= qdict.get('end_date') + ' 23:59:59')
        if qdict.get('description',''):
            query = query.filter(AdvertisingPosition.description.like('%'+qdict.get('description')+'%'))
        if qdict.get('name',''):
            query = query.filter(AdvertisingPosition.name == qdict.get('name'))
        if qdict.get('code_name',''):
            query = query.filter(AdvertisingPosition.code_name == qdict.get('code_name'))
        if qdict.get('reorder') == 'asc':
            query = query.order_by(AdvertisingPosition.gmt_created.asc())
        else:
            query = query.order_by(AdvertisingPosition.gmt_created.desc())
        return query

    def _add(self,**qdict):
        '''
        添加广告位
        :param qdict:
        :return:
        '''
        brand = AdvertisingPosition()
        brand.name = qdict.get('name')
        brand.code_name = qdict.get('code_name')
        brand.description = qdict.get('description')
        brand.width = int(qdict.get('width'))
        brand.height = int(qdict.get('height'))
        if qdict.get('category_id'):
            brand.category_id = int(qdict.get('category_id'))
        else:
            brand.category_id = 0
        self.db.add(brand)
        self.db.commit()
        return True

    def update_position_by_id(self,position_id,**qdict):
        '''
        更新
        :param qdict: id
        :return:
        '''
        brand = self.db.query(AdvertisingPosition).filter(AdvertisingPosition.id == position_id)
        brand.update(qdict)
        self.db.commit()
        return True

    def get_position_by_id(self,id):
        '''
        根据id查询信息
        :param id:
        :return:
        '''
        return self.rdb.query(AdvertisingPosition).filter(AdvertisingPosition.id == id, AdvertisingPosition.deleted == 0).scalar()

    def delete_by_id(self,id):
        """
        :todo 根据id删除品牌
        :param brand_id 品牌ID
        """
        if id:
            brand = self.db.query(AdvertisingPosition).filter_by( id = id ).first()
            brand.deleted = True
            self.db.commit()

    def get_positions(self):
        '''
        获取广告位置
        :return:
        '''
        return self.rdb.query(AdvertisingPosition).filter(AdvertisingPosition.deleted == 0)


    def get_position_name_by_id(self,id):
        return self.rdb.query(AdvertisingPosition.name).filter(AdvertisingPosition.id==id).scalar()

    def get_position_by_code(self,code_name):
        '''
        todo:根据code获得广告位置
        :param code_name:
        :return:
        '''
        return self.rdb.query(AdvertisingPosition).filter(AdvertisingPosition.deleted == 0,AdvertisingPosition.code_name == code_name).scalar()