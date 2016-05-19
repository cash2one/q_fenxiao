#encoding:utf-8
__author__ = 'binpo'
from common.base_handler import AdminBaseHandler
from services.logs.logs_services import LogsServices
from models.logs_do import Tasks
from common.asyn_wrap import unblock
import requests

class TaskHandlers(AdminBaseHandler):

    def get(self):
        logs_service = LogsServices(rdb=self.rdb)
        status = self.get_argument('status','')
        logs_type = self.get_argument('logs_type','')
        key_params = self.get_argument('key_params','')
        start_time = self.get_argument('start_time','')
        end_time = self.get_argument('end_time','')
        query = logs_service.task_list(status=status,task_type=logs_type,key_params=key_params)
        data = self.get_page_data(query)
        self.echo('admin/tasks/tasks.html',{'data':data,'status':status,'logs_type':logs_type,'key_params':key_params,
                                              'start_time':start_time,
                                              'end_time':end_time})


    def post(self, *args, **kwargs):
        pass

import ujson

class TaskDealHandler(AdminBaseHandler):

    @unblock
    def get(self,task_id, **kwargs):
        task = self.db.query(Tasks).filter(Tasks.id==task_id,Tasks.status==0).scalar()
        # task_type = Column(SmallInteger,doc='任务类型')     #1.悦华清关接口  2.物流接口 3.回调接口
        # key_params = Column(Text,doc='关键参数',default='')
        # _url = Column(String(512),doc='请求URL')
        # params = Column(Text,doc='请求参数')
        # action = Column(String(32),doc='方法类型')      #post  get
        # result = Column(Text,doc='返回值')
        # status = Column(SmallInteger,doc='状态值')     #0:待执行 1.自动执行， 2:手动执行
        # error = Column(String(2048),doc='错误信息')    #执行错误信息记录 做容错处理

        if task:
            if task.task_type==1:
                pass
            elif task.task_type==2:
                pass
            elif task.task_type==3:
                data = ujson.loads(task.params)
                req = requests.post((task._url),data=data,timeout=3 , verify=False)
                result = req.content
                task.result = result
                task.status = 1
                self.db.add(task)
                self.db.commit()

