#encoding:utf-8
__author__ = 'binpo'

from tornado.web import url
from .yh_task_handler import *
from tasks import TaskHandlers,TaskDealHandler

_handlers = [
    url(r'/admin/tasks/',TaskHandlers,name='tasks'),
    url(r'/admin/tasks/([\d]*).html',TaskDealHandler,name='tasks_deal'),
    url(r'/admin/tasks/deal/',YhTaskHandler,name='api_tasks'),
]