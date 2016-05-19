#encoding:utf-8
__author__ = 'binpo'
from models.logs_do import ApiLogs,Tasks
from ..base_services import BaseService

class LogsServices(BaseService):

    def new_api_logs(self,**kwargs):
        '''

        :param kwargs:
        :return:
        '''
        api_logs = ApiLogs()

        api_logs.logs_type = kwargs.get('logs_type','')
        api_logs.key_params = kwargs.get('key_params','')
        api_logs.reqeust_url = kwargs.get('reqeust_url','')
        api_logs.params = kwargs.get('params','')
        api_logs.action = kwargs.get('action','')
        api_logs.result = kwargs.get('result','')
        api_logs.status = kwargs.get('status',0)
        api_logs.error = kwargs.get('error','')
        self.db.add(api_logs)
        self.db.commit()
        return api_logs

    def operation_logs(self,**kwargs):
        pass

    def _list(self,**kwargs):
        '''
        查询所有接口调用记录
        :param kwargs:
        :return:
        '''
        query = self.rdb.query(ApiLogs).filter(ApiLogs.deleted==0)
        if kwargs.get('logs_type',''):
            query = query.filter(ApiLogs.logs_type==kwargs.get('logs_type'))
        if kwargs.get('status',''):
            query = query.filter(ApiLogs.status==kwargs.get('status'))
        if kwargs.get('start'):
            query = query.filter(ApiLogs.gmt_created>=kwargs.get('start')+' 00:00:00')
        if kwargs.get('end'):
            query = query.filter(ApiLogs.gmt_created<=kwargs.get('end')+' 23:59:59')
        if kwargs.get('key_params',''):
            query = query.filter(ApiLogs.key_params.like('%'+kwargs.get('key_params')+'%'))
        if kwargs.get('order_by'):
            query = query.order_by(kwargs.get('order_by'))
        else:
            query = query.order_by(ApiLogs.gmt_created.desc())
        return query

    def _update(self,log_id,**kwargs):
        '''
        todo:更新日志
        :param log_id:
        :param kwargs:
        :return:
        '''
        query = self.db.query(ApiLogs).filter(ApiLogs.deleted == 0,ApiLogs.id == log_id)
        query.update(kwargs)
        self.db.commit()

    def create_task(self,**kwargs):
        '''
        生成任务
        :param kwargs:
        :return:
        '''
        tasks = Tasks()
        tasks.task_type = kwargs.get('task_type','')
        tasks.key_params = kwargs.get('key_params','')
        tasks._url = kwargs.get('reqeust_url','')
        tasks.params = kwargs.get('params','post')
        tasks.action = kwargs.get('action','')
        tasks.result = kwargs.get('result','')
        tasks.status = kwargs.get('status',0)
        tasks.error = kwargs.get('error')
        self.db.add(tasks)
        self.db.commit()

    def task_list(self,**kwargs):
        '''
        任务记录
        :param kwargs:
        :return:
        '''
        query = self.rdb.query(Tasks).filter(Tasks.deleted==0)
        if kwargs.get('logs_type',''):
            query = query.filter(Tasks.task_type==kwargs.get('task_type'))
        if kwargs.get('status',''):
            query = query.filter(Tasks.status==kwargs.get('status'))
        if kwargs.get('key_params',''):
            query = query.filter(Tasks.key_params.like('%'+kwargs.get('key_params')+'%'))
        if kwargs.get('order_by'):
            query = query.order_by(Tasks.get('order_by'))
        else:
            query = query.order_by(Tasks.gmt_created.desc())
        return query
