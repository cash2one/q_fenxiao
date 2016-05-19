#encoding:utf-8
'''
Created on 2014-10-15

@author: qiuyan.zwp
'''

from models.user_do import *
from models.admin_do import *
from models.orders_do import *
from services.base_services import BaseService
from utils.md5_util import create_md5
from sqlalchemy.sql.expression import select, desc
from sqlalchemy import func, or_
from datetime import datetime
from services.locations.location_services import LocationServices
import copy

import uuid

class UserServices(BaseService):


    def query_role_list(self,id_list=None):
        if not id_list:
            self.role_list = self.rdb.query(Roles)
        else:self.role_list = self.rdb.query(Roles).filter(Roles.id.in_(id_list))
     
    def _add(self,*args,**kargs):

        is_params_ok,info = self.adduser_check_params(**kargs)
        if not is_params_ok:
            return is_params_ok,info
        is_exist,user = self.registe_check_exist(**kargs)
        if is_exist:
            return False,user

        user = Users()
        uid = self.user_uid(**kargs)
        user.uid = uid
        user.belong_id = kargs.get('belong_id')
        user.nick = kargs.get('nick','').strip()
        user.email = kargs.get('email','').strip()
        user.phone = kargs.get('phone','').strip()
        user.photo = kargs.get('photo', '')
        user.user_name = kargs.get('user_name','').strip()
        user.user_pwd = self.user_passed(kargs.get('user_pwd')).strip()
        user.real_name = kargs.get('real_name','')
        user.sex = kargs.get('sex','')
        user.weibo = kargs.get('weibo','')
        user.weixin = kargs.get('weixin','')
        user.taobao = kargs.get('taobao','')
        user.qq = kargs.get('qq','')
        user.last_visit = datetime.now()
        user.last_visit_ip = kargs.get('last_visit_ip','')
        user.visit_times = kargs.get('visit_times',0)
        user.regist_from = kargs.get('regist_from','web')
        user.find_pw_url = kargs.get('find_pw_url','')

        user.user_type = kargs.get('user_type',0)
        user.find_pw_expire_time = kargs.get('find_pw_expire_time',None)
        user.birthday = kargs.get('birthday',None)
        user.auto_repost = kargs.get('auto_repost',None)
        user.promoted_type = kargs.get('promoted_type',None)
        user.status = kargs.get('status','normal')
        user.avatar = kargs.get('avatar','')
        user.vip_info = kargs.get('vip_info','')
        user.sign_text = kargs.get('sign_text','')
        self.db.add(user)
        self.db.commit()

        return True,user


    def adduser_check_params(self,**kargs):
        if not kargs.get('user_name',None) and not kargs.get('email',None) and not kargs.get('phone',None):
            return  False,u'参数不正确'
        return True,''

    def delete_by_id(self,user_id):
        """
        :todo 根据id删除用户
        :param user_id 用户ID
        """
        if user_id:
            user = self.db.query(Users).filter_by(id=user_id).first()
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
        user = self.rdb.query(Users).filter(Users.deleted==0).filter(Users.user_name==name).first()
        if user:
            if user.user_pwd == self.user_passed(passwd):
                return user
        return False


    def add_user_roles(self,user_id,roles):

        """用户添加角色"""
        if roles:
            for r in roles:
                userRoles = UserRoles()
                userRoles.user_id = user_id
                userRoles.role_id = r
                self.db.add(userRoles)
            self.db.commit()


    def get_user_by_query(self,query):
        user_array=[]
        for user_info in query:
            user = self.db.query(Users).filter(Users.id == user_info.user_id,Users.deleted==0).scalar()
            user_array.append(user)
        return user_array

    def get_user_by_id(self,user_id):

        """根据id查询用户
        :param user_id 用户ID
        """
        return self.rdb.query(Users).filter(Users.id ==user_id).scalar()

    def get_user_roles(self,user):
        """
            获取用户角色
        """
        user_role_q = select([UserRoles.role_id]).where(UserRoles.user_id==user.id).alias()
