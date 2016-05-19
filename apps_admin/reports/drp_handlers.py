#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'gaoaifei'


from common.base_handler import AdminBaseHandler
from apps_admin.common_handler import CommonHandler

from services.orders.orders_services import OrderServices
from services.users.user_services import UserServices
from services.distributor.distributor_service import DistributorUserservice

orders_services = OrderServices()
distributor_service = DistributorUserservice()
user_services = UserServices()

class DrpReport(CommonHandler):
    def get(self, *args, **kwargs):
        '''

        :param args:
        :param kwargs:
        :return:
        '''
        self.get_paras_dict()
        distributor_service.set_rdb(self.rdb)
        query = distributor_service.list(**self.qdict)
        data = self.get_page_data(query)
        self.echo('admin/reports/drp_reports.html',{
                'data':data,
                'count':query.count()
            })

    def get(self, *args, **kwargs):
        orders_services.set_rdb(self.rdb)
        query = orders_services.drp_item_orders_list()
        self.echo('admin/reports/drp_reports.html',{
            'data':query
        })

    def get_drp_total_amount_by_id(self,id):
        '''
        获取分销商销售总金额
        :param id: 分销商用户id
        :return:
        '''
        orders_services.set_rdb(self.rdb)
        count = orders_services.get_drp_total_amount_by_id(id)
        if count==None:
            return 0.0
        return count

    def get_drpusers_by_id(self,id):
        '''
        获取分销商下发展的会员
        :param id:
        :return:
        '''
        user_services.set_rdb(self.rdb)
        return user_services.get_drpusers_by_id(id)