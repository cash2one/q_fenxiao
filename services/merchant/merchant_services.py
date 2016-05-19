#encoding:utf-8
__author__ = 'wangjinkuan'

from ..base_services import BaseService
from models.item_do import Merchant
from utils.md5_util import create_md5

class MerchantService(BaseService):

    def _list(self,**kwargs):
        '''
        todo:获取供应商列表
        :param kwargs:
        :return:
        '''
        query = self.rdb.query(Merchant).filter(Merchant.deleted==0)
        return query

    def get_by_id(self,vendor_id):
        '''
        todo:
        :param vendor_id:
        :return:
        '''
        query = self.rdb.query(Merchant).filter(Merchant.deleted==0,Merchant.id==vendor_id).scalar()
        return query

    def _add(self,name,account ,address,contact,phone,remark,vendor_id=None):
        '''
        todo:新增供应商
        :param kwargs:
        :return:
        '''
        vendor = self.db.query(Merchant).filter(Merchant.deleted==0,Merchant.id==vendor_id).scalar()
        if not vendor:
            vendor = Merchant()
        vendor.name = name
        vendor.account = account
        vendor.address = address
        vendor.contact = contact
        vendor.phone = phone
        vendor.remark = remark
        self.db.add(vendor)
        self.db.commit()

    def get_all_vendors(self):
        '''
        获取所有的供应商
        :return:
        '''
        return self.rdb.query(Merchant).filter(Merchant.deleted==0)

    def user_passed(self,passowrd):
        '''
        生成密码
        :param uid:
        :param passowrd:
        :return:
        '''
        return create_md5(create_md5(create_md5(passowrd)))