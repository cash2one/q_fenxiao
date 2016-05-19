#encoding:utf-8
__author__ = 'binpo'
from ..base_services import BaseService
from models.location_do import Country,Province,City,Area

class LocationServices(BaseService):

    def _list(self):
        pass


    def get_countries(self):
        '''
        查询国家
        :return:
        '''
        return self.rdb.query(Country).filter(Country.deleted==0)

    def _list_by_parent_id(self,query_type=None,parent_id=None):
        if query_type=='city':
            return self.rdb.query(City.name,City.id).filter(City.deleted==0,City.father==parent_id)
        elif query_type=='area':
            return self.rdb.query(Area.name,Area.id).filter(Area.deleted==0,Area.father==parent_id)
        else:
            return self.rdb.query(Province.name,Province.id).filter(Province.deleted==0)


    def get_by_id(self,query_type,id):
        '''
        根据类型和ID查询对象
        :param query_type:
        :param id:
        :return:
        '''
        if query_type=='city':
            return self.rdb.query(City).filter(City.deleted==0,City.id==id).scalar()
        elif query_type=='area':
            return self.rdb.query(Area).filter(Area.deleted==0,Area.id==id).scalar()
        elif query_type=='province':
            return self.rdb.query(Province).filter(Province.deleted==0,Province.id==id).scalar()
        else:
            return self.rdb.query(Country).filter(Country.deleted==0,Country.id==id).scalar()

    def get_by_code(self,query_type,yh_code):
        '''
        todo:根据code查询对象
        :param query_type:
        :param yh_code:
        :return:
        '''
        if query_type == 'province':
            return self.rdb.query(Province).filter(Province.deleted==0,Province.yh_code==yh_code).scalar()
        elif query_type == 'city':
            return self.rdb.query(City).filter(City.deleted==0,City.yh_code==yh_code).scalar()
        else:
            return self.rdb.query(Area).filter(Area.deleted==0,Area.yh_code==yh_code).scalar()


