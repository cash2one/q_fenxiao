#encoding:utf-8
__author__ = 'binpo'

from models.base_do import Base,ChoiceType
from sqlalchemy import Column, Integer, String, DateTime, Boolean, SmallInteger,Text,Float,Float
from conf.orders_conf import ORDER_STAYUS,PAY_STATUS,DELIVERRY_STATUS,PAY_TYPE,REFUND_STATUS,ORDER_STATUS_REMARK
from sqlalchemy import event
from sqlalchemy.sql.functions import now

class Orders(Base):
    __tablename__ = 'orders'

    order_no = Column(String(64))
    user_id = Column(Integer,doc='用户ID')
    drp_usere_id = Column(Integer,doc='分销商ID')
    supply_user_id = Column(Integer,doc='供应商ID')
    #相关状态
    status = Column(SmallInteger,doc='订单状态',default=1) #ChoiceType(ORDER_STAYUS)订单状态 1:生成订单 2:完成订单 3:取消订单 4:作废订单
    pay_status = Column(SmallInteger,doc='支付状态',default=0)#ChoiceType(PAY_STATUS),doc='支付状态',default=0) # 支付状态 0:未付款 1: 已付款 2:申请退款 3: 已退款,
    delivery_status = Column(SmallInteger)#ChoiceType(DELIVERRY_STATUS),doc='配送状态',default=None) #配送状态 0:未发货 1: 已发货 2:已签收 3:申请退货 4:已退货

    #相关费用
    payable_amount = Column(Float,doc='商品金额',default=0)
    real_amount = Column(Float,doc='实付金额',default=0)
    discount_amount = Column(Float,doc='优惠金额',default=0)
    transport_anmount = Column(Float,doc='运费',default=0)
    # tax_amount = Column(Float,doc='税费',default=0)
    voucher = Column(Integer,doc='优惠卷ID',default=0)
    brokerage = Column(Float,doc='佣金金额')
    #支付相关
    pay_time = Column(DateTime,doc='支付时间',nullable=True,default=None)
    pay_type = Column(SmallInteger,doc='支付方式',default=0)#ChoiceType(PAY_TYPE)
    deliver_time = Column(DateTime,doc='发货时间',nullable=True,default=None)
    receive_time = Column(DateTime,doc='收货时间',nullable=True,default=None)
    completion_time = Column(DateTime,doc='完成时间',nullable=True,default=None)

    user_remark = Column(String(512),doc='用户备注',default='')
    admin_remark = Column(String(512),doc='客服备注',default='')

    order_type = Column(SmallInteger,doc='订单类型',default=0)#普通订单,限时优惠,团购 #activity_id
    # house_ware_id = Column(Integer,doc='保税仓id',nullable=True,default=1)
    # house_ware_name = Column(String(128),doc='发货仓',default='')
    recevie_address = Column(String(512),doc='收货地址',default='') # json {省市区，姓名，电话，证件号，证件类型 邮编}
    recevie_address_id = Column(Integer,doc='收货地址',nullable=True,default=None)
    # is_abroad = Column(Boolean,doc='是否跨境订单') #1:是   0:否
    # is_asyn = Column(Boolean,doc='是否已经同步',default=False)      #数据同步到海关
    is_assess = Column(Boolean,doc='是否已经评价',default=False)      #是否已评价
    is_addition_assess = Column(Boolean,doc='是否追加评价',default=False)  #是否追加评论
    cancle_remark = Column(String(128),default='',doc='取消原因')
    order_from = Column(String(32),default='PC_WEB',doc='订单来源')


class ItemOrders(Base):
    '''商品订单'''
    __tablename__ = 'item_orders'

    order_id = Column(Integer,doc='订单ID')
    order_no = Column(String(64),doc='订单序号')
    drp_usere_id = Column(Integer,doc='分销商ID')
    supply_user_id = Column(Integer,doc='供应商ID')
    item_id = Column(Integer,doc='商品ID')
    is_drp_item = Column(Boolean,doc='是否分销商的商品 1:是 0:否',default=0)
    drp_user_id = Column(Integer,doc='分销商ID')
    sku_id = Column(Integer,doc='商品SKUID')
    item_price = Column(Integer,doc='商品单价')
    buy_nums = Column(SmallInteger,doc='购买数量')
    total_amount = Column(Float,doc='总金额',default=0)
    description = Column(String(512),doc='描述')
    is_apply_refund = Column(Boolean,default=False,doc='是否申请了退单')

