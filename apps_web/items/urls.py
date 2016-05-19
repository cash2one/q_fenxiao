#encoding:utf-8
__author__ = 'binpo'

from tornado.web import url
from handlers import *

_handlers = [
    url(r'/item/category/(\d*).html',ItemsQueryHandler,name='item_category'),
    url(r'/item/category_(\d*).html',ItemscategoryHandler,name='item_category_list'),#导航二级分类进去
    url(r'/item/nav.html',NavHandler,name='navigation'), #导航
    url(r'/item/detail/(\d*).html',ItemsDetailHandler,name='item_detail'),#
    url(r'/item/history.html',HistoryViewHandler,name='item_history_view'),
    url(r'/item/similar.html',SimilarItemsHandler,name='item_similar_view'),
    url(r'/item/comment_list.html', CommentListHandler, name='item_comment_list'),
    url(r'/item/comment.html', CommentHandler,name='item_comment'),
]