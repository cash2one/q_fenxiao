#!/usr/bin/env python2.7
# encoding:utf-8
from __future__ import absolute_import
__author__ = 'dozy-sun'

import time

from celery_tasks.base import DatabaseTasks
from celery_tasks.celery import app
from utils.regular import Regular

@app.task
def sleep(seconds):
    time.sleep(float(seconds))
    print seconds
    return seconds

@app.task(base=DatabaseTasks)
def sqltest(table):
    sqltest.db.execute('insert into users(`nick`) values ("%s")' % table)
    sqltest.db.commit()

@app.task
def add(x, y):
    print x+y
    return x + y
