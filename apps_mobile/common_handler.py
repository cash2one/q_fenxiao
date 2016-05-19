#encoding:utf-8
__author__ = 'binpo'

from services.advertising.Advertising_service import AdvertisingService
from services.advertising.advertising_position_service import AdvertisingPositionService
from common.base_handler import MobileBaseHandler
import random
from tornado.options import options
from common.permission_control import mobile_user_authenticated

advertising_service = AdvertisingService()
advertising_position_service = AdvertisingPositionService()

CACHE_SECONDE=24*3600*2
class CommonHandler(MobileBaseHandler):

    @mobile_user_authenticated
    def prepare(self):
        self.cart_count = self.get_cart_count()
        self.STATIC_DOMAIN = options.STATIC_FILE_DOMAIN

    def get_drp_user_id(self):
        '''
        todo:获取客户所对应的分销商id
        :return:
        '''
        user = self.get_current_user()
        if user.has_key('role_type') and user.get('role_type') in ('0',0):
            drp_user_id = user.get('id')
        else:
            drp_user_id = user.get('belong_id')
        return drp_user_id

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

