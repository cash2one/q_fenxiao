#encoding:utf-8
__author__ = 'wangjinkuan'

from models.user_do import Users,DistributorUser
from models.orders_do import Orders
from models.item_do import ItemCategory
from common.base_handler import AdminBaseHandler
from models.item_do import ItemCategory
from models.item_do import Merchant
import random

class CommonHandler(AdminBaseHandler):
    def get_order_no(self,order_id):
        m_key = 'order_no_'+str(order_id)
        order_no = self.mcache.get(m_key)
        if not order_no:
            order = self.rdb.query(Orders).filter(Orders.deleted == 0,Orders.id == order_id).scalar()
            order_no = order.order_no
            self.mcache.set(m_key,order_no,3600*24*7)
        return order_no

    def get_user_name(self,user_id):
        m_key = 'user_name_'+str(user_id)
        user_name = self.mcache.get(m_key)
        if not user_name:
            user = self.rdb.query(Users).filter(Users.deleted == 0,Users.id == user_id).scalar()
            user_name = user.user_name
            self.mcache.set(m_key,user_name,3600*24*7)
        return user_name

    def delete_banners(self,position_id):
        '''
        todo:删除banner缓存
        :param code_name:
        :return:
        '''
        banner_key = 'banner_position_'+str(position_id)
        lst_banner = self.mcache.get(banner_key)
        if lst_banner:
            self.mcache.delete(banner_key)

    def get_category_name(self,category_id):
        '''
        todo:获取类目名称
        :param category_id:
        :return:
        '''
        category_key = 'category_'+str(category_id)
        category_name = self.mcache.get(category_key)
        if not category_name:
            category_name = self.rdb.query(ItemCategory.name).filter(ItemCategory.deleted==0,ItemCategory.id==category_id).scalar()
            self.mcache.set(category_key,category_name,3600*24*7)
        return category_name

    def get_category_name_by_id(self,category_id):
        '''
        查询类目名称
        :param category_id:
        :return:
        '''
        return self.rdb.query(ItemCategory.name).filter(ItemCategory.id==category_id).scalar()

    def delete_category_name(self,category_id):
        '''
        todo:删除类目缓存
        :param category_id:
        :return:
        '''
        category_key = 'category_'+str(category_id)
        category_name = self.mcache.get(category_key)
        if category_name:
            self.mcache.delete(category_key)


    def get_id_by_show_id(self,showId):
        '''
        根据showid获取真实id值
        :param showId: type string 自动增长列id值
        :return:
        '''
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

    def get_category_name_list(self,category_id):
        '''
        todo:
        :param category_id:
        :return:
        '''
        item_category = self.rdb.query(ItemCategory).filter(ItemCategory.deleted==0,ItemCategory.id==category_id).scalar()
        if item_category.parent_id == '0':
            return item_category.name
        else:
            top_category = self.rdb.query(ItemCategory).filter(ItemCategory.deleted==0,ItemCategory.id==item_category.parent_id).scalar()
            return top_category.name +' / '+item_category.name

    def get_supplys_by_id(self,id):
        '''
        获取供应商的名字
        :param id:
        :return:
        '''
        sup = self.rdb.query(Merchant).filter(Merchant.id==id).scalar()
        if not sup:
            return ''
        else:
            return sup.name

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

    def get_distributors_vendor_by_id(self,id):
        '''
        获取分销商
        :param id:
        :return:
        '''
        drp = self.rdb.query(DistributorUser).filter(DistributorUser.id==id,
                                                      DistributorUser.parent_id==0,DistributorUser.role_type==1).scalar()


        if not drp:
            return ''
        else:
            return drp.real_name