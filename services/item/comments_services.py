#encoding:utf-8
__author__ = 'binpo'

from services.base_services import BaseService
from models.item_do import ItemComment

class CommentsServies(BaseService):

    def _list(self,item_id,assess_level,is_show,is_add_comment):
        '''
        品论查询
        :param item_id: 商品ID
        :param kwargs: 其他参数集合
        :return: 查询列表
        '''
        query = self.rdb.query(ItemComment).filter(ItemComment.deleted==0,ItemComment.item_id==item_id)
        if assess_level!='':
            query = query.filter(ItemComment.assess_level == assess_level)
        if is_show!='':
            query = query.filter(ItemComment.is_show == is_show)
        if is_add_comment!='':
            query = query.filter(ItemComment.is_add_comment == is_add_comment)
        query = query.order_by('gmt_created desc')
        return query

    def get_comment_by_id(self,comment_id):
        '''
        查询评论信息
        :param comment_id:
        :return:
        '''
        query = self.rdb.query(ItemComment.id,
                ItemComment.item_id,
                ItemComment.order_id,
                ItemComment.order_no,
                ItemComment.user_name,
                ItemComment.assess_level,
                ItemComment.comment,
                ItemComment.is_show,
                ItemComment.is_add_comment,
                ItemComment.addition_comment,
                ItemComment.add_show_imgs,
                ItemComment.show_imgs).filter(ItemComment.deleted==0,ItemComment.id==comment_id)
        return query

    def check_comment_by_user_id(self,item_id, user_id, order_no):
        '''
        检查用户是否评论
        :param item_id:商品id
        :param user_id:用户id
        :param order_no:订单号
        :return:
        '''
        query = self.rdb.query(ItemComment).filter(ItemComment.deleted==0,ItemComment.user_id==user_id, ItemComment.order_no==order_no,
                                        ItemComment.item_id==item_id).scalar()
        return query

    def _add(self, **qdict):
        '''
        添加评论
        :param qdict:
        :return:
        '''
        comment = ItemComment()
        comment.item_id = qdict.get('item_id')
        comment.order_id = qdict.get('order_id')
        comment.order_no = qdict.get('order_no')
        comment.user_id = qdict.get('user_id')
        comment.user_name = qdict.get('user_name')
        comment.assess_level = qdict.get('assess_level',2)
        comment.is_show = qdict.get('is_show',1)
        comment.is_add_comment = qdict.get('is_add_comment',0)
        comment.show_imgs = qdict.get('show_imgs','')
        comment.comment = qdict.get('comment')
        str = qdict.get('comment')
        if len(str.strip())==0:
            comment.comment = '默认好评'
        comment.add_show_imgs = qdict.get('add_show_imgs','')
        comment.addition_comment = qdict.get('addition_comment', '')
        self.db.add(comment)
        self.db.commit()
        return True,comment.id

    def update_by_id(self,comment_id,**qdict):
        '''
        追加评论
        :param comment_id: 评论id
        :param qdict:
        :return:
        '''
        comment = self.db.query(ItemComment).filter(ItemComment.deleted == 0,ItemComment.id == comment_id).scalar()
        comment.add_show_imgs = qdict.get('add_show_imgs')
        comment.addition_comment = qdict.get('addition_comment')
        comment.is_add_comment = qdict.get('is_add_comment')
        if qdict.get('is_add_comment')==1 and qdict.get('addition_comment').replace(' ','')=='':
            comment.addition_comment = '默认好评'
        self.db.add(comment)
        self.db.commit()
        return True, comment

    def _list_comment(self,**kwargs):
        '''
        todo:全部评价
        :param kwargs:
        :return:
        '''
        query = self.rdb.query(ItemComment).filter(ItemComment.deleted == 0)
        return query

    def get_comment_count_by_item_id(self,item_id):
        '''
        获取商品的评论条数
        :param item_id:
        :return:
        '''
        return self.rdb.query(ItemComment).filter(ItemComment.deleted==0,ItemComment.item_id==item_id).count()