#        print   user_role_q
#        print dir(user_role_q)
        user_roles = self.db.query(Roles).join(user_role_q,user_role_q.c.role_id==Roles.id)
        return user_roles
    
    def registe_check_exist(self,**kargs):

        """注册检测  用户名手机是否已经被占用
        """
        if kargs.get('user_name')and self.db.query(Users).filter(Users.deleted==0,Users.user_name == kargs.get('user_name')).count()>0:
            return True,'用户名:'+kargs.get('user_name')+' 已经存在'
        if kargs.get('email') and self.db.query(Users).filter(Users.deleted==0,Users.email == kargs.get('email')).count()>0:
            return True,'邮箱:'+kargs.get('email')+' 已经存在'
        if kargs.get('phone') and self.db.query(Users).filter(Users.deleted==0,Users.phone == kargs.get('phone')).count()>0:
            return True,'手机号:'+kargs.get('phone')+' 已经存在'
        return False,''
    
    def user_login(self,**kargs):
        '''
            用户登录
        '''
        from sqlalchemy import or_
        username = kargs.get('username')
        password = kargs.get('password')
        user = self.rdb.query(Users).filter(Users.deleted==0,Users.user_pwd==self.user_passed(password)).filter(or_(Users.user_name==username,Users.phone==username)).scalar()
        return user


    def get_user_by_username(self,username):
        user_obj = self.rdb.query(Users).filter(Users.deleted==0,Users.user_name==username).first()

        return user_obj



    def get_user_by_phone(self, phone):
        user_obj = self.rdb.query(Users).filter(Users.deleted==0,Users.phone==phone).first()
        return user_obj

    def update_user(self, user_id, **kargs):
        """
        更新用户对象
        :param user_id 用户ID
        """
        query = self.db.query(Users).filter(Users.deleted==0, Users.id==user_id)
        query.update(kargs)
        self.db.commit()
        return True,'设置成功'

    def query_users(self,**qdict):

        """
        :todo 查询用户
        :param qdict 请求参数集合
        """
        #print qdict
        query = self.rdb.query(Users)
        if qdict.get('start_date',''):
            query = query.filter(Users.gmt_created>qdict.get('start_date'))
        if qdict.get('end_date',''):
           query = query.filter(Users.gmt_created<qdict.get('end_date'))
        if qdict.get('role',''):
            query = query.filter(Users.role_codes.like('%'+qdict.get('role')+'%'))
        if qdict.get('status')== '1':
            query = query.filter(Users.deleted == 1)
        else:
            query = query.filter(Users.deleted == 0)
        if qdict.has_key('belong_id'):
            query = query.filter(Users.belong_id==qdict.get('belong_id'))
        if qdict.get('phone',''):
            query = query.filter(Users.phone==qdict.get('phone'))
        if qdict.get('reorder')=='asc':
            query = query.order_by(Users.last_visit.asc())
        else:
            query = query.order_by(Users.last_visit.desc())
        return query

    def get_roles(self,cache_name):
        """
        查询数据cache
        """
        return self.db.query(Roles.id,Roles.name).all()

    def set_user_roles(self,user_id,roles):
        """
        :todo 用户授权
        :param user_id 用户ID
        :param roles 角色列表
        """
        self.db.query(UserRoles).filter(UserRoles.user_id).filter(UserRoles.role_id.in_(roles)).delete(synchronize_session=False)
        roles_ = self.db.query(Roles).filter(Roles.id.in_(roles)).all()
        self.db.query(Users).filter(Users.id == user_id).update({'role_codes':','.join([r.code for r in roles_])})
        self.add_user_roles(user_id,roles)

    def delete_user(self,user_id,status):

        """
        :todo 删除用户
        :param user_id 删除用户id
        :param status 是否删除 0正常 1删除
        """
        user = self.db.query(Users).filter(Users.id==user_id).first()
        user.deleted = status
        self.db.commit()


    def user_format(self,user):
        keys = ['id','nick', 'qq','regist_from','sex', 'sign_text','status','uid','user_name','visit_times', 'weibo', 'weixin','is_bussiness']
        cookies={key:getattr(user,key) for key in keys}
        return cookies

    def change_pwd(self, id, old, new):
        user = self.db.query(Users.id, Users.user_pwd, Users.uid).filter(Users.deleted == 0, Users.id == id).first()
        if user[1] != self.user_passed(old):
            return '密码不正确'
        self.update_user(user[0], user_pwd=self.user_passed(new))
        return True


    def check_user_login_pwd(self, name, passwd):
        users = self.rdb.query(Users).filter(Users.deleted == 0).filter(Users.deleted == 0, or_(Users.user_name == name, Users.phone == name))
        for user in users:
            if user.user_pwd == self.user_passed(passwd):
                return True, user
        return False, '账号或密码错误'
        # user = self.db.query(Users).filter(Users.deleted == 0).filter(Users.user_name == name, Users.deleted == 0).first()
        # if user:
        #     if user.user_pwd == self.user_passed(passwd,user.uid):
        #         return user
        # user = self.db.query(Users).filter(Users.deleted == 0).filter(Users.phone == name, Users.deleted == 0).first()
        # if user:
        #     if user.user_pwd == self.user_passed(passwd,user.uid):
        #         return user
        # return False

    def check_username_exist(self, user_name):
        return self.rdb.query(Users.id).filter(Users.user_name == user_name, Users.deleted == 0).scalar()

    def get_username_by_id(self, id):
        return self.rdb.query(Users.user_name).filter(Users.id == id, Users.deleted == 0).scalar()

    def get_user_cache_msg_by_id(self, id):
        '''
        获取用户存入缓存信息
        '''
        return self.rdb.query(Users.id,Users.nick,Users.photo,Users.user_name,Users.role_codes).filter(Users.id == id, Users.deleted == 0).first()

    def get_drpusers_by_id(self,id):
        '''
        获取会员数
        :param id:
        :return:
        '''
        return self.rdb.query(Users.id).filter(Users.deleted == 0, Users.belong_id==id).count()

    def check_user_exist_by_id(self, id):
        return True  if self.rdb.query(Users.id).filter(Users.id == id, Users.deleted == 0).scalar() else False

    def get_users_index_info(self, id):
        return self.rdb.query(Users.id, Users.nick, Users.photo, Users.bg_ground, Users.coin, Users.vip_info, Users.sign_text).\
            filter(Users.id==id, Users.deleted==0).scalar()

    def check_user_login_pwd_by_id(self, id, passwd):
        '''根据id判断用户密码 用于修改 账号密码'''
        users = self.db.query(Users).filter(Users.deleted == 0).filter(Users.deleted == 0, Users.id == id)
        for user in users:
            if user.user_pwd == self.user_passed(passwd):
                return True
        return False

    def get_user_role_in_user_table(self,role_code):
        query=self.rdb.query(Users).filter(Users.deleted==0,Users.role_codes.like('%%%s%%'%role_code))
        return query

    def get_role_info_by_code(self,role_code):
        # print 'role_code',role_code
        query=self.rdb.query(Roles).filter(Roles.code.like('%%%s%%'%role_code))
        return query

    def get_all_roles(self):
        # print 'role_code',role_code
        query = self.db.query(Roles)
        return query

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
        user = self.db.query(Users).filter(Users.deleted==0,Users.id==user_id).scalar()
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
            user = Users()
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
        return self.rdb.query(Users).filter(Users.deleted==0,Users.weibo==weibo_id).scalar()

    def create_user_by_qq(self,user=None,**kargs):
        if not user:
            user = Users()
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
        return self.rdb.query(Users).filter(Users.deleted==0,Users.qq==qq).first()

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
        return self.rdb.query(Users).filter(Users.deleted==0,Users.weixin==open_id).first()

    def create_user_by_weixin(self,user=None,**kargs):
        if not user:
            user = Users()
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



    def set_users_weixin_null_by_weixin_id(self,weixin_id,user_id):
        '''
        :todo 根据微信ID设置为空
        :param weixin_id:
        :return:
        '''
        self.db.query(Users).filter(Users.deleted==0,Users.weixin==weixin_id,Users.id!=int(user_id)).update({'weixin':''})
        self.db.commit()

    #---------------topic ---------------------

    def login_with_phone(self,phone,passwd):
        '''
        :todo 用户账号登陆
        :param phone:
        :param passwd:
        :return:
        '''
        user = self.rdb.query(Users).filter(Users.deleted==0,Users.phone==phone,Users.user_pwd==self.user_passed(passwd)).scalar()
        return user

    def login_with_drp_username(self,user_name,passwd):
        '''
        todo:分销商登录前台
        :param user_name:
        :param passwd:
        :return:
        '''
        drp_user = self.rdb.query(DistributorUser).\
            filter(DistributorUser.deleted == 0,DistributorUser.phone == user_name,DistributorUser.user_pwd == self.user_passed(passwd)).scalar()
        return drp_user

    def login_with_username(self,user_name,passwd):
        '''
        :todo 用户名登陆
        :param user_name:
        :param passwd:
        :return:
        '''
        user = self.rdb.query(Users).filter(Users.deleted==0,Users.user_name==user_name,Users.user_pwd==self.user_passed(passwd)).scalar()
        return user

    def create_user_by_phone(self,phone,passwd):

        user = self.db.query(Users).filter(Users.deleted==0,Users.phone==phone).scalar()
        if user:
            user.nick = phone[:3]+'****'+phone[7:]
            user.user_pwd = self.user_passed(passwd)
            user.last_visit = now()
            self.db.add(user)
            self.db.commit()
            return user



    def add_recieve_address(self,user_id,**kwargs):
        location_service = LocationServices(rdb=self.db)
        addresses = self.db.query(UserAddress).filter(UserAddress.deleted==0,UserAddress.user_id==user_id)
        address_id = kwargs.get('address_id',None)
        if address_id:
            user_address = addresses.filter(UserAddress.id==address_id).scalar()
            if not user_address:
                user_address = UserAddress()
        else:user_address = UserAddress()
        user_address.user_id = user_id
        user_address.name = kwargs.get('name')
        user_address.card_type = 1
        user_address.card_num = kwargs.get('card_num')
        user_address.phone = kwargs.get('phone')

        province = location_service.get_by_id('province',kwargs.get('province'))
        city = location_service.get_by_id('city',kwargs.get('city'))
        area = location_service.get_by_id('area',kwargs.get('area'))

        user_address.province = province.name
        user_address.province_code = province.yh_code
        user_address.city = city.name
        user_address.city_code = city.yh_code
        user_address.area = area.name
        user_address.area_code = area.yh_code
        user_address.zipcode = city.zip_code
        user_address.address = kwargs.get('address')
        user_address.card_img1 = kwargs.get('font_card','')
        user_address.card_img2 = kwargs.get('back_card','')

        if addresses.count()<=0:
            user_address.is_default=True
        else:
            user_address.is_default=False

        self.db.add(user_address)
        self.db.commit()
        return user_address

    def get_address(self,user_id,**kwargs):
        '''
        获取用户地址
        :param user_id:
        :param is_default:
        :return:
        '''
        query = self.rdb.query(UserAddress).filter(UserAddress.deleted==0,UserAddress.user_id==user_id)
        if kwargs.has_key('is_default'):
            query = query.filter(UserAddress.is_default==kwargs.get('is_default'))
        query = query.order_by(desc(UserAddress.is_default))
        return query

    def get_one_address(self,user_id):
        '''
        获取用户地址
        :param user_id:
        :param is_default:
        :return:
        '''
        query = self.rdb.query(UserAddress).filter(UserAddress.deleted==0,UserAddress.user_id==user_id)
        query = query.order_by(desc(UserAddress.id)).first()
        return query

    def get_default_address(self,user_id):
        '''
        获取用户默认地址
        :param user_id:
        :return:
        '''
        return self.rdb.query(UserAddress).filter(UserAddress.deleted==0,UserAddress.user_id==user_id,UserAddress.is_default==1).scalar()


    def get_address_by_id(self,user_id,address_id):
        '''
        根据id查询用户地址
        :param user_id:
        :param address_id:
        :return:
        '''
        return self.rdb.query(UserAddress).filter(UserAddress.deleted==0,UserAddress.user_id==user_id,UserAddress.id==address_id).scalar()

    def set_default_address(self,address_id,user_id):
        '''
        设置默认收货地址
        :param address_id:
        :param user_id:
        :return:
        '''
        self.db.query(UserAddress).filter(UserAddress.deleted==0,UserAddress.user_id==user_id,UserAddress.is_default==True).update({'is_default':False},synchronize_session=False)
        self.db.query(UserAddress).filter(UserAddress.deleted==0,UserAddress.user_id==user_id,UserAddress.id==address_id).update({'is_default':True},synchronize_session=False)
        self.db.commit()

    def delete_address(self,address_id,user_id):
        '''
        删除地址
        :param address_id:
        :param user_id:
        :return:
        '''
        self.db.query(UserAddress).filter(UserAddress.deleted==0,UserAddress.user_id==user_id,
                                          UserAddress.id==address_id).update({'deleted':1},synchronize_session=False)
        self.db.commit()

    def batch_user(self,data):
        '''
        todo:批量添加大客户
        :param data:
        :return:
        '''
        user_ids = []
        for key in data:
            query = self.db.query(Users).filter(Users.deleted == 0,Users.id == key)
            query.update({'is_bussiness':1})
            user_ids.append(key)
        self.db.commit()
        return True,user_ids

    def get_users_total_count(self):
        '''
        统计会员总数
        :return:
        '''
        return self.rdb.query(Users.id).filter(Users.deleted==0).count()

    def get_member_order_count(self):
        mysql = '''
select count(distinct o.user_id) as total from users  as u inner join orders as o
where o.deleted=0 and u.deleted=0 and u.id = o.user_id and o.status=1 and o.pay_status=1;'''
        query = self.rdb.execute(mysql)
        # print query.scalar()
        return query

    def check_user_by_phone(self,phone):
        '''
        todo:
        :param phone:
        :return:
        '''
        user = self.rdb.query(Users).filter(Users.deleted == 0,Users.phone == phone).scalar()
        return user

    def get_vendors(self):
        '''
        获取所有供应商
        :return:
        '''
        return self.rdb.query(DistributorUser).filter(DistributorUser.deleted == 0, DistributorUser.role_type==1,DistributorUser.status=='normal')
