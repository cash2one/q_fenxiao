#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'binpo'

from models.user_do import DistributorUser
from services.base_services import BaseService
from utils.md5_util import create_md5
from sqlalchemy.sql.expression import select, desc
from sqlalchemy import func, or_
from datetime import datetime
import uuid

class DistributorUserServices(BaseService):


    def add_distributor_user(self,username,password,phone,nick,role_type=0):
        distrib_user = DistributorUser()
        distrib_user.uid = str(uuid.uuid4())
        distrib_user.role_type = role_type
        distrib_user.nick = nick
        distrib_user.phone = phone
        distrib_user.user_name = username
        distrib_user.user_pwd = self.user_passed(password)
        # self.db.add(distrib_user)
        self.db.add(distrib_user)
        self.db.flush()
        distrib_user.shop_id = self.set_show_id_by_id(distrib_user.id)
        self.db.add(distrib_user)
        self.db.commit()


    def _login(self,**kargs):
        '''
        用户登录
        :param kargs:
        :return:
        '''
        from sqlalchemy import or_
        username = kargs.get('username')
        password = kargs.get('password')
        user = self.rdb.query(DistributorUser).filter(DistributorUser.deleted==0,DistributorUser.user_pwd==self.user_passed(password)).filter(or_(DistributorUser.user_name==username,DistributorUser.phone==username)).scalar()
        return user


    def delete_by_id(self,user_id):
        """
        :todo 根据id删除用户
        :param user_id 用户ID
        """
        if user_id:
            user = self.db.query(DistributorUser).filter_by(id=user_id).first()
            user.deleted=True
            self.db.commit()

    def user_uid(self,**kargs):
        """
        :todo 生成uuid
        :param name 用户名 如果是手机注册用手机号  微信注册用微信号
        """
        uuid_str = uuid.uuid4()
        return str(uuid_str)

    def user_passed(self,passowrd):
        '''
        生成密码
        :param uid:
        :param passowrd:
        :return:
        '''
        return create_md5(create_md5(create_md5(passowrd)))

    def check_passwd_by_username(self,name,passwd):
        user = self.rdb.query(DistributorUser).filter(DistributorUser.deleted==0).filter(DistributorUser.user_name==name).first()
        if user:
            if user.user_pwd == self.user_passed(passwd):
                return user
        return False

    def get_user_by_query(self,query):
        user_array=[]
        for user_info in query:
            user = self.db.query(DistributorUser).filter(DistributorUser.id == user_info.user_id,DistributorUser.deleted==0).scalar()
            user_array.append(user)
        return user_array

    def get_user_by_id(self,user_id):

        """根据id查询用户
        :param user_id 用户ID
        """
        return self.rdb.query(DistributorUser).filter(DistributorUser.id ==user_id).scalar()


    def user_login(self,**kargs):
        '''
            用户登录
        '''
        from sqlalchemy import or_
        username = kargs.get('username')
        password = kargs.get('password')
        user = self.rdb.query(DistributorUser).filter(DistributorUser.deleted==0,DistributorUser.user_pwd==self.user_passed(password)).filter(or_(DistributorUser.user_name==username,DistributorUser.phone==username)).scalar()
        return user

    def get_user_by_username(self,username):
        user_obj = self.rdb.query(DistributorUser).filter(DistributorUser.deleted==0,DistributorUser.user_name==username).first()
        return user_obj

    def get_user_by_phone(self, phone):
        user_obj = self.rdb.query(DistributorUser).filter(DistributorUser.deleted==0,DistributorUser.phone==phone).first()
        return user_obj

    def update_user(self, user_id, **kargs):
        """
        更新用户对象
        :param user_id 用户ID
        """
        query = self.db.query(DistributorUser).filter(DistributorUser.deleted==0, DistributorUser.id==user_id)
        query.update(kargs)
        self.db.commit()
        return True,'设置成功'

    def query_DistributorUser(self,**qdict):

        """
        :todo 查询用户
        :param qdict 请求参数集合
        """
        #print qdict
        query = self.rdb.query(DistributorUser)
        if qdict.get('start_date',''):
            query = query.filter(DistributorUser.gmt_created>qdict.get('start_date'))
        if qdict.get('end_date',''):
           query = query.filter(DistributorUser.gmt_created<qdict.get('end_date'))
        if qdict.get('role',''):
            query = query.filter(DistributorUser.role_codes.like('%'+qdict.get('role')+'%'))
        if qdict.get('status')== '1':
            query = query.filter(DistributorUser.deleted == 1)
        else:
            query = query.filter(DistributorUser.deleted == 0)
        if qdict.get('phone',''):
            query = query.filter(DistributorUser.phone==qdict.get('phone'))
        # if qdict.get('search_text',''):
        #     content = qdict.get('search_text')
        #     if '@' in content:
        #         #.filter(Tags.tag_name.like('%hello%'))
        #         query = query.filter(DistributorUser.email.like('%'+content+'%'))
        #     elif is_chinese(content.decode('utf-8')):
        #         query = query.filter(DistributorUser.nick.like('%'+content+'%'))
        #     else:
        #         query = query.filter(or_(DistributorUser.nick.like('%'+content+'%'), DistributorUser.user_name.like('%'+content+'%')) )
        if qdict.get('reorder')=='asc':
            query = query.order_by(DistributorUser.last_visit.asc())
        else:
            query = query.order_by(DistributorUser.last_visit.desc())
        return query


    def user_format(self,user):
        keys = ['id','nick', 'qq','regist_from','sex', 'sign_text','status','uid','user_name','visit_times', 'weibo', 'weixin','is_bussiness']
        cookies={key:getattr(user,key) for key in keys}
        return cookies

    def change_pwd(self, id, old, new):
        user = self.db.query(DistributorUser.id, DistributorUser.user_pwd, DistributorUser.uid).filter(DistributorUser.deleted == 0, DistributorUser.id == id).first()
        if user[1] != self.user_passed(old):
            return '密码不正确'
        self.update_user(user[0], user_pwd=self.user_passed(new))
        return True

    def check_username_exist(self, user_name):
        return self.rdb.query(DistributorUser.id).filter(DistributorUser.user_name == user_name, DistributorUser.deleted == 0).scalar()

    def get_username_by_id(self, id):
        return self.rdb.query(DistributorUser.user_name).filter(DistributorUser.id == id, DistributorUser.deleted == 0).scalar()

    def get_user_cache_msg_by_id(self, id):
        '''
        获取用户存入缓存信息
        '''
        return self.rdb.query(DistributorUser.id,DistributorUser.nick,DistributorUser.photo,DistributorUser.user_name,DistributorUser.role_codes).filter(DistributorUser.id == id, DistributorUser.deleted == 0).first()

    def check_user_exist_by_id(self, id):
        return True  if self.rdb.query(DistributorUser.id).filter(DistributorUser.id == id, DistributorUser.deleted == 0).scalar() else False

    def reset_passwd(self,user_id,passoword):
        user = self.get_user_by_id(user_id)
        self.update_user(user_id, user_pwd=self.user_passed(passoword))

    def reset_passwd_by_phone(self,phone,passoword):
        user = self.get_user_by_phone(phone)
        self.update_user(user.id, user_pwd=self.user_passed(passoword))
        return self.get_user_by_phone(phone)

    def check_user_by_user_id(self,user_id):
        '''
        :todo 检测用户是否存在
        '''
        user = self.db.query(DistributorUser).filter(DistributorUser.deleted==0,DistributorUser.id==user_id).scalar()
        if user:
            return True
        else:
            return  False

    def create_user_by_weibo(self,user=None,**kargs):
        '''
        微博创建用户
        :param kargs:
        :return:
        '''
        if not user:
            user = DistributorUser()
            user.nick = kargs.get('nick','')
            user.photo = kargs.get('photo', '')
        uid = self.user_uid(user_name=kargs.get('weibo',''))
        user.uid = uid
        user.email = kargs.get('email','')
        user.phone = kargs.get('phone','')
        user.is_employee = kargs.get('is_employee',0)
        user.sex = kargs.get('sex','')
        user.weibo = kargs.get('weibo','')
        user.last_visit = datetime.now()
        user.last_visit_ip = kargs.get('last_visit_ip','')
        user.visit_times = kargs.get('visit_times',0)
        user.regist_from = kargs.get('regist_from','weibo')
        user.find_pw_url = kargs.get('find_pw_url','')
        user.status = kargs.get('status','normal')
        user.avatar = kargs.get('avatar','')
        user.sign_text = kargs.get('sign_text','')
        user.deleted = 0
        self.db.add(user)
        self.db.commit()
        return user


    def get_user_by_weibo(self,weibo_id):
        '''
        根据微博查询
        :param weibo_id:
        :return:
        '''
        return self.rdb.query(DistributorUser).filter(DistributorUser.deleted==0,DistributorUser.weibo==weibo_id).scalar()

    def create_user_by_qq(self,user=None,**kargs):
        if not user:
            user = DistributorUser()
            user.nick = kargs.get('nick','')
            user.photo = kargs.get('photo', '')
        uid = self.user_uid(user_name=kargs.get('qq',''))
        user.uid = uid
        user.email = kargs.get('email','')
        user.phone = kargs.get('phone','')
        user.is_employee = kargs.get('is_employee',0)
        user.sex = kargs.get('sex','')
        user.qq = kargs.get('qq','')
        user.last_visit = datetime.now()
        user.last_visit_ip = kargs.get('last_visit_ip','')
        user.visit_times = kargs.get('visit_times',0)
        user.regist_from = kargs.get('regist_from','qq')
        user.find_pw_url = kargs.get('find_pw_url','')
        user.status = kargs.get('status','normal')
        user.avatar = kargs.get('avatar','')
        user.sign_text = kargs.get('sign_text','')
        user.deleted = 0
        self.db.add(user)
        self.db.commit()
        return user


    def get_user_by_qq(self,qq):
        '''
        根据qq open ID获取用户
        :param qq:
        :return:
        '''
        return self.rdb.query(DistributorUser).filter(DistributorUser.deleted==0,DistributorUser.qq==qq).first()

    def get_role_id_by_role_code(self, code):
        '''
        :param code:
        :return:
        '''
        return self.rdb.query(Roles.id).filter(Roles.code == code).first()

    def get_user_by_weixin(self,open_id):
        '''
        根据open_id获取微信登陆用户
        :param open_id:
        :return:
        '''
        return self.rdb.query(DistributorUser).filter(DistributorUser.deleted==0,DistributorUser.weixin==open_id).first()

    def create_user_by_weixin(self,user=None,**kargs):
        if not user:
            user = DistributorUser()
            user.nick = kargs.get('nick','')
            user.photo = kargs.get('photo', '')

        uid = self.user_uid(user_name=kargs.get('weixin',''))
        user.uid = uid
        user.email = kargs.get('email','')
        user.phone = kargs.get('phone','')
        user.is_employee = kargs.get('is_employee',0)
        user.sex = kargs.get('sex','')==1 and '男' or '女'
        user.weixin = kargs.get('weixin','')
        user.last_visit = datetime.now()
        user.last_visit_ip = kargs.get('last_visit_ip','')
        user.visit_times = kargs.get('visit_times',0)
        user.regist_from = kargs.get('regist_from','weixin')
        user.find_pw_url = kargs.get('find_pw_url','')
        user.status = kargs.get('status','normal')
        user.avatar = kargs.get('avatar','')
        user.sign_text = kargs.get('sign_text','')
        user.deleted = 0
        self.db.add(user)
        self.db.commit()
        return user



    def set_DistributorUser_weixin_null_by_weixin_id(self,weixin_id,user_id):
        '''
        :todo 根据微信ID设置为空
        :param weixin_id:
        :return:
        '''
        self.db.query(DistributorUser).filter(DistributorUser.deleted==0,DistributorUser.weixin==weixin_id,DistributorUser.id!=int(user_id)).update({'weixin':''})
        self.db.commit()

    #---------------topic ---------------------

    def login_with_phone(self,phone,passwd):
        '''
        :todo 用户账号登陆
        :param phone:
        :param passwd:
        :return:
        '''
        user = self.rdb.query(DistributorUser).filter(DistributorUser.deleted==0,DistributorUser.phone==phone,DistributorUser.user_pwd==self.user_passed(passwd)).scalar()
        return user

    def login_with_username(self,user_name,passwd):
        '''
        :todo 用户名登陆
        :param user_name:
        :param passwd:
        :return:
        '''
        user = self.rdb.query(DistributorUser).filter(DistributorUser.deleted==0,DistributorUser.user_name==user_name,DistributorUser.user_pwd==self.user_passed(passwd)).scalar()
        return user


    def batch_user(self,data):
        '''
        todo:批量添加大客户
        :param data:
        :return:
        '''
        user_ids = []
        for key in data:
            query = self.db.query(DistributorUser).filter(DistributorUser.deleted == 0,DistributorUser.id == key)
            query.update({'is_bussiness':1})
            user_ids.append(key)
        self.db.commit()
        return True,user_ids