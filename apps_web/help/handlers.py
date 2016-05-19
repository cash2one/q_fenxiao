#encoding:utf-8
__author__ = 'binpo'
from common.base_handler import BaseHandler

class HelpHandlers(BaseHandler):

    def get(self,html, **kwargs):
        path='help/'+html+'.html'
        self.echo(path,{'parent_category_id':''})
        #self.write('ok')

    def post(self, *args, **kwargs):
        pass

