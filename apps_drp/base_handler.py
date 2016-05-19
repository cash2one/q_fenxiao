#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'binpo'

from common.base_handler import DistributorHandler
from common.permission_control import distributor_user_authenticated,drp_user_authenticated
import random
from models.user_do import Users,DistributorUser


class DrpBaseHandler(DistributorHandler):

    @distributor_user_authenticated
    @drp_user_authenticated
    def prepare(self):
        pass
    def echo(self, template, context=None, globals=None,layout='admin_drp/include/base.html'):
        data = self.render(template, context, globals,layout)
        self.write(data)
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

    def get_distributors_by_id(self,id):
        '''
        获取分销商
        :param id:
        :return:
        '''
        drp = self.rdb.query(DistributorUser).filter(DistributorUser.id==id,
                                                      DistributorUser.parent_id==0,DistributorUser.role_type==0).scalar()


        if not drp:
            return ''
        else:
            return drp.real_name

class DrpHomeHandler(DrpBaseHandler):

    def get(self, *args, **kwargs):
        self.echo('admin_drp/index.html',layout='admin_drp/base.html')