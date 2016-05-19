#encoding:utf-8
__author__ = 'wangjinkuan'

from ..common_handler import CommonHandler
from services.item.comments_services import CommentsServies
from conf.item_conf import ASSESS_LEVEL

comments_service = CommentsServies()

class CommentHandler(CommonHandler):
    def get(self,*args, **kwargs):
        comments_service.set_rdb(self.rdb)
        query = comments_service._list_comment()
        comments = self.get_page_data(query)
        self.echo('admin/comment/comments.html',{'data':comments,'ASSESS_LEVEL':ASSESS_LEVEL})