#encoding:utf-8
__author__ = 'gaoaifei'

from common.base_handler import AdminBaseHandler
from services.advertising.advertising_position_service import *
from services.advertising.Advertising_service import *
from conf.base_conf import DELETED_STATUS,OPEN_STATUS,MEDIA_TYPES
from services.item.item_services import ItemService
from ..common_handler import CommonHandler
import sys
import json
import datetime
import ujson
from common.asyn_wrap import unblock
ad_pos_service = AdvertisingPositionService()
ad_service = AdvertisingService()
item_service = ItemService()

class AdvertisingPositionHandler(AdminBaseHandler):

    def get(self,operation=None, *args, **kwargs):
        if operation == 'add':
            self.echo('admin/advertising/add_position.html',{
                'data':''
            })
        elif operation == 'edit':
            self.get_paras_dict()
            id = self.qdict.get('id','')
            ad_pos_service.set_rdb(self.rdb)
            data = ad_pos_service.get_position_by_id(id)
            self.echo('admin/advertising/add_position.html',{
                      'data':data,
            })
        else:
            self.get_paras_dict()
            start_date = self.qdict.get('start_date','')
            end_date = self.qdict.get('end_date','')
            status = self.qdict.get('status','0')
            reorder = self.qdict.get('reorder','')
            name = self.qdict.get('name','')
            description = self.qdict.get('description','')
            ad_pos_service.set_rdb(self.rdb)
            query = ad_pos_service._list(**self.qdict)
            data = self.get_page_data(query)
            self.echo('admin/advertising/position_list.html',{
                'data':data,
                'start_date':start_date,
                'end_date':end_date,
                'status':status,
                'reorder':reorder,
                'name':name,
                'description':description,
                'DELETED_STATUS':DELETED_STATUS,
            })

    def post(self, operation=None, *args, **kwargs):
           self.get_paras_dict()
           if  operation=='edit':
             id = self.qdict.get('id')
             self.qdict.pop('category_name')
             ad_pos_service.set_db(self.db)
             is_success = ad_pos_service.update_position_by_id(id, **self.qdict)
             if is_success:
                 self.redirect('/admin/advertis/position/')
           else:
             ad_pos_service.set_db(self.db)
             is_success = ad_pos_service._add(**self.qdict)
             if is_success:
                 self.redirect('/admin/advertis/position/')

    def delete(self,operation=None, *args, **kwargs):
        self.get_paras_dict()
        id = self.qdict.get('id')
        try:
            ad_pos_service.set_db(self.db)
            ad_pos_service.delete_by_id(id)
            ad_service.set_db(self.db)
            ad_service.delete_by_position_id(id)
            self.write_json({'state':'200','info':'success'})
            # return json.dumps({'state':'200','info':'success'})
        except Exception,e:
            self.captureException(sys.exc_info())
            self.write_json({'state':'400','info':e.message})
            # return json.dumps({'state':'400','info':e.message})

    def get_category_name_by_id(self,category_id):
        '''
        todo:通过id获取商品类目
        :param category_id:
        :return:
        '''
        if category_id:
            item_service.set_rdb(self.rdb)
            return item_service.get_category_name_by_id(category_id)
        else:
            return ''

class AdvertisingHandler(CommonHandler):
    '''
    广告操作类
    '''
    def get(self, operation=None, *args, **kwargs):
        if operation == 'add':
            ad_pos_service.set_rdb(self.rdb)
            positions = ad_pos_service.get_positions()
            self.echo('admin/advertising/add_adv.html',{'data':'','MEDIA_TYPES':MEDIA_TYPES,'positions':positions})

        elif operation == 'edit':
            self.get_paras_dict()
            id = self.qdict.get('id','')
            ad_service.set_rdb(self.rdb)
            data = ad_service.get_advertising_by_id(id)
            ad_pos_service.set_rdb(self.rdb)
            positions = ad_pos_service.get_positions()
            self.echo('admin/advertising/add_adv.html',{
                      'data':data,
                      'positions':positions,
                      'MEDIA_TYPES':MEDIA_TYPES
            })
        else:
            self.get_paras_dict()
            start_date = self.qdict.get('start_date','')
            end_date = self.qdict.get('end_date','')
            status = self.qdict.get('status','0')
            reorder = self.qdict.get('reorder','')
            name = self.qdict.get('name','')
            is_open = self.qdict.get('is_open','')
            media_types = self.qdict.get('media_types','')
            ad_service.set_rdb(self.rdb)
            query = ad_service._list(**self.qdict)
            data = self.get_page_data(query)
            self.echo('admin/advertising/ad_list.html',{
                'data':data,
                'start_date':start_date,
                'end_date':end_date,
                'status':status,
                'reorder':reorder,
                'name':name,
                'media_types':media_types,
                'is_open':is_open,
                'DELETED_STATUS':DELETED_STATUS,
                'OPEN_STATUS':OPEN_STATUS,
                'MEDIA_TYPES':MEDIA_TYPES
            })


    def post(self, operation=None, *args, **kwargs):
        '''
        添加／编辑广告
        :param operation:
        :param args:
        :param kwargs:
        :return:
        '''
        self.get_paras_dict()
        if operation=='edit':
            id = self.qdict.get('id')
            postion_id = self.qdict.get('position_id')
            ad_service.set_db(self.db)
            if self.qdict.get('imgs_url'):
                self.qdict['ad_img'] = self.qdict.get('imgs_url')
                self.qdict.pop('imgs_url')
            self.qdict.pop('id')
            self.qdict.pop('_xsrf')
            is_success = ad_service.update_by_id(id, **self.qdict)
            if is_success:
                self.redirect('/admin/advertis/advertising/')
        else:
            ad_service.set_db(self.db)
            is_success,Ad = ad_service._add(**self.qdict)
            postion_id = Ad.position_id
            if is_success:
                self.redirect('/admin/advertis/advertising/')
        self.delete_banners(postion_id) #删除banner缓存

    def get_position_name_by_id(self,id):
            '''
            todo:通过id广告位置
            :param id:
            :return:
            '''
            ad_pos_service.set_rdb(self.rdb)
            return ad_pos_service.get_position_name_by_id(id)

    def check_is_online(self,start_time, end_time):
        '''
        判断广告是否上线 到期下线等
        :param start_time: 广告开始时间
        :param end_time: 广告结束时间
        :return:
        '''
        currect_time = datetime.datetime.now()
        if currect_time < start_time:
            return '还未上线'
        elif end_time < currect_time:
            return "到期下线"
        elif start_time <= currect_time and currect_time <= end_time:
            return '已上线'

    def delete(self,operation=None, *args, **kwargs):
        self.get_paras_dict()
        ad_id = self.qdict.get('id')
        ad_service.set_rdb(self.rdb)
        ad = ad_service._list(id=ad_id).scalar()
        try:
            ad_service.set_db(self.db)
            ad_service.delete_by_id(ad_id)
            self.delete_banners(ad.position_id)
            self.write_json({'state':'200','info':'success'})
        except Exception,e:
            self.captureException(sys.exc_info())
            self.write_json({'state':'400','info':e.message})