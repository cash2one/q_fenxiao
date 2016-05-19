#encoding:utf-8
__author__ = 'binpo'

from common.base_handler import AdminBaseHandler
from services.logs.logs_services import LogsServices

class ApiHandlers(AdminBaseHandler):

    def get(self, *args, **kwargs):
        logs_service = LogsServices(rdb=self.rdb)
        status = self.get_argument('status','')
        logs_type = self.get_argument('logs_type','')
        key_params = self.get_argument('key_params','')
        start_time = self.get_argument('start_time','')
        end_time = self.get_argument('end_time','')
        query = logs_service._list(status=status,logs_type=logs_type,key_params=key_params,start=start_time,end=end_time)
        data = self.get_page_data(query)
        self.echo('admin/logs/api_logs.html',{'data':data,'status':status,'logs_type':logs_type,'key_params':key_params,
                                              'start_time':start_time,
                                              'end_time':end_time})

    def post(self, *args, **kwargs):
        pass

