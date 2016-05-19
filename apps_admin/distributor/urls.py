#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'gaoaifei'

from apps_admin.distributor.handlers import *
from tornado.web import url

_handlers = [
    url(r'/admin/distributor/([\w\W]*)',DistributorHandler,name='distributor_list')
]