class PaylogsEhking(Base):
    '''
    易汇金支付存储跳转记录
    '''
    __tablename__ = 'pay_logs_ehking'
    order_id = Column(Integer,doc='订单ID')
    order_no = Column(String(64),doc='订单序号')
    user_id = Column(Integer,doc='用户ID')
    requestId = Column(String(64),doc='订单序号')
    merchantId = Column(String(64),doc='商户id')
    status = Column(String(20),doc='返回状态')
    redirectUrl = Column(String(250),doc='跳转地址')

class PayOrders(Base):

    '''支付单'''

    __tablename__='pay_orders'

    order_id = Column(Integer)
    drp_usere_id = Column(Integer,doc='分销商ID')
    supply_user_id = Column(Integer,doc='供应商ID')

    order_no = Column(String(64),doc='订单序号')
    payment_id = Column(String(64),doc='支付ID,唯一序号')
    other_payment_id = Column(String(64),doc='第三方产生的支付单号',default='',nullable=True)
    user_id = Column(Integer,doc='用户ID')
    pay_status = Column(SmallInteger,doc='支付状态',default=0)#ChoiceType(PAYMENT_STATUS),doc='支付状态',default=0)#SmallInteger,doc='支付状态',default=0) # 支付状态 0:等待支付 1: 支付成功 2.取消支付
    pay_type = Column(SmallInteger,doc='支付方式',default=0)#ChoiceType(PAY_TYPE)
    pay_account = Column(String(64),doc='支付账号',default='')
    amount  = Column(Float,doc='金额')
    brokerage = Column(Float,doc='佣金金额')
    payment_time = Column(DateTime,nullable=True,doc='支付时间',default=None)
    exchange = Column(String(32),doc='汇率',default='')
    recevie_address = Column(String(512),doc='收货地址')
    settlement = Column(Boolean,default=0,doc='是否已结算 0未结算 1结算')
    settlement_no = Column(String(128),doc='结算编号',default='')

class Settlement(Base):

    '''结算中心'''
    __tablename__='settlement'

    drp_usere_id = Column(Integer,doc='分销商ID')
    settlement_no = Column(String(128),doc='结账ID')
    settlement_amount = Column(Float,doc='结算金额')
    payment_no = Column(String(128),doc='银行流水号')
    admin_id = Column(Integer,doc='管理员账户',default=0)
    content = Column(String(2048),doc='结算描述',default='')


class RefundOrders(Base):
    '''退款单'''

    __tablename__ = 'refund_orders'

    order_id = Column(Integer,doc='退款订单')
    drp_usere_id = Column(Integer,doc='分销商ID')
    supply_user_id = Column(Integer,doc='供应商ID')
    order_no = Column(String(64),doc='订单序号')
    refund_no = Column(String(64),doc='退单序号',default='')
    payment_id = Column(String(64),doc='支付ID,唯一序号')
    other_payment_id = Column(String(64),doc='第三方产生的支付单号')
    item_id = Column(Integer,doc='商品ID',nullable=True)
    user_id = Column(Integer,doc='用户ID')
    payment_time = Column(DateTime,nullable=True,doc='支付时间')
    order_create_time = Column(DateTime,nullable=True,doc='订单创建时间(冗余)')
    pay_status = Column(SmallInteger,doc='支付状态',default=0) #
                                                #     REFUND_STATUS={
                                                #     0:'申请退款',
                                                #     1:'不予退款',
                                                #     2:'已受理退款',
                                                #     3:'退款成功'
                                                # }
    pay_type = Column(SmallInteger,doc='退款方式',default=0)

    pay_account = Column(String(64),doc='退款账号',default='')
    admin_id = Column(Integer,doc='管理员账户',default=0)
    content = Column(String(512),doc='退款原因',default='')
    handling_idea = Column(String(512),doc='处理意见',default='')
    handling_time = Column(DateTime,doc='处理时间',default='')

    apply_amount = Column(Float,doc='申请退款金额',default=0)
    refound_amount = Column(Float,doc='实际退款金额',default=0)
    refund_proof = Column(String(1024),default='',doc='退款凭证(图片)')
    express_no = Column(String(32),doc='物流单号',default='')
    express_company_id = Column(Integer,doc='物流公司ID',nullable=True)

