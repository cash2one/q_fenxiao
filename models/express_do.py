#encoding:utf-8
__author__ = 'binpo'

from models.base_do import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, SmallInteger,Text,Numeric,Float
from sqlalchemy import event
from sqlalchemy.sql.functions import now


class ExpressCompany(Base):
    #https://code.google.com/p/kuaidi-api/wiki/Open_API_API_URL
    '''物流公司'''
    __tablename__='express_company'

    name = Column(String(128),doc='物流公司名称',default='')
    code = Column(String(32),doc='物流公司代码',default='')
    contact = Column(String(128),doc='联系人',default='')
    phone = Column(String(30),doc='电话',default='')
    remark = Column(String(1024),doc='简要说明',default='')
    api_url = Column(String(256),doc='物流信息',default='')

class OrderExpress(Base):
    '''订单物流'''
    __tablename__ = 'order_express'

    order_id = Column(Integer,doc='订单ID')
    order_no = Column(String(64),doc='订单号')
    express_comoany_id = Column(Integer,doc='物流ID')
    express_no = Column(String(64),doc='物流单号')
    # status = Column(SmallInteger,doc='状态',default=1)#状态  1:已发货  2:已签收
    # sign_time = Column(DateTime,doc='牵手时间')


class InvoiceOrders(Base):
    '''发货单'''
    __tablename__ = 'invoice_orders'

    invoice_no = Column(String(64),doc='发货单号',default='')
    user_id = Column(Integer,doc='用户DI',nullable=True)
    name = Column(String(64),doc='名称',default='')
    order_id = Column(Integer,doc='订单号')
    supply_id = Column(Integer,doc='供应商ID',nullable=True,default=0)
    drp_user_id = Column(Integer,doc='供应商ID',nullable=True,default=0)
    order_no = Column(String(64),doc='订单编号')
    province = Column(String(64),doc='省份')
    city = Column(String(64),doc='城市')
    county = Column(String(64),doc='国家')
    zip = Column(String(32),doc='邮编')
    addr = Column(String(128),doc='地址')
    mobile = Column(String(16),doc='电话')
    express_no = Column(String(32),doc='物流单号',default='')
    express_company_id = Column(Integer,doc='物流公司',default=0)
    status = Column(SmallInteger,doc='状态',default=0)#状态 0:未发货 1:已发货  2:已签收
    delivery_time = Column(DateTime,doc='发货时间',nullable=True,default=None)  #后台提交物流订单时间 status=1
    complete_time = Column(DateTime,doc='签收时间',nullable=True,default=None)  #签收时间
    express_content = Column(Text,doc='物流流转信息',default='')
    remark = Column(String(1024),doc='备注')

class ReturnOrders(Base):
    '''退货单'''

    __tablename__ = 'return_orders'

    user_id = Column(Integer,doc='用户ID')
    admin_id = Column(Integer,doc='处理人ID')
    order_id = Column(Integer,doc='订单id')
    order_no  = Column(Integer,doc='订单序列号')
    reason = Column(String(1024),doc='退货原因')
    province = Column(Integer,doc='省份')
    city = Column(Integer,doc='城市')
    area = Column(Integer,doc='区域')
    zip = Column(String(32),doc='邮编')
    addr = Column(String(256),doc='地址')
    name = Column(String(64),doc='名称')
    mobile = Column(String(16),doc='电话')
    express_no = Column(String(32),doc='物流单号')
    express_company_id = Column(Integer,doc='物流公司ID')
    handling_idea = Column(String(1025),doc='处理意见')
    status = Column(SmallInteger,doc='状态')#状态: 0 申请退货 1 同意退货 2 拒绝退货 3 货品寄回中 4 退货完成


@event.listens_for(InvoiceOrders, 'before_update')
def receive_before_update(mapper, connection, target):
    target.gmt_modified = now()

@event.listens_for(ReturnOrders, 'before_update')
def receive_before_update(mapper, connection, target):
    target.gmt_modified = now()

@event.listens_for(OrderExpress, 'before_update')
def receive_before_update(mapper, connection, target):
    target.gmt_modified = now()

from sqlalchemy.orm.session import Session
from .orders_do import Orders

@event.listens_for(InvoiceOrders, 'after_update')
def after_update_listener(mapper, connection, target):
    # print 'OK'
    session = Session(bind=connection)
    order = session.query(Orders).filter(Orders.deleted==0,Orders.id==target.order_id).scalar()#(Orders.delivery_status)
    if order:
        if target.status==1:
            order.deliver_time = now()
            order.delivery_status=1
        # elif target.status==2:
        #     order.receive_time=now()
        #     order.delivery_status=2
        #     order.complete_time=now()
        #     order.status=2
        session.add(order)
    session.commit()


# @event.listens_for(InvoiceOrders.status, 'set')
# def receive_set(target, value, oldvalue, initiator):
#
#     '''
#     根据发货单自动更新状态
#     :param mapper:
#     :param connection:
#     :param target:
#     :return:
#     '''
#     print type(target)
#     print value
#     print oldvalue
#     print dir(initiator)


# @event.listens_for(ReturnOrders.status, 'after_update')
# def after_update_listener(mapper, connection, target):
#     '''
#     自动更新状态
#     :param mapper:
#     :param connection:
#     :param target:
#     :return:
#     '''
#     session = Session(bind=connection)
#     order = session.query(Orders).filter(Orders.deleted==0,Orders.id==target.order_id).scalar()#(Orders.delivery_status)
#     if order:
#         if target.status==1:
#             order.delivery_status=1
#         elif target.status==2:
#             order.delivery_status=2
#             order.status=2
#         session.add(order)
#     session.commit()