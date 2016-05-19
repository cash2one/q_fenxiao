#encoding:utf-8
from tornado.web import url
from handlers import *

handlers=[

        url(r'/admin/system/index.html', SystemIndexHandler,name='system_index'),
        url(r'/admin/system/apps.html', SystemAppsQueryHandler,name='apps_list'),
        url(r'/admin/system/apps_upload.html', SystemAppsUploadHandler,name='apps_upload'),
        url(r'/admin/system/login.html', SystemLoginHandler,name='admin_web_login'),
        url(r'/admin/system/paydeal.html', PayDealHandler,name='PayDealHandler'),


]
