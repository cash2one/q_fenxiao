#encoding:utf-8

#!/usr/bin/env python


from models.admin_do import *
from models.advertise import *
from models.express_do import *
from models.coupon_do import *
from models.gallery import *
from models.help_do import *
from models.item_do import *
from models.location_do import *
from models.message_do import *
from models.orders_do import *
from models.site_do import *
from models.member_do import *
from models.user_do import *
from models.workorder_do import *
from models.employee import *
from models.logs_do import ApiLogs
from models.cities.init_data import *
from models.config import Config
from sqlalchemy import create_engine, MetaData,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from models.base_do import Base
from sqlalchemy import inspect
from sqlalchemy.orm import column_property
from conf.express_company import express_company
from models.app_do import AppVersion
from models.user_do import *

# class AdminUser(Base):
#     __tablename__ = 'user'
#     id = Column(Integer, primary_key=True)
#     firstname = Column(String(50))
#     lastname = Column(String(50))
#     fullname = column_property(firstname + " " + lastname)

mysql_engine = create_engine('mysql://root@localhost:3306/fenxiao?charset=utf8',encoding = "utf-8",echo =True)

Session = sessionmaker(bind=mysql_engine)
session = Session()
# Base.metadata.create_all(mysql_engine)  #建表
# exit(0)

# Base.metadata.create_all(mysql_engine)  #建表
# exit(0)
def create_table():
    #Base.metadata.drop_all(mysql_engine)
    Base.metadata.create_all(mysql_engine)  #建表
    from services.users.distributor_user_services import DistributorUserServices
    admin_service = DistributorUserServices(session)
    admin_service.add_distributor_user(
        'admin',
        '1qazxsw23edc',
        '15397008337',
        'hello',
        0
        )
    session.commit()

def init_roles():
    data = [('admin','管理员','整个站点管理')]
    session.execute(
        Roles.__table__.insert(),[{'code':code,'name':name,'description':description} for code,name,description in data]
    )
    session.commit()

def init_users():

    from services.users.user_services import UserServices
    user_service = UserServices(session)
    user_service.set_db(session)
    user_service._add(user_name='qiuyan',user_pwd='1qazxsw2007',roles=[1])
    user_service._add(user_name='xiaobei',user_pwd='1qazxsw2007',roles=[1])
    session.commit()
#
#
#
# def init_admin():
# from services.users.admin_services import AdminServices
# admin_service = AdminServices(session)
# admin_service._add(
#     tel='18268802385',
#     real_name='丘岩',
#     user_name='qiuyan',
#     newpassword='111111',
#     sex='M',
#     roles=[1]
#     )
# session.commit()
#
# def init_categories():
#     categories = [{'id':1,'name':'母婴专区'},{'id':2,'name':'食品保健'},{'id':3,'name':'电子数码'},{'id':4,'name':'海外直邮'}]
#     for c in categories:
#         category = ItemCategory()
#         category.id = c.get('id')
#         category.name = c.get('name')
#         category.desc = c.get('name')
#         category.parent_id = 0
#         category.full_parent_id = '/0/'
#         category.level = 1
#         session.add(category)
#     session.commit()
#
# def init_work_types():
#     names = [['支付错误处理','支付成功,回调成功,回调修改订单状态错误'],
#         ['支付异常','']]
#     for name in names:
#         work_type = WorkOrderType()
#         work_type.name=name[0]
#         work_type.desc = name[1]
#         session.add(work_type)
#     session.commit()
#
# def init_ware_house():
#     s = WareHouse()
#     s.name = '南沙保税仓'
#     s.desc ='南沙保税仓'
#     s.site_real_name==True
#     session.add(s)
#     session.commit()
#
# def init_express_company():
#     for key in express_company:
#         express_comapny = ExpressCompany()
#         express_comapny.code = key
#         express_comapny.name = express_company.get(key)
#         session.add(express_comapny)
#     session.commit()





def init_site_data():
    create_table()
    #query = session.query(ItemDetail).filter(ItemDetail.deleted==0).order_by('')

    # query = session.query(ItemDetail).filter(ItemDetail.deleted==0,ItemDetail.top_category_id==1,ItemDetail.is_online==True)
    # query = query.having((ItemDetail.sale_quantity-ItemDetail.warning_quantity)>1)
    # print query
    #,ItemDetail.top_category_id==category_id,ItemDetail.is_online==True)

    # print dir(session)
    # sql='update item_detail set sale_quantity=(sale_quantity-1) where id=1;update item_detail set sale_quantity=(sale_quantity-1) where id=2;update item_detail set sale_quantity=(sale_quantity-1) where id=3;'
    # session.execute(sql)
    # session.commit()
    # exit(0)
    #create_table()
    #exit(0)
    # print '创建表成功'
    # init_roles()
    # print '创建角色成'
    # init_admin()
    # print '初始化管理员成功'
    # init_categories()
    # print '类目初始化成功'
    # init_users()
    # print
    # init_work_types()
    # print '工单类型初始化成功'
    # init_ware_house()
    # print '初始化保税仓成功'
    # init_express_company()
    # print '初始化快递公司信息'
    # from lxml import etree
    # import os
    # ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
    # file_path = ROOT_PATH + "/" + "cities"+"/"
    # parse(session,etree,file_path)
    # print '初始化地理信息'
    print '完成初始化'
    exit(0)

# invoice_orders = session.query(InvoiceOrders).filter(InvoiceOrders.deleted==0,InvoiceOrders.status.in_([0,1]))
# print invoice_orders

# ['_Session__binds', '__class__', '__contains__', '__delattr__',
#  '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__',
#  '__init__', '__iter__', '__module__', '__new__', '__reduce__', '__reduce_ex__',
#  '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__',
#  '_attach', '_autoflush', '_before_attach', '_conditional_expire', '_connection_for_bind',
#  '_contains_state', '_delete_impl', '_deleted', '_dirty_states', '_enable_transaction_accounting',
#  '_expire_state', '_expunge_state', '_flush', '_flush_warning', '_flushing', '_identity_cls',
#  '_is_clean', '_merge', '_new', '_query_cls', '_register_altered', '_register_newly_persistent',
#  '_remove_newly_deleted', '_save_impl', '_save_or_update_impl', '_save_or_update_state',
#  '_update_impl', '_validate_persistent', '_warn_on_events', 'add', 'add_all',
#
#  'autocommit', 'autoflush', 'begin', 'begin_nested', 'bind', 'bind_mapper',
#  'bind_table', 'close', 'close_all', 'commit', 'connection', 'connection_callable',
#  'delete', 'deleted', 'dirty', 'dispatch', 'enable_relationship_loading', 'execute', 'expire',
#  'expire_all', 'expire_on_commit', 'expunge', 'expunge_all', 'flush', 'get_bind', 'hash_key',
#  'identity_key', 'identity_map', 'info', 'is_active', 'is_modified', 'merge', 'new', 'no_autoflush',
#  'object_session', 'prepare', 'prune', 'public_methods', 'query', 'refresh', 'rollback', 'scalar', 'transaction', 'twophase']
#
# query = session.query(ItemOrders.id,ItemOrders.item_id,ItemOrders.item_price,ItemOrders.total_amount,ItemOrders.buy_nums,ItemOrders.order_id,
#                        Orders.order_no,Orders.status,Orders.pay_status,Orders.delivery_status,Orders.recevie_address,Orders.gmt_created,
#                        ItemDetail.brand,ItemDetail.item_no,ItemDetail.name,ItemDetail.tax_rate,PayOrders.payment_id,PayOrders.other_payment_id,PayOrders.payment_time)\
#                        .join(Orders,ItemOrders.order_id == Orders.id).join(ItemDetail,ItemOrders.item_id == ItemDetail.id)\
#                        .join(PayOrders,PayOrders.order_id==Orders.id).filter(ItemOrders.deleted==0,ItemDetail.deleted==0,Orders.deleted==0,PayOrders.deleted==0)
#
#
# print query

if __name__ == '__main__':
    init_site_data()