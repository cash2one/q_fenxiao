__author__ = 'yijiaren-sun'
from base_handler import BaseHandler

class NotFoundHandler(BaseHandler):
    def get(self):
        self.echo('view/login/404.html', layout='')

class InternalErrorHandler(BaseHandler):
    def get(self):
        self.echo('view/login/500.html', layout='')