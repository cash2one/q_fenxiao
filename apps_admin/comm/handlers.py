#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'gaoaifei'
from common.base_handler import AdminBaseHandler
from ..common_handler import CommonHandler
from services.distributor.distributor_service import DistributorUserservice
from services.orders.orders_services import OrderServices
from services.users.user_services import UserServices
from services.item.item_services import ItemService
import sys
import uuid

distributor_service = DistributorUserservice()
orders_services = OrderServices()
user_services = UserServices()
item_services = ItemService()

class CommHandler(CommonHandler):
    def get(self,operation,*args, **kwargs):
        self.get_paras_dict()
        distributor_service.set_rdb(self.rdb)
        orders_services.set_rdb(self.rdb)
        item_services.set_rdb(self.rdb)
        # 供应商list
        if operation=='merchant':
            query = item_services._list_merchant()
            data = self.get_page_data(query)
            self.echo('admin/comm/merchant_list.html',{
                'data':data,
                'count':query.count()
            })
        # 分销商列表
        elif operation=='distributor':
            query = distributor_service.list(**self.qdict)
            data = self.get_page_data(query)
            self.echo('admin/comm/drp_list.html',{
                'data':data,
                'count':query.count()
            })
        # 结算界面
        elif operation == 'clearing':
            drp_id = self.qdict.get('drp_id')
            count = orders_services.get_drp_total_comm_by_id(drp_id,0)
            if count==None:
                count = 0.0
            drp = distributor_service.get_distributor_by_id(drp_id)
            self.echo('admin/comm/clearing.html',
                          {'drp':drp,
                           'count':count,
                           'drp_id':drp_id,
                          })
        #  结算日志
        else:
            drp_usere_id = self.get_argument('drp_usere_id','')
            keyword = self.get_argument('keyword','')
            distributor_service.set_rdb(self.rdb)
            distributors = distributor_service.get_all_distributor_users(type=0)

            orders_services.set_rdb(self.rdb)
            query = orders_services.list_settlement(drp_usere_id,keyword)
            data = self.get_page_data(query)
            self.echo('admin/comm/log_list.html',{
                'data':data,
                'count':query.count(),
                'drp_usere_id':drp_usere_id,
                'keyword':keyword,
                'distributors':distributors
            })

    def post(self,operation):
        # 结算
        if operation == 'clearing':
            try:
                 drp_usere_id = self.get_argument('drp_usere_id','')
                 payment_no = self.get_argument('payment_no','')
                 content = self.get_argument('content','')
                 orders_services.set_rdb(self.rdb)
                 count = orders_services.get_drp_total_comm_by_id(drp_usere_id,0)
                 if count:
                    settlement_no = str(uuid.uuid4())
                    orders_services.set_db(self.db)
                    admin_id = self.get_current_user().get('id')
                    res = orders_services.add_settlement(admin_id,drp_usere_id,count,payment_no,content,settlement_no)
                    print res
                    if res ==True:
                        orders_services.update_payorders_settlement(drp_usere_id,settlement_no)
                 self.db.commit()
            except Exception,e:
                return self.write(e.message)
                # return  self.write_json({'stat':'fail','info':e.message})
        # self.redirect(self.reverse_url('comm','distributor'))
        return self.write('结算成功')

    def get_drp_total_comm_by_id(self,id,settlement=None):
        '''
        获取分销商总金额
        :param id: 分销商用户id
        :return:
        '''
        orders_services.set_rdb(self.rdb)
        count = orders_services.get_drp_total_comm_by_id(id,settlement)
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

    def get_merchant_total_comm_by_id(self,id,settlement):
        '''
        获取分销商总金额
        :param id: 分销商用户id
        :return:
        '''
        orders_services.set_rdb(self.rdb)
        count = orders_services.get_merchant_total_comm_by_id(id,settlement)
        if count==None:
            return 0.0
        return count


