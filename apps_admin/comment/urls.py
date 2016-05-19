#encoding:utf-8
__author__ = 'wangjinkuan'

from apps_admin.comment.handlers import *
from tornado.web import url

_handlers = [
    url(r'/admin/comment',CommentHandler,name='item_comment')
]