#encoding:utf-8
__author__ = 'gaoaifei'

from ..base_handler import DrpBaseHandler
from services.users.user_services import UserServices
from conf.user_conf import USER_STATUS
import sys
from models.user_do import Users

user_service = UserServices()

# 会员列表 查看 删除
class Userhandlers(DrpBaseHandler):
    def get(self, operation=None, *args, **kwargs):
        self.get_paras_dict()
        start_date = self.qdict.get('start_date','')
        end_date = self.qdict.get('end_date','')
        phone = self.qdict.get('phone','')
        user_service.set_rdb(self.rdb)
        self.qdict['belong_id'] = self.current_user.get('id')
        query = user_service.query_users(**self.qdict)
        data = self.get_page_data(query)
        self.echo('admin_drp/users/list.html',{
                'data':data,
                'start_date':start_date,
                'end_date':end_date,
                'phone':phone,
                'count':query.count()
            })

class UserAddHandler(DrpBaseHandler):
    def get(self, *args, **kwargs):
        self.get_paras_dict()
        user_id = self.qdict.get('user_id',None)
        if user_id:
            user_service.set_rdb(self.rdb)
            user = user_service.get_user_by_id(user_id)
        else:
            user = Users()
        self.echo('admin_drp/users/edit.html',{'user':user})

    def post(self, *args, **kwargs):
        self.get_paras_dict()
        user_service.set_db(self.db)

        # user.belong_id = kargs.get('belong_id')
        # user.nick = kargs.get('nick','').strip()
        # user.email = kargs.get('email','').strip()
        # user.phone = kargs.get('phone','').strip()
        # user.photo = kargs.get('photo', '')
        # user.user_name = kargs.get('user_name','').strip()
        # user.user_pwd = self.user_passed(kargs.get('user_pwd')).strip()
        user_service._add(belong_id=self.current_user.get('id'),
                          nick=self.qdict.get('nick'),
                          real_name=self.qdict.get('real_name'),
                          phone=self.qdict.get('phone'),
                          user_name=self.qdict.get('phone'),
                          user_pwd=self.qdict.get('user_pwd'))
        self.redirect(self.reverse_url('drp_users'))

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

