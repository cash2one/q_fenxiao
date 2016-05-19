#encoding:utf-8
__author__ = 'binpo'

from common.base_handler import AdminBaseHandler

from utils.datetime_util import datetime_format
from setting import *
from utils.upload_utile import upload_to_oss
from tornado.options import options

from services.systems.apps_service import AppsServices
from services.users.user_services import UserServices

app_service = AppsServices()

class SystemIndexHandler(AdminBaseHandler):

    def get(self):
        self.echo('admin/system/index.html')


class SystemAppsUploadHandler(AdminBaseHandler):

    def get(self, *args, **kwargs):
        self.echo('admin/system/upload_apps.html')

    def post(self, *args, **kwargs):

        self.get_paras_dict()
        #print self.qdict
        #file_metas=self.request.files.get('appszip')       #提取表单中‘name’为‘file’的文件元数据
        data = {}
        size = 0
        try:
            file_prex = 'apps/'+datetime_format(format="%Y%m%d%H%M")
            is_ok,filenames = upload_to_oss(self,options.APPS_BUCKET,param_name='appzip',file_type=None,file_prex=file_prex)

            print is_ok,filenames

            if is_ok:
                request_url = filenames[0].get('full_name')
                size = filenames[0].get('size')
            else:
                message = filenames

        except Exception,e:
            raise
            data['error']=1
            data['message']=e.message
            data['url']=''

        data['error'] = is_ok
        data['message'] = '发功成功'
        data['url'] = request_url
        data['size'] = size
        data['file_name'] = filenames[0].get('file_name')
        app_service.set_db(self.db)
        app = app_service.create_apps_version(data,self.qdict)
        if app:
            self.write('upload success')
        else:
            self.write('upload fail')

class SystemAppsQueryHandler(AdminBaseHandler):

    def get(self, *args, **kwargs):
        app_service.set_rdb(self.rdb)
        apps = app_service.query_all()
        self.echo('admin/system/apps_list.html',
            {'apps':apps}
        )

    def post(self, *args, **kwargs):
        pass

import ujson
class SystemLoginHandler(AdminBaseHandler):

    def get(self):
        self.echo('admin/admin_login.html')

    def post(self, *args, **kwargs):
        phone = self.get_argument('phone')
        user_service = UserServices()
        user_service.set_rdb(self.rdb)
        user = user_service.get_user_by_phone(phone)
        if user:
            from setting import settings,admin_settings
            self.application.settings['cookie_secret'] = settings.get('cookie_secret')
            self.set_secure_cookie('loginuser',ujson.dumps(user.user_format(user)),domain=self.cookie_domain,expires_days=1)#(ujson.dumps(user.user_format(user)))
            self.application.settings['cookie_secret'] = admin_settings.get('cookie_secret')
            self.write('<h1>{0}已经登录</h1>'.format(phone))
        else:self.write('<h1>{0}用户不存在</h1>'.format(phone))

import httplib
import logging
import urllib

def http_api(url,para,action,method="POST",json=None,accept="text/plain"):
    """
    url 调用的host
    para参数 以字典的形式
    action  调用的地址
    accept 参数接受的形式
    """
    conn = None
    try:
        params = urllib.urlencode(para)
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept":accept,'Authorization': 'Basic cm9vdEBkdWJibzpoZWxsMDVh'}
        conn = httplib.HTTPConnection(url)
        if json:
            conn.request(method,action,body=json,headers=headers)
        else:
            conn.request(method,action,params,headers=headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        print data
        return data
    except Exception,e:
        print e.message
    finally:
        if conn:
            conn.close()

# #data ={u'status': u'SUCCESS', u'remark': u'', u'totalRefundCount': u'0', u'serialNumber': u'c2aa8c10077e453db220f3cd6f319193', u'completeDateTime': u'2015-11-25 17:02:51', u'hmac': u'2ad6e6a98e77158229a50cf4ca72e97c', u'requestId': u'11144844184908', u'orderAmount': u'40500', u'orderCurrency': u'CNY', u'merchantId': u'120140267', u'totalRefundAmount': u'0'}
# data = {u"status":u"SUCCESS",u"remark":"",u"totalRefundCount":"0",u"serialNumber":u"a34a1072bad742e491be5049d29bdf2c",u"completeDateTime":u"2015-11-26 22:31:20",u"merchantId":u"120140267",u"requestId":u"51144854803074",u"orderAmount":u"37500",u"orderCurrency":u"CNY",u"hmac":u"d954fd199e9057204c80b850172a7c45",u"totalRefundAmount":u"0"}
# data1 = {u"status":u"SUCCESS",u"remark":"",u"totalRefundCount":"0",u"serialNumber":u"7b7708c3ac084e1d8fa612346ffcfa97",u"completeDateTime":u"2015-11-26 22:22:59",u"merchantId":u"120140267",u"requestId":u"51144854758733",u"orderAmount":u"37500",u"orderCurrency":u"CNY",u"hmac":u"10a6e4691ac756efbab5e2b8ac2743ae",u"totalRefundAmount":u"0"}
#
import ujson
import requests

class PayDealHandler(AdminBaseHandler):

    def get(self):
        self.echo('admin/system/pay_deal.html')

    def post(self, *args, **kwargs):
        self.get_paras_dict()
        data = self.qdict
        pay_type = data.get('pay_type')
        content = data.get('content')
        log_content = ujson.loads(content)
        # print type(content)
        # print content
        if pay_type=='8':
            jsondata=ujson.dumps(log_content)
            req = http_api('www.qqqg.com',{},'/order/ehking/payback/1/51144854803074.html',json=jsondata)
            self.write(req)
        elif pay_type=='7':
            url = 'http://www.qqqg.com/order/allinpay/payback/12/1212.html'
            req = requests.post((url),data=log_content,timeout=3 , verify=False)
            req.read()
            self.write(req.content)
