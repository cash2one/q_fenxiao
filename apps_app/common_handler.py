#encoding:utf-8
__author__ = 'wangjinkuan'

from common.base_handler import AppBaseHandler
from services.advertising.Advertising_service import AdvertisingService
from services.advertising.advertising_position_service import AdvertisingPositionService
from services.locations.location_services import LocationServices
from models.location_do import *
from models.item_do import ItemCategory


advertising_service = AdvertisingService()
advertising_position_service = AdvertisingPositionService()
location_service = LocationServices()

CACHE_SECONDE = 3600*24*7


class CommonHandler(AppBaseHandler):
    def get_banner(self,code_name):
        '''
        todo:根据code获取banner
        :return:
        '''
        position_id = self.get_position_by_code(code_name)
        banner_key = 'banner_position_'+str(position_id)
        lst_banner = self.mcache.get(banner_key)
        if not lst_banner:
            advertising_service.set_rdb(self.rdb)
            advertising = advertising_service._list(position_id=position_id,is_open=1)
            lst_banner = []
            for data in advertising:
                dict = self.obj_to_dict(data,['ad_img','ad_link','name'])
                dict.update(item_list_id = dict.pop('ad_link'))
                lst_banner.append(dict)
            self.mcache.set(banner_key,lst_banner,CACHE_SECONDE)
        return lst_banner

    def get_position_by_code(self,code):
        '''
        todo:获取图片code
        :param positon_id:
        :return:
        '''
        my_key = 'ad_position_code_'+code
        ad_position_id = self.mcache.get(my_key)
        if not ad_position_id:
            advertising_position_service.set_rdb(self.rdb)
            ad_position = advertising_position_service._list(code_name=code).scalar()
            ad_position_id = ad_position.id
            self.mcache.set(my_key,ad_position_id,CACHE_SECONDE)
        return ad_position_id

    def get_country_flag(self,country_id):
        '''
        获取国旗
        :return:
        '''
        flag = self.mcache.get('country_flag_'+str(country_id))
        if flag:
            return flag
        else:
            flag = self.rdb.query(Country.national_flag).filter(Country.deleted==0,Country.id==country_id).scalar()
            self.mcache.set('country_flag_'+str(country_id),flag,CACHE_SECONDE)
            return flag

    def get_country_name(self,country_id):
        '''
        国家名称
        :return:
        '''
        country_name = self.mcache.get('country_'+str(country_id))
        if country_name:
            return country_name
        else:
            country_name = self.rdb.query(Country.name).filter(Country.deleted==0,Country.id==country_id).scalar()
            self.mcache.set('country_'+str(country_id),country_name,CACHE_SECONDE)
            return country_name

    def get_category_name_by_id(self,category_id):
        '''
        查询类目名称ƒƒ
        :param category_id:
        :return:
        '''
        return self.rdb.query(ItemCategory.name).filter(ItemCategory.id==category_id).scalar()

    def get_ware_house_name_by_id(self,ware_house_id):
        '''
        保税仓名称
        :param ware_house_id:
        :return:
        '''
        cache_name = self.mcache.get('ware_house_id'+str(ware_house_id))
        if self.mcache.get('ware_house_'+str(ware_house_id)):
            return cache_name
        else:
            name = self.rdb.query(WareHouse.name).filter(WareHouse.id==ware_house_id).scalar()
            self.mcache.set('ware_house_id'+str(ware_house_id),name,CACHE_SECONDE)
            return name