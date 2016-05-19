#!/usr/bin/env python2.7
# encoding:utf-8
from __future__ import absolute_import
from celery.schedules import crontab

#celery需要引入的包含任务的文件 计划任务配置
TASKS_LIST = ['celery_tasks.tasks_orders']

Timing_task={

        #超时取消订单
        "cancel_timeout_orders": {
            "task": "celery_tasks.tasks_orders.cancel_timeout_orders",
            "schedule":crontab(minute=0, hour='*/1')
        },

        #自动完成订单
        "complete_timeout_orders": {
            "task": "celery_tasks.tasks_orders.complete_timeout_orders",
            "schedule":crontab(minute=0, hour=0)
        },

        #自动评论
        # "comment_timeout_orders": {
        #     "task": "celery_tasks.tasks_orders.comment_timeout_orders",
        #     # "schedule":crontab(minute='*/1'),
        #     "schedule":crontab(minute=0, hour=0)
        # },
    }
#定时任务

