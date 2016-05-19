#encoding:utf-8
__author__ = 'binpo'

from utils.db_connection import DB
from utils.cache_manager import MemcacheManager

from setting import ENGINE
db = DB(ENGINE)

class CacheBase(object):

    def __init__(self):
        self.mcache = MemcacheManager().get_conn()
        #self.rcache = RedisManaher().cache_con()
    @property
    def db(self):
        return db.get_session()

    # @property
    # def mcache(self):
    #     return MemcacheManager.get_single_conn()

    # @property
    # def rcache(self):
    #     return RedisManaher.get_single_cache()