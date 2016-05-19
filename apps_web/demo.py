#encoding:utf-8
__author__ = 'binpo'

from common.base_handler import BaseHandler
from common.asyn_wrap import unblock
import time
from models.orders_do import PayOrders

class CommonHandler(BaseHandler):
    '''
        普通请求处理
        tornado 完美支持restful 接口
        常用 get post put delete四种方法
        最常用 get和post
        重写四中方法即可
    '''

    def get(self, *args, **kwargs):
        # self.set_cache(10,is_privacy='OK')
        # print 'cache 数据'
        pay_order = self.db.query(PayOrders).first()
        order_api = YhOrderApi(self.db)
        order_api.create_order_params(pay_order)
        order_api.send_order_to_yh()
        self.cache_echo('index.html')

    def post(self, *args, **kwargs):

        self.echo('index.html')

    def put(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        pass

'''返回json'''
class JsonHandler(BaseHandler):

    def get(self, *args, **kwargs):
        from models.express_do import InvoiceOrders
        invoice_order= self.db.query(InvoiceOrders).filter(InvoiceOrders.id==1).scalar()
        #invoice_order = InvoiceOrders()
        invoice_order.invoice_no = '121212'
        invoice_order.order_id = 1212
        invoice_order.order_no = 'dsdsd'
        invoice_order.province = 'dsdsdsd'
        invoice_order.city = 'sdsd'
        invoice_order.county = 'sdsds'
        invoice_order.zip = 'sdsd'
        invoice_order.addr = 'sdsdsd'
        invoice_order.mobile = 'sdsdsd'
        invoice_order.express_no = 'sdsds'
        invoice_order.express_company_id = 1
        invoice_order.status = 2
        invoice_order.express_content =  'dsdsds'
        invoice_order.remark = 'sdsdsd'
        self.db.add(invoice_order)
        self.db.commit()
        print 'ok'
        self.write_json({'json':'this is the tornado webframword json response'})

    def post(self, *args, **kwargs):
        self.write_json({'json':'this is the tornado webframword json response with '})

'''非阻塞试请求处理,解决高并发请求'''
class AsynHandler(BaseHandler):

    @unblock
    def get(self, *args, **kwargs):
        return self.render('index.html')

    @unblock
    def post(self, *args, **kwargs):
        return self.render('index.html')

    def put(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        pass

import tornado
class AvatarHandlerSample(tornado.web.RequestHandler):
    @tornado.web.asynchronous#使用异步的请求
    def get(self):#GET请求
        HttpClient = tornado.httpclient.AsyncHTTPClient()#使用AsyncHTTPClient
        avatarLink = 'http://127.0.0.1:8080'
        HttpClient.fetch(avatarLink, callback = self.callback)#去取回（Fetch的英文意思）这个URL的内容，并在返回后将响应送到callback函数

    def callback(self, response):#接受响应
        if response.error:#如果出现错误
            print(response.error)
            raise tornado.web.HTTPError(response.code)#终止并返回错误
        avatar = response.body#获取头像
        #self.set_header('Content-Type', response.headers.get('content-type'))#设置文件头（告诉浏览器这是一张图片）
        self.write(avatar)#发送头像
        self.finish()#完成请

