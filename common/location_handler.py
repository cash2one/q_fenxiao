#encoding:utf-8
__author__ = 'binpo'
from common.base_handler import BaseHandler,AdminBaseHandler
from services.locations.location_services import LocationServices

class LocationHandler(BaseHandler):

    def get(self, *args, **kwargs):
        query_type = self.get_argument('query_type',None)
        parent_id = self.get_argument('parent_id',None)
        query = LocationServices(rdb=self.rdb)._list_by_parent_id(query_type=query_type,parent_id=parent_id)
        data = [{'name':obj.name,'id':obj.id} for obj in query]
        self.write_json({'state':200,'data':data})

class AdminLocationHandler(BaseHandler):

    def get(self,*args, **kwargs):
        '''
        todo:获得地理信息
        :return:
        '''
        query_type = self.get_argument('query_type',None)
        parent_id = self.get_argument('parent_id',None)
        query = LocationServices(rdb=self.rdb)._list_by_parent_id(query_type=query_type,parent_id=parent_id)
        if query_type == 'city':
            query_area = LocationServices(rdb=self.rdb)._list_by_parent_id(query_type='area',parent_id=query[0].id)
            city = [{'name':obj.name,'id':obj.id} for obj in query]
            area = [{'name':obj.name,'id':obj.id} for obj in query_area]
            data = {'city':city,'area':area}
        else:
            area = [{'name':obj.name,'id':obj.id} for obj in query]
            data = {'area':area}
        self.write_json({'stat':200,'data':data})