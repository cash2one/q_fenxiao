#encoding:utf-8
__author__ = 'binpo'

from ..base_services import BaseService
from models.decorate_do import CollectionTypes,UserCollection
from sqlalchemy import func


class UserCollectionService(BaseService):

    def create_collection(self,user_id,coll_type,obj_id):
        '''
        :todo 创建用户收藏
        :param user_id:
        :param coll_type:
        :param obj_id:
        :param request_url:
        :return:
        '''
        user_collection = UserCollection()
        user_collection.collect_type = coll_type
        user_collection.url = ''#request_url
        user_collection.key_id = obj_id
        user_collection.user_id = user_id
        self.db.add(user_collection)
        self.db.commit()


    def delete_collection(self,coll_id,user_id):
        '''
        :todo 删除用户收藏
        :param coll_id:
        :param user_id:
        :return:
        '''
        self.db.query(UserCollection).filter(UserCollection.deleted==0,UserCollection.user_id==user_id,UserCollection.id==coll_id).update({'deleted':1},synchronize_session=False)


    def query_collection_by_type(self,user_id,coll_type=None):
        '''
        :todo 根据用户查询用户收藏
        :param coll_type:
        :param user_id:
        :return:查询结果集
        '''

        query = self.db.query(UserCollection).filter(UserCollection.deleted==0,UserCollection.user_id==user_id)
        if coll_type.strip():
            query = query.filter(UserCollection.collect_type==coll_type)
        query=query.order_by('gmt_created desc')
        return query


    def query_collection_by_id(self,collection_id):
        '''
        :todo 根据ID查询收藏
        :param collection_id:
        :return: 返回收藏对象
        '''
        return self.db.query(UserCollection).filter(UserCollection.deleted==0,UserCollection.id==collection_id).scalar()


    def query_all_collection_by_user_id(self,user_id):
        '''
        :todo 按分类查询某个用户的所有收藏
        :param user_id:
        :return:查询结果集
        '''

        return self.db.query(UserCollection.collect_type,UserCollection.collection_name,func.count(UserCollection.id))\
            .filter(UserCollection.deleted==0,UserCollection.user_id==user_id)\
            .group_by(UserCollection.collect_type)

