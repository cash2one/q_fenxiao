#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'gaoaifei'

from tornado.web import url
from handlers import *

_handlers = [
    url(r'/admin/comm/([\w\W]*)',CommHandler,name='comm'),
]
