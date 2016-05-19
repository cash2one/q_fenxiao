#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'gaoaifei'


from services.base_services import BaseService
from models.user_do import Users,DistributorUser
from sqlalchemy import or_
from sqlalchemy.sql.functions import now
from sqlalchemy.orm import aliased
import datetime
import time
import uuid
from utils.exchange_rate import get_usd_exchange_rate_and_count
from utils.md5_util import create_md5

class DistributorUserservice(BaseService):

    def list(self,**qdict):
        '''
        list 查询所有分销商用户
        :return:
        '''
        type = qdict.get('type')
        query = self.rdb.query(DistributorUser).filter(DistributorUser.role_type==0)
        if type=='1':
            query = self.rdb.query(DistributorUser).filter(DistributorUser.role_type==1)
        if qdict.get('start_date',''):
            query = query.filter(DistributorUser.gmt_created>qdict.get('start_date'))
        if qdict.get('end_date',''):
           query = query.filter(DistributorUser.gmt_created<qdict.get('end_date'))
        if qdict.get('status')== '1':
            query = query.filter(DistributorUser.deleted == 1)
        else:
            query = query.filter(DistributorUser.deleted == 0)

        if qdict.get('phone',''):
            query = query.filter(DistributorUser.phone==qdict.get('phone'))
        if qdict.get('reorder')=='asc':
            query = query.order_by(DistributorUser.gmt_created.asc())
        else:
            query = query.order_by(DistributorUser.gmt_created.desc())
        return query

    def _add(self,**qdict):
        '''
        添加广告位
        :param qdict:
        :return:
        '''
        drp = DistributorUser()
        drp.uid = str(uuid.uuid4())
        drp.user_name = qdict.get('user_name')
        drp.role_type = qdict.get('role_type')
        drp.nick = qdict.get('nick')
        drp.email = qdict.get('email')
        drp.phone = qdict.get('phone')
        drp.role_type = qdict.get('role_type',0)
        if qdict.get('parent_id'):
            drp.parent_id = int(qdict.get('parent_id'))
        else:
            drp.parent_id = 0
        drp.real_name = qdict.get('real_name')
        drp.user_pwd = self.user_passed(qdict.get('user_pwd')).strip()
        drp.sex = qdict.get('sex')
        drp.area = qdict.get('area')
        drp.status = qdict.get('status')
        if qdict.get('status')=='reeze':
            drp.reeze_time = now()
        drp.comments = qdict.get('comments')
        self.db.add(drp)
        self.db.commit()
        return drp.id

    def user_passed(self,passowrd):
        '''
        生成密码
        :param uid:
        :param passowrd:
        :return:
        '''
        return create_md5(create_md5(create_md5(passowrd)))

    def delete_user(self,user_id,status):
        """
        :todo 删除用户
        :param user_id 删除用户id
        :param status 是否删除 0正常 1删除
        """
        user = self.db.query(DistributorUser).filter(DistributorUser.id==user_id).first()
        user.deleted = status
        self.db.commit()

    def get_all_distributor_users(self,type):
        '''
        查询所有一级分销商用户
        :return:object
        '''
        if type == 0:
            return self.rdb.query(DistributorUser.real_name,DistributorUser.id).filter(
                                    DistributorUser.deleted==0,
                                    DistributorUser.role_type==0,
                                    DistributorUser.parent_id==0,
                                    DistributorUser.status=='normal').order_by('gmt_created desc')
        else:
            return self.rdb.query(DistributorUser.real_name,DistributorUser.id).filter(
                                    DistributorUser.deleted==0,
                                    DistributorUser.role_type==1,
                                    DistributorUser.parent_id==0,
                                    DistributorUser.status=='normal').order_by('gmt_created desc')

    def update_distributor_shop_id_by_id(self,id, show_id):
        '''
        设置商品详情的showid
        :param id: 类目的真实id
        :param show_id:类目showId
        :return:
        '''
        query = self.db.query(DistributorUser).filter(DistributorUser.deleted == 0,DistributorUser.id == id)
        query.update({'shop_id':show_id})
        self.db.commit()
        return True

    def get_distributor_by_id(self,id):
        '''
        获取分销商信息
        :param id:
        :return:
        '''
        return self.rdb.query(DistributorUser).filter(DistributorUser.deleted == 0 ,DistributorUser.id==id).scalar()

    def check_distributor_is_exsit(self,user_name):
        print user_name
        return self.rdb.query(DistributorUser).filter(DistributorUser.user_name==user_name).count()
