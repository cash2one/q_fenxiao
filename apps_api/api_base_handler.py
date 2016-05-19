#encoding:utf-8
__author__ = 'binpo'

from common.base_handler import BaseHandler
from services.logs.logs_services import LogsServices
import ujson

log_service = LogsServices()

class ApiBaseHandler(BaseHandler):

    def check_xsrf_cookie(self):
        pass

    # def prepare(self):
    #     self.get_paras_dict()
    #     print self.qdict
    #     data = {}
    #     data['key_params'] = self.qdict.get('order_no')
    #     data['params'] = ujson.dumps(self.qdict)
    #     data['logs_type'] = 2
    #     data['reqeust_url'] = self.request.full_url()
    #     data['action'] = self.request.method
    #     log_service.set_db(self.db)
    #     api_logs = log_service.new_api_logs(**data)
    #     self.log_id = api_logs.id
    #
    # def on_finish(self):
    #     data = {}
    #     if self.stat == 'success':
    #         data['status'] = 1
    #     else:
    #         data['status'] = 0
    #     data['result'] = self.stat
    #     log_service.set_db(self.db)
    #     log_service._update(self.log_id,**data)








