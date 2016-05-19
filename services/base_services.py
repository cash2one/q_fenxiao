#encoding:utf-8
# from myshop.services.db_manager import DBManager

import random
class BaseService(object):

    def __init__(self,db=None,rdb=None):
        self.db = db
        self.rdb = rdb

    def set_rdb(self,db):
        '''
        读链接
        :param db:
        :return:
        '''
        self.rdb = db

    def set_db(self,db):
        '''
        写链接
        :param db:
        :return:
        '''
        self.db = db

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
