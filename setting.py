# encoding:utf-8
__author__ = 'binpo'

import os
current_path = os.path.dirname(__file__)
static_path = os.path.join(current_path, 'static')
template_path = os.path.join(current_path, 'templates')

# img_upload = 'upload/img/'
# upload_path = os.path.join(static_path, img_upload)
#
# avatar_upload = 'upload/img/avatar/'
# upload_avatar_path = os.path.join(static_path, avatar_upload)


settings = dict(
    title=u"全球抢购分销系统",
    desc=u"全球抢购分销系统",
    static_path=static_path,
    template_path=template_path,
    cookie_secret='^e9060bd3a5987d638ac66399444117d1',
    login_url='/login.html',
    xsrf_cookies=True,
    debug=True,
    page_size=50,
)


admin_settings = dict(
    title=u"全球抢购分销系统后台",
    desc=u"全球抢购分销系统后台",
    static_path=static_path,
    template_path=template_path,
    cookie_secret='^e7482419870895eaa9a12d4f68c78ec9',
    login_url='/admin/login',
    xsrf_cookies=False,
    debug=True,
    page_size=50,
)

mobile_settings = dict(
    title=u"全球抢购分销系统app",
    desc=u"全球抢购分销系统app",
    static_path=static_path,
    template_path=template_path,
    cookie_secret='^e9060bd3a5987d638ac66399444117d1',
    login_url='/login.html',
    xsrf_cookies=False,
    debug=True,
    page_size=50,
)

# oss access key
ACCESS_ID = 'UN3OCE13y52qvQSr'
SECRET_ACCESS_KEY = 'HPbZa35JfJCKsiGSTb8B1PbPRmWufC'
IMG_BUCKET = 'qqqg'


OSS_HOST = "oss.aliyuncs.com"#OSS_HOST ="oss-cn-hangzhou-internal.aliyuncs.com"    online-inner dns


#ocs access key
OCS_ACCESS_URL = '5dd63cfeba764856.m.cnhzaliqshpub001.ocs.aliyuncs.com'
OCS_ACCESS_ID = ''
OCS_ACCESS_PASS = ''

# redis config
REDIS_HOST='127.0.0.1'
REDIS_PORT=6379

# redis config
MEMCACHE_HOST='127.0.0.1:11211'

#celery配置信息
#broker, backend
BACKEND_URL = 'redis://127.0.0.1:6379/2'

# BROKER_URL = 'amqp://guest:guest@localhost:5672//'
BROKER_URL = 'redis://127.0.0.1:6379/1'

#Database : Mysql
ENGINE="mysql://root:111111@127.0.0.1:3306/qqqg_fenxiao?charset=utf8"

DB_HOST = '127.0.0.1'
DB_PORT = 3306
DB_USER = 'root'
DB_PASSWD= ''
DB_NAME = 'fenxiao'
EV='TEST'
COOKIE_DOMAIN='qqqg.com'
PAYMENT_BACK_HOST='http://test.qqqg.com'
STATIC_DOMAIN='http://cdn.qqqg.com'
_basedir = os.path.abspath(os.path.dirname(__file__))
WHOOSH_INDEX = os.path.join(_basedir, 'qqqg.index')
DOCUMENTATION_PATH = os.path.join(_basedir, '../flask/docs/_build/dirhtml')

del os
