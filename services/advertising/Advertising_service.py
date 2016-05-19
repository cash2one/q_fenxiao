#encoding:utf-8

__author__ = 'gaoaifei'


from services.base_services import BaseService
from models.advertise import *

class AdvertisingService(BaseService):
    def _list(self,**qdict):
        """
        :todo 查询用户
        :param qdict 请求参数集合
        """
        if qdict.get('status')=='1':
            query = self.rdb.query(Advertising).filter(Advertising.deleted == 1)
        else:
            query = self.rdb.query(Advertising).filter(Advertising.deleted == 0)
        if qdict.get('id',''):
            query = query.filter(Advertising.id == qdict.get('id'))
        if qdict.get('position_id',''):
            query = query.filter(Advertising.position_id == qdict.get('position_id'))
        if qdict.get('start_date',''):
            query = query.filter(Advertising.gmt_created >= qdict.get('start_date') + ' 00:00:00')
        if qdict.get('end_date',''):
           query = query.filter(Advertising.gmt_created <= qdict.get('end_date') + ' 23:59:59')
        if qdict.get('name',''):
            query = query.filter(Advertising.description.like('%'+qdict.get('name')+'%'))
        if qdict.get('is_open',''):
            query = query.filter(Advertising.is_open == qdict.get('is_open'))
        if qdict.get('media_types',''):
            query = query.filter(Advertising.media_types == qdict.get('media_types'))
        if qdict.get('reorder') == 'asc':
            query = query.order_by(Advertising.gmt_created.asc())
        else:
            query = query.order_by(Advertising.gmt_created.desc())
        return query

    def update_by_id(self,id,**qdict):
        '''
        更新
        :param qdict: id
        :return:
        '''
        Ad = self.db.query(Advertising).filter(Advertising.id == id)
        Ad.update(qdict)
        self.db.commit()
        return True

    def _add(self, **qdict):
        '''
        添加广告
        :param qdict:
        :return:
        '''
        Ad = Advertising()
        Ad.position_id = qdict.get('position_id')
        Ad.name = qdict.get('name')
        Ad.media_types = qdict.get('media_types')
        Ad.ad_link = qdict.get('ad_link')
        Ad.start_time = qdict.get('start_time')
        Ad.end_time = qdict.get('end_time')
        Ad.is_open = qdict.get('is_open')
        Ad.description = qdict.get('description')
        Ad.contact = qdict.get('contact')
        Ad.phone = qdict.get('phone')
        Ad.email = qdict.get('email')
        img_obj = qdict.get('imgs_url',None)
        if img_obj:
            if isinstance(img_obj,list):
                Ad.ad_img = ';'.join(img_obj)
            else:
                Ad.ad_img = img_obj

        self.db.add(Ad)
        # self.db.flush()
        self.db.commit()
        return True,Ad

    def get_advertising_by_id(self,id):
        return self.rdb.query(Advertising).filter(Advertising.id==id,Advertising.deleted==0).scalar()

    def delete_by_id(self,id):
        """
        :todo 根据id删除品牌
        :param brand_id 品牌ID
        """
        if id:
            brand = self.db.query(Advertising).filter_by( id = id ).first()
            brand.deleted = True
            self.db.commit()

    def delete_by_position_id(self,position_id):
        """
        :todo 根据id删除品牌
        :param position_id 广告位置ID
        """
        if id:
            brand = self.db.query(Advertising).filter_by( position_id = position_id ).first()
            brand.deleted = True
            self.db.commit()
