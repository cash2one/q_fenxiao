#encoding:utf-8
__author__ = 'gaoaifei'


from common.base_handler import AdminBaseHandler
from services.users.user_services import UserServices
from conf.user_conf import USER_STATUS
import sys
import json
import ujson
from common.asyn_wrap import unblock
from services.distributor.distributor_service import DistributorUserservice

user_service = UserServices()
distributor_service = DistributorUserservice()

# 会员列表 查看 删除
class Userhandlers(AdminBaseHandler):
    def get(self, operation=None, *args, **kwargs):
        if operation == 'edit':
            self.get_paras_dict()
            id = self.qdict.get('id','')
            user_service.set_rdb(self.rdb)
            data = user_service.get_user_by_id(id)
            self.echo('admin/users/edit.html',{
                      'data':data,
            })
        else:
            self.get_paras_dict()
            start_date = self.qdict.get('start_date','')
            end_date = self.qdict.get('end_date','')
            status = self.qdict.get('status','0')
            reorder = self.qdict.get('reorder','')
            phone = self.qdict.get('phone','')
            belong_id = self.qdict.get('belong_id')
            distributor_service.set_rdb(self.rdb)
            distributors = distributor_service.get_all_distributor_users(type=0)
            user_service.set_rdb(self.rdb)
            query = user_service.query_users(**self.qdict)
            data = self.get_page_data(query)
            if self.request.uri.startswith('/admin/users/mobile'):
                self.echo('admin/mobile/user/list.html',{
                    'data':data,
                    'start_date':start_date,
                    'end_date':end_date,
                    'status':status,
                    'reorder':reorder,
                    'phone':phone,
                    'USER_STATUS':USER_STATUS,
                },layout='')
            else:
                self.echo('admin/users/list.html',{
                    'data':data,
                    'start_date':start_date,
                    'end_date':end_date,
                    'status':status,
                    'reorder':reorder,
                    'phone':phone,
                    'USER_STATUS':USER_STATUS,
                    'count':query.count(),
                    'distributors':distributors,
                    'belong_id':belong_id
                })

    def delete(self,operation=None, *args, **kwargs):
        self.get_paras_dict()
        id = self.qdict.get('id')
        if operation == 'renew':
            deleted = 0
        else:
            deleted = 1
        try:
            user_service.set_db(self.db)
            user_service.delete_user(id,deleted)
            self.write_json({'state':'200','info':'success'})
        except Exception,e:
            self.captureException(sys.exc_info())
            self.write_json({'state':'400','info':e.message})

# 查看会员收货地址列表
class Addresshandlers(AdminBaseHandler):

    def get(self, *args, **kwargs):
        self.get_paras_dict()
        user_id = self.qdict.get('user_id')
        user_service.set_rdb(self.rdb)
        data = user_service.get_address(user_id)
        self.echo('admin/users/user_address.html',{'data':data})

class BusinessHandler(AdminBaseHandler):
    def get(self,operation=None,*args, **kwargs):
        self.echo('admin/users/batch_business.html')

    def post(self,operation=None,*args, **kwargs):
        data = self.get_argument('data','')
        user_service.set_db(self.db)
        if operation == 'batch':
            data = data.split(',')
            is_success,user_ids = user_service.batch_user(data)
            if is_success:
                for user_id in user_ids:
                    user_cache_key = 'user_login_cookie_'+str(user_id)
                    self.mcache.delete(user_cache_key)
                self.write_json({'stat':'success','info':'设置成功','data':''})
        else:
            dict = {}
            dict['is_bussiness'] = int(self.get_argument('is_bussiness'))
            is_success,info = user_service.update_user(data,**dict)
            if is_success:
                user_cache_key = 'user_login_cookie_'+str(data)
                self.mcache.delete(user_cache_key)
                self.write_json({'stat':'success','info':info,'data':''})





