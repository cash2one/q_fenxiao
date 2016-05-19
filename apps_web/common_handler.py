#encoding:utf-8
__author__ = 'binpo'
from models.item_do import *
from models.location_do import *
from models.config import Config
import random
CACHE_SECONDE=24*3600*2
class CommonHandler(object):

    def __init__(self):
        pass

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

    def get_config(self,key):
        cache_name = self.mcache.get('config_'+str(key))
        if self.mcache.get('config_'+str(key)):
            return cache_name
        else:
            config = self.rdb.query(Config).filter(Config.key==key).scalar()
            self.mcache.set('config_'+str(key),config.value)
            return config.value

    def get_id_by_show_id(self,showId):
        '''
        根据showid获取真实id值
        :param showId: type string 自动增长列id值
        :return:
        '''
        showId = str(showId)
        i = showId[len(showId)-1]
        j = showId[0:len(showId)-1]
        k = (int(j) - int(i) - 1000)/int(i)
        return k

    def set_show_id_by_id(self,id):
        '''
        设置showid
        :param id: 真实id
        :return:
        '''
        a = random.randint(1,9)
        b = a*int(id) + 1000 + a
        j = str(b) + str(a)
        return j
    