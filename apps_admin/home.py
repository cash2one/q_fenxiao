#encoding:utf-8
__author__ = 'wangjinkuan'

from common.base_handler import AdminBaseHandler,BaseHandler

class AdminHandler(AdminBaseHandler):
    def get(self,html_name=None):

        # render_html = 'admin/index.html'
        # if html_name:
        #     render_html = 'admin/'+html_name
        self.echo('admin/index.html',layout='admin/base.html')

class HomeHandler(AdminBaseHandler):

    def get(self, path, **kwargs):
        self.echo('admin/index.html',layout='admin/base.html')


class IndexHandler(BaseHandler):
    def get(self,**kwargs):
        host = self.request.headers.get('host')
        if host=='fenxiao.admin.qqqg.com':
            self.redirect("http://fenxiao.admin.qqqg.com/admin/index")
        elif host=='fenxiao.drp.qqqg.com':
            self.redirect("http://fenxiao.drp.qqqg.com/drp/index.html")
        elif host=='supply.drp.qqqg.com':
            self.redirect("http://fenxiao.supply.qqqg.com/supply/index.html")


class TmsHandler(BaseHandler):

    def get(self,path,**kwargs):
        self.echo(path)