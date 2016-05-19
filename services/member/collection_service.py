#encoding:utf-8
__author__ = 'gaoaifei'
from ..base_services import BaseService
from models.member_do import *

class MemberCollectionsServices(BaseService):
    '''
    我的收藏商品类
    '''
    def get_collections_by_user_id(self,user_id):
        '''
        我的收藏品
        :param user_id: 当前用户id
        :return:
        '''
        return self.rdb.query(MemberCollections.item_id,MemberCollections.user_id).filter(MemberCollections.deleted == 0 ,
                                                                                          MemberCollections.user_id == user_id)

    def check_item_is_collection(self,item_id,user_id):
        '''
        判断商品是否已经收藏
        :param item_id:
        :param user_id:
        :return:
        '''
        return self.rdb.query(MemberCollections.id,MemberCollections.deleted,MemberCollections.item_id).filter(MemberCollections.item_id == item_id,
                                                             MemberCollections.user_id == user_id).first()


    def add_collection(self,item_id,user_id):
        '''
        添加收藏
        :param item_id: 商品id
        :param user_id: 用户id
        :return:
        '''
        member_collection = MemberCollections()
        member_collection.user_id = user_id
        member_collection.item_id = item_id
        self.db.add(member_collection)
        self.db.commit()
        return True

    def cancle_member_collection(self,item_id,user_id):
        '''
        更新
        :param qdict: id
        :return:
        '''
        self.db.query(MemberCollections).filter(MemberCollections.item_id == item_id,
                                                             MemberCollections.user_id == user_id).delete(synchronize_session=False)
        self.db.commit()