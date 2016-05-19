#encoding:utf-8
from tornado.web import url
from handlers import *

_handlers=[

        url(r'/admin/sites/nav/index.html', NavHandler,name='site_navigation'),
        url(r'/admin/sites/conf/index.html', ConfHandler,name='site_conf'),
]
