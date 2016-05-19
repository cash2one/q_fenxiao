#encoding:utf-8
__author__ = 'binpo'

from common.base import BaseHandler
from utils.datetime_util import datetime_format
from utils.md5_util import create_md5

MAIL_TEMPLATE = {'reg':'view/message/register.html',
                 'reset_passwd':'view/message/reset_passwd.html',
                 }
class EmailHandler(BaseHandler):

    def get(self,mail_type):
        token = self.get_argument('token')
        date_str = datetime_format(format='%Y-%m-%d')
        token_result = create_md5(''.join(['zenmez_email',date_str,mail_type]))
        if token==token_result:
            self.echo(MAIL_TEMPLATE.get(mail_type),layout='')
        else:
            return self.write('ok')


    # def post(self):
    #     pass

