#encoding:utf-8
__author__ = 'gaoaifei'
from common.base_handler import MobileBaseHandler

class HelpHandlers(MobileBaseHandler):

    def get(self,html, **kwargs):
        path='help/'+html+'.html'
        self.echo(path,{'parent_category_id':''})
        #self.write('ok')

    def post(self, *args, **kwargs):
        pass


class PaymentHandlers(MobileBaseHandler):
    def get(self, *args, **kwargs):
        self.echo('mobile/help/agreement.html')