class OrderStatus(Base):

    '''订单状态'''
    __tablename__='order_status'

    operation_id = Column(Integer,doc='操作人ID')
    order_id = Column(Integer,doc='订单ID')
    status = Column(String(10),doc='上一状态')
    pay_status = Column(String(10),doc='支付状态')
    deliver_status = Column(String(10),doc='发货状态')
    remark = Column(String(2048),doc='订单状态描述')

class PayStatus(Base):

    '''支付状态变化跟踪'''
    __tablename__='pay_status'
    pay_order_id = Column(Integer,doc='订单壮体')
    current_state = Column(String(10),doc='当前状态')

from sqlalchemy.orm.session import Session
@event.listens_for(PayOrders, 'after_update')
def after_update_listener(mapper, conn, target):
    '''
    :所有支付完成以后更新订单状态
    :param mapper:
    :param conn:
    :param target:
    :return:
    '''
    #trans = conn.begin()
    #try:
    session = Session(bind=conn)
    pay_status = PayStatus()
    pay_status.pay_order_id = target.id
    pay_status.current_state = target.pay_status
    session.add(pay_status)
    session.commit()

@event.listens_for(PayOrders, 'after_insert')
def after_insert_listener(mapper, conn, target):
    '''
    :所有支付完成以后更新订单状态
    :param mapper:
    :param conn:
    :param target:
    :return:
    '''
    #trans = conn.begin()
    #try:
    session = Session(bind=conn)
    pay_status = PayStatus()
    pay_status.pay_order_id = target.id
    pay_status.current_state = target.pay_status
    session.add(pay_status)
    session.commit()

@event.listens_for(Orders, 'after_update')
def after_update_listener(mapper, conn, target):
    '''
    :所有支付完成以后更新订单状态
    :param mapper:
    :param conn:
    :param target:
    :return:
    '''
    #trans = conn.begin()
    #try:
    session = Session(bind=conn)
    try:
        order_status = session.query(OrderStatus).filter(OrderStatus.order_id == target.id,
        OrderStatus.status ==target.status,
        OrderStatus.pay_status == target.pay_status,
        OrderStatus.deliver_status == target.delivery_status
        ).scalar()
    except:
        pass
    if not order_status:
        order_status = OrderStatus()
        order_status.order_id = target.id
        order_status.status =target.status
        order_status.pay_status = target.pay_status
        order_status.deliver_status = target.delivery_status
        order_remark = str(target.status)+str(target.pay_status)+str(target.delivery_status)
        #if order_remark==110:
        order_status.remark = ORDER_STATUS_REMARK.get(order_remark,'')#'订单提交成功'
        session.add(order_status)
        session.commit()

@event.listens_for(Orders, 'after_insert')
def after_insert_listener(mapper, conn, target):
    '''
    :所有支付完成以后更新订单状态
    :param mapper:
    :param conn:
    :param target:
    :return:
    '''
    #trans = conn.begin()
    #try:
    session = Session(bind=conn)
    order_status = OrderStatus()
    order_status.order_id = target.id
    order_status.status =target.status
    order_status.pay_status = target.pay_status
    order_status.deliver_status = target.delivery_status
    order_status.remark = '订单提交成功'
    session.add(order_status)
    session.commit()

@event.listens_for(PayStatus, 'before_update')
def receive_before_update(mapper, connection, target):
    target.gmt_modified = now()

@event.listens_for(Orders, 'before_update')
def receive_before_update(mapper, connection, target):
    target.gmt_modified = now()


@event.listens_for(PayOrders, 'before_update')
def receive_before_update(mapper, connection, target):
    target.gmt_modified = now()

