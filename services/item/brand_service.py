#encoding:utf-8
__author__ = 'gaoaifei'

from services.base_services import BaseService
from models.item_do import Brand,ItemCategory

class BrandService(BaseService):
    def _list(self,**qdict):
        """
        :todo 查询用户
        :param qdict 请求参数集合
        """
        if qdict.get('status')=='1':
            query = self.rdb.query(Brand).filter(Brand.deleted == 1)
        else:
            query = self.rdb.query(Brand).filter(Brand.deleted == 0)
        if qdict.get('start_date',''):
            query = query.filter(Brand.gmt_created > qdict.get('start_date'))
        if qdict.get('end_date',''):
           query = query.filter(Brand.gmt_created < qdict.get('end_date'))
        if qdict.get('description',''):
            query = query.filter(Brand.description.like('%'+qdict.get('description')+'%'))
        if qdict.get('name',''):
            query = query.filter(Brand.phone == qdict.get('name'))
        if qdict.get('category_id',''):
                query = query.filter(Brand.category_id == qdict.get('category_id'))
        if qdict.get('reorder') == 'asc':
            query = query.order_by(Brand.sort.asc())
        else:
            query = query.order_by(Brand.sort.desc())

        return query

    def _add(self,**qdict):
        '''
        添加品牌
        :param qdict:
        :return:
        '''
        brand = Brand()
        brand.category_id = qdict.get('category_id')
        brand.name = qdict.get('name')
        brand.description = qdict.get('description')
        brand.is_online = qdict.get('is_online')
        if qdict.get('sort'):
            brand.sort = qdict.get('sort')
        else:
            brand.sort = 50
        self.db.add(brand)
        self.db.flush()
        self.db.commit()
        return True

    def update_brand_by_id(self,brand_id,**qdict):
        '''
        更新
        :param qdict: id
        :return:
        '''
        brand = self.db.query(Brand).filter(Brand.id == brand_id)
        qdict.pop('category_name')
        brand.update(qdict)
        self.db.commit()
        return True

    def delete_by_id(self,brand_id):
        """
        :todo 根据id删除品牌
        :param brand_id 品牌ID
        """
        if brand_id:
            brand = self.db.query(Brand).filter_by( id = brand_id ).first()
            brand.deleted = True
            self.db.commit()

    def update_status_by_id(self,brand_id):
        """
        更改状态为正常状态
        :param brand_id:
        :return:
        """
        if brand_id:
            brand = self.db.query(Brand).filter_by( id = brand_id ).first()
            brand.deleted = 0
            self.db.commit()

    def get_brand_by_id(self,brand_id):

        """根据id查询品牌详细信息
        :param brand_id 品牌ID
        """
        return self.rdb.query(Brand).filter(Brand.id == brand_id, Brand.deleted == 0).scalar()

    def check_brand_name_is_exist(self,name,category_id):
        """
        校验品牌名称在同一目录下不能重复
        :param name:
        :param category_id:
        :return:
        """
        data = self.rdb.query(Brand).filter(Brand.category_id == category_id, Brand.deleted == 0 , Brand.name == name ).scalar()
        return data

    def get_brands_by_category_id(self,category_id):
        '''
        todo:获取category_id下所有的品牌
        :param category_id:
        :return:
        '''
        category_ids = self.rdb.query(ItemCategory.id).filter(ItemCategory.deleted==0,ItemCategory.parent_id==category_id)
        cids = []
        if category_ids.count()>0:
            for c_id in category_ids:
                cids.append(c_id[0])
        cids.append(category_id)
        query = self.rdb.query(Brand).filter(Brand.deleted==0,Brand.category_id.in_(cids))
        return query

    def get_brands_by_ids(self,ids):
        '''
        根据ids获取所有品牌
        :param ids:品牌id列表
        :return:
        '''
        return self.rdb.query(Brand).filter(Brand.deleted == 0,
                                                  Brand.category_id.in_(ids))











