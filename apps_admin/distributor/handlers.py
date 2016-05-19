#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'gaoaifei'

from common.base_handler import AdminBaseHandler
from apps_admin.common_handler import CommonHandler
from services.distributor.distributor_service import DistributorUserservice
from conf.user_conf import USER_STATUS, ROLE_TYPE
import sys

distributor_service = DistributorUserservice()

class DistributorHandler(CommonHandler):
    '''
    分销商管理列表
    '''
    def get(self, operation, *args, **kwargs):
        distributor_service.set_rdb(self.rdb)
        # 新增
        if operation == 'add':
            self.echo('admin/distributor/add.html',{
                'data':''
            })
        else:
            self.get_paras_dict()
            start_date = self.qdict.get('start_date','')
            end_date = self.qdict.get('end_date','')
            status = self.qdict.get('status','0')
            type = self.qdict.get('type','0')
            reorder = self.qdict.get('reorder','')
            phone = self.qdict.get('phone','')
            query = distributor_service.list(**self.qdict)
            data = self.get_page_data(query)
            self.echo('admin/distributor/list.html',{
                'data':data,
                'start_date':start_date,
                'end_date':end_date,
                'status':status,
                'type':type,
                'reorder':reorder,
                'phone':phone,
                'USER_STATUS':USER_STATUS,
                'ROLE_TYPE':ROLE_TYPE,
                'count':query.count()
            })

    def post(self, operation=None, *args, **kwargs):
        '''
        新增or编辑
        :param operation:
        :param args:
        :param kwargs:
        :return:
        '''
        self.get_paras_dict()
        distributor_service.set_db(self.db)
        if operation=='edit':
            id = self.qdict.get('id')
            self.qdict.pop('category_name')
            is_success = distributor_service.update_distributor_by_id(id, **self.qdict)
            if is_success:
                 self.redirect('/admin/distributor/position/')
        else:
            checkRes = self.check_distributor_is_exsit(self.qdict.get('user_name'))
            if checkRes==False:
                return self.write('该用户名已存在，请重新输入')
            id = distributor_service._add(**self.qdict)
            show_id = self.set_show_id_by_id(id)
            distributor_service.update_distributor_shop_id_by_id(id,show_id)
            self.redirect('/admin/distributor/position/')

    def delete(self,operation=None, *args, **kwargs):
        self.get_paras_dict()
        id = self.qdict.get('id')
        if operation == 'renew':
            deleted = 0
        else:
            deleted = 1
        try:
            distributor_service.set_db(self.db)
            distributor_service.delete_user(id,deleted)
            self.write_json({'state':'200','info':'success'})
        except Exception,e:
            self.captureException(sys.exc_info())
            self.write_json({'state':'400','info':e.message})

    def check_distributor_is_exsit(self,user_name):
        '''
        判断新增得分销商账号是否已经存在
        :param user_name:新增账号
        :return:
        '''
        distributor_service.set_rdb(self.rdb)
        drp  = distributor_service.check_distributor_is_exsit(user_name)
        if  drp:
            return False
        else:
            return True