#encoding:utf-8
__author__ = 'binpo'

from ..base_services import BaseService
from models.user_do import UserFans,UserFocus

class UserSnsService(BaseService):

    def focus(self,user_id,focus_user_id):
        '''
        :todo 关注用户
        :param user_id:
        :param focus_user_id:
        :return:
        '''
        try:
            focus_table=UserFocus()
            focus_table.focus_user_id=focus_user_id
            focus_table.user_id=user_id
            focus_table.deleted=0
            self.db.add(focus_table)
            self.db.commit()
            return 'ok'
        except:
            return 'error'

    def unfocus(self,user_id,unfocus_user_id):
        '''
        :todo 取消关注
        :param user_id:
        :param unfocus_user_id:
        :return:
        '''
        try:
            self.db.query(UserFocus).filter(UserFocus.focus_user_id==unfocus_user_id,UserFocus.user_id==user_id).delete()
            self.db.commit()
            return 'ok'
        except Exception,e:
            print e
            return 'error'

