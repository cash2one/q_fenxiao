#encoding:utf-8
__author__ = 'binpo'
from services.base_services import BaseService
from models.orders_do import Orders,ItemOrders,PayOrders,PaylogsEhking,Settlement
from models.express_do import InvoiceOrders
from models.item_do import ItemDetail,ItemCategory
from models.user_do import Users
from sqlalchemy import or_
from sqlalchemy.sql.functions import now
from sqlalchemy.orm import aliased
import datetime
import time
from utils.exchange_rate import get_usd_exchange_rate_and_count
from sqlalchemy import func, or_, not_


class OrderServices(BaseService):

    def get_drp_total_comm_by_id(self,id,settlement):
        '''
        获取分销商佣金总金额
        :param id: 分销商用户id
        :return:
        '''
        if settlement==None:
             mysql = '''
               select sum(a.brokerage)  as total from pay_orders a, orders b where a.order_id = b.id and a.pay_status=1
               and b.delivery_status =2 and a.deleted = 0 and b.deleted = 0 and b.status =1 ;'''
             query = self.rdb.execute(mysql)
             return query.scalar()
            # return self.rdb.query(func.sum(PayOrders.brokerage)).filter(PayOrders.deleted==0,PayOrders.drp_usere_id==id,PayOrders.pay_status==1).scalar()
        else:
            if int(settlement)==1:
                mysql = '''
               select sum(a.brokerage)  as total from pay_orders a, orders b where a.order_id = b.id and a.pay_status=1
and a.settlement = 1 and b.delivery_status =2 and a.deleted = 0 and b.deleted = 0 and b.status =1 ;'''
            else:
                mysql = '''
               select sum(a.brokerage)  as total from pay_orders a, orders b where a.order_id = b.id and a.pay_status=1
and a.settlement = 0 and b.delivery_status =2 and a.deleted = 0 and b.deleted = 0 and b.status =1;'''
            query = self.rdb.execute(mysql)
            return query.scalar()
            # return self.rdb.query(func.sum(PayOrders.brokerage)).filter(PayOrders.deleted==0,PayOrders.drp_usere_id==id,PayOrders.pay_status==1,PayOrders.settlement==settlement).scalar()

    def get_drp_total_amount_by_id(self):
        '''
        根据分销商id获取分销商的销售总额
        :return:
        '''
        return self.rdb.query(func.sum(PayOrders.amount)).filter(PayOrders.deleted==0,PayOrders.drp_usere_id==id).scalar()

    def get_merchant_total_comm_by_id(self,id,settlement=''):
        '''
        供应商
        :param id:
        :param settlement:
        :return:
        '''
        if settlement=='':
            return self.rdb.query(func.sum(PayOrders.brokerage)).filter(PayOrders.deleted==0,PayOrders.drp_usere_id==id).scalar()
        else:
            return self.rdb.query(func.sum(PayOrders.brokerage)).filter(PayOrders.deleted==0,PayOrders.supply_user_id==id,PayOrders.settlement==settlement).scalar()


    def update_payorders_settlement(self,drp_usere_id,settlement_no):
        query = self.db.query(PayOrders).filter(PayOrders.deleted == 0,PayOrders.drp_usere_id == drp_usere_id,PayOrders.settlement==0,PayOrders.pay_status==1)
        query.update({'settlement_no':settlement_no,'settlement':1})
        self.db.commit()
        return True

    def list_settlement(self,drp_user_id, keyword):
        query = self.rdb.query(Settlement).filter(Settlement.deleted ==0)
        if drp_user_id:
            query = query.filter(Settlement.drp_usere_id==drp_user_id)
        if keyword:
            query = query.filter(or_(Settlement.payment_no.like("%"+keyword+"%"),Settlement.settlement_no.like("%"+keyword+"%")))
        query = query.order_by('Settlement.gmt_created desc')
        return query


    def get_item_old_price(self,order_id,item_id):
        return self.rdb.query(ItemOrders).filter(ItemOrders.deleted==0,ItemOrders.order_id==order_id,ItemOrders.item_id==item_id).scalar()

    def get_order_by_order_no(self,order_no):
        '''
        根据订单号获取订单相关信息
        :param order_no:
        :return:
        '''
        return self.rdb.query(Orders).filter(Orders.deleted==0,Orders.order_no==order_no).scalar()

    def get_order_id(self,order_id,user_id):
        '''
        根据ID获取订单
        :param order_id:
        :param user_id:
        :return:
        '''
        return self.rdb.query(Orders).filter(Orders.deleted==0,Orders.id==order_id,Orders.user_id==user_id).scalar()

    def get_order_no(self,order_no,user_id):
        '''
        todo:根据order_no获取order
        :param order_no:
        :return:
        '''
        return self.rdb.query(Orders).filter(Orders.deleted==0,Orders.order_no==order_no,Orders.user_id==user_id).scalar()


    def _list(self,user_id=None,drp_user_id=None,supply_user_id=None,state='',**kwargs):
        '''
        查下订单列表
        :param user_id: 用户ID
        :param kwargs: 其他集合参数
        :return:
        '''
        query = self.rdb.query(Orders.id,
                               Orders.order_no,
                               Orders.gmt_created,
                               Orders.user_id,
                               Orders.recevie_address_id,
                               Orders.real_amount,
                               Orders.payable_amount,
                               Orders.status,
                               Orders.order_from,
                               Orders.brokerage,
                               Orders.drp_usere_id,
                               Orders.supply_user_id,
                               Orders.pay_status,
                               Orders.delivery_status,
                               Orders.recevie_address,
                               Orders.is_assess,
                               Orders.is_addition_assess).join(PayOrders,Orders.id==PayOrders.order_id).filter(Orders.deleted==0)
        '''
        waiting_pay= query.filter(Orders.status==1,Orders.pay_status==0).count()
        waiting_deliver = query.filter(Orders.pay_status==1,Orders.delivery_status==0).count()
        waiting_recieve = query.filter(Orders.pay_status==1,Orders.delivery_status==1).count()
        waiting_assess = query.filter(Orders.delivery_status==2,Orders.is_assess==False).count()
        '''

        if state=='1':
            kwargs['status'] = 1
            kwargs['pay_status'] = 0
        elif state=='2':
            kwargs['pay_status'] = 1
            kwargs['delivery_status'] = 0
        elif state=='3':
            kwargs['pay_status'] = 1
            kwargs['delivery_status'] = 1
        elif state=='4':
            kwargs['delivery_status'] = 2
            kwargs['is_assess'] = False

        if user_id:
            query = query.filter(Orders.user_id==user_id,PayOrders.user_id==user_id)

        if drp_user_id:
            query = query.filter(Orders.drp_usere_id == drp_user_id)

        if supply_user_id:
            query = query.filter(Orders.supply_user_id == supply_user_id)

        if kwargs.has_key('status'):
            query = query.filter(Orders.status==kwargs.get('status'))

        if kwargs.has_key('pay_status'):
            query = query.filter(Orders.pay_status==kwargs.get('pay_status'))
        if kwargs.has_key('delivery_status'):
            query = query.filter(Orders.delivery_status==kwargs.get('delivery_status'))
        if kwargs.get('start_date'):
            query = query.filter(Orders.gmt_created >= kwargs.get('start_date')+' 00:00:00')
        if kwargs.get('end_date'):
            query = query.filter(Orders.gmt_created <= kwargs.get('end_date')+' 23:59:59')
        if kwargs.get('pay_start_date'):
            query = query.filter(Orders.id.in_(self.rdb.query(PayOrders.order_id).filter(PayOrders.payment_time>=kwargs.get('pay_start_date')+' 00:00:00')))
        if kwargs.get('pay_end_date'):
            query = query.filter(Orders.id.in_(self.rdb.query(PayOrders.order_id).filter(PayOrders.payment_time<=kwargs.get('pay_end_date')+' 23:59:59')))
        if kwargs.get('content'):
            content = kwargs.get('content')
            query = query.filter(or_(Orders.order_no.like("%"+content+"%"),Orders.recevie_address.like("%"+content+"%"),Orders.user_id==(self.rdb.query(Users.id).filter(Users.deleted==0,Users.phone==content))))
        if kwargs.get('asyn_status'):
            asyn_status = kwargs.get('asyn_status')
            query = query.filter(Orders.is_asyn==kwargs.get('asyn_status'))
            if asyn_status == '0':
                query = query.filter(Orders.status==0,Orders.pay_status == 1,Orders.delivery_status==0)
        if kwargs.has_key('order_by'):
            query = query.order_by('Orders.'+kwargs.get('order_by')+' desc')
        else:
            query = query.order_by('Orders.gmt_created desc')
        return query

    def query_orders(self,user_id):
        '''
        查询订单
        :param user_id:
        :return:
        '''
        query = self.rdb.query(Orders.id).filter(Orders.deleted==0)
        if user_id:
            query = query.filter(Orders.user_id==user_id)
        return query

    def query_item_by_order_id(self,order_id):
        '''
        根据订单ID下查询所有购买的商品信息
        :param order_id:订单id
        :return:
        '''
        query = self.rdb.query(ItemDetail.id,ItemDetail.show_id,ItemDetail.main_pic,ItemDetail.price,ItemDetail.orgin_price,ItemOrders.order_no,
                               ItemDetail.inner_price,ItemDetail.title,ItemOrders.buy_nums,ItemDetail.top_category_id,ItemDetail.product_keywords,ItemDetail.drp_min_price,
                               ItemOrders.item_price,ItemDetail.vendor_id,ItemOrders.total_amount,ItemDetail.item_no,ItemDetail.name,ItemDetail.brand,ItemDetail.amount,ItemOrders.is_apply_refund,ItemOrders.is_drp_item).\
                               join(ItemOrders,ItemDetail.id==ItemOrders.item_id).filter(ItemOrders.order_id==order_id)
        return query

    def query_buy_items_by_order_id(self,order_id):
        '''
        根据订单ID下查询所有购买的商品信息
        :param order_id:订单id
        :return:
        '''
        query = self.rdb.query(ItemOrders.id,ItemOrders.item_price,ItemOrders.total_amount,ItemOrders.buy_nums,ItemDetail.main_pic,ItemDetail.item_no,ItemDetail.name,ItemDetail.brand,ItemDetail.amount,ItemOrders.is_apply_refund).\
                               join(ItemDetail,ItemDetail.id==ItemOrders.item_id).filter(ItemOrders.order_id==order_id)
        return query


    # def query_item_by_order_no(self,order_no):
    #     '''
    #     根据订单号下查询所有购买的商品信息
    #     :param order_no:订单号
    #     :return:
    #     '''
    #     query = self.rdb.query(ItemDetail.id,ItemDetail.main_pic,ItemDetail.price,ItemDetail.orgin_price,ItemOrders.order_no,
    #                            ItemDetail.inner_price,ItemDetail.title,ItemOrders.buy_nums,ItemDetail.top_category_id,
    #                            ItemOrders.item_price,ItemOrders.total_amount,ItemDetail.item_no,ItemDetail.name,ItemDetail.brand,ItemDetail.amount,ItemOrders.is_apply_refund).\
    #                            join(ItemOrders,ItemDetail.id==ItemOrders.item_id).filter(ItemOrders.order_no==order_no)
    #     return query

    def query_item_by_item_id(self,item_id,order_id):
        '''
        根据商品id下查询所有购买的商品信息
        :param order_id:
        :return:
        '''
        query = self.rdb.query(ItemDetail.id,ItemDetail.main_pic,ItemDetail.price,ItemDetail.orgin_price,ItemOrders.order_no,
                               ItemDetail.inner_price,ItemDetail.title,ItemOrders.buy_nums,ItemDetail.top_category_id,
                               ItemOrders.item_price,ItemOrders.total_amount,ItemDetail.item_no,ItemDetail.name,ItemDetail.brand,ItemDetail.amount,ItemOrders.is_apply_refund).\
                               join(ItemOrders,ItemDetail.id==ItemOrders.item_id).filter(ItemOrders.item_id==item_id,ItemOrders.order_id==order_id)
        return query


    def query_item_orders_by_id(self,item_order_id):
        '''
        根据商品id下查询所有购买的商品信息
        :param order_id:
        :return:
        '''
        # query = self.rdb.query(ItemDetail.id,ItemDetail.show_id,ItemDetail.main_pic,ItemDetail.price,ItemDetail.orgin_price,ItemOrders.order_no,
        #                        ItemDetail.inner_price,ItemDetail.title,ItemOrders.buy_nums,ItemDetail.top_category_id,ItemDetail.bussiness_price,
        #                        ItemOrders.item_price,ItemOrders.total_amount,ItemDetail.item_no,ItemDetail.name,ItemDetail.brand,ItemDetail.amount,ItemOrders.is_apply_refund).\
        #                        join(ItemOrders,ItemDetail.id==ItemOrders.item_id).filter(ItemOrders.id==item_order_id)
        # return query

        query = self.rdb.query(ItemOrders.id,ItemOrders.drp_usere_id,ItemOrders.item_price,ItemOrders.total_amount,ItemOrders.buy_nums,ItemDetail.main_pic,ItemDetail.item_no,ItemDetail.name,ItemDetail.brand,ItemDetail.amount,ItemOrders.is_apply_refund).\
                               join(ItemDetail,ItemDetail.id==ItemOrders.item_id).filter(ItemOrders.id==item_order_id)
        return query


    def query_item_by_order_no(self,order_no):
        '''
        根据订单号下查询所有购买的商品信息
        :param order_id:
        :return:
        '''
        query = self.rdb.query(ItemDetail.id,ItemDetail.show_id,ItemDetail.main_pic,ItemDetail.price,ItemDetail.orgin_price,ItemOrders.order_no,ItemOrders.order_id,
                               ItemDetail.inner_price,ItemDetail.title,ItemOrders.buy_nums,ItemDetail.top_category_id,
                               ItemOrders.item_price,ItemOrders.total_amount,ItemDetail.item_no,ItemDetail.name,ItemDetail.brand,ItemDetail.amount,ItemDetail.summary).\
                               join(ItemOrders,ItemDetail.id==ItemOrders.item_id).filter(ItemOrders.order_no==order_no)
        return query

    def _add_order(self,user_id=None,drp_user_id = None,supply_id = None,payable_amount=None,pay_amount=None,discount_amount=None,
                   voucher=None,user_remark=None,recevie_address=None,items=None,recevie_address_id=None,order_from=None,
                   brokerage = None,**kwargs):
        # try:
            order = Orders()
            order.order_no = ''.join([str(user_id),str(int(time.time()*100))])
            order.user_id = user_id
            order.drp_usere_id = drp_user_id

            order.supply_user_id = supply_id

            order.status = 1
            order.pay_status = 0
            order.delivery_status = 0
            order.payable_amount = payable_amount
            order.real_amount = pay_amount
            order.discount_amount = discount_amount
            order.transport_anmount = 0
            order.brokerage = brokerage
            # if voucher:
            #     order.voucher = voucher
            order.user_remark = user_remark
            order.order_type = 1
            order.recevie_address = recevie_address
            order.recevie_address_id = recevie_address_id
            order.is_asyn = False
            order.order_from = order_from
            self.db.add(order)
            self.db.flush()
            self.add_item_order(order,items,drp_user_id,supply_id)

            pay_order = self.add_payorder(order.id,order.order_no,user_id,order.real_amount,recevie_address,items[0].id,brokerage,drp_user_id,supply_id)
            self.db.commit()
            return True,order,pay_order

    def add_item_order(self,order,items,drp_user_id,supply_id):
        '''
        :todo 创建订单商品
        :param order:
        :param items:
        :return:
        '''
        for item in items:
            item_order = ItemOrders()
            item_order.order_id = order.id
            item_order.order_no = order.order_no
            item_order.item_id = item.id
            item_order.is_drp_item = item.is_drp_item
            item_order.drp_usere_id = item.drp_user_id
            item_order.buy_nums = item.num      #购买数量
            item_order.item_price = item.price
            item_order.total_amount = item.price*int(item.num)
            item_order.drp_usere_id = drp_user_id
            item_order.supply_user_id = supply_id
            self.db.add(item_order)
        self.db.flush()

    def add_payorder(self,order_id,order_no,user_id,amount,recevie_address,item_id,brokerage,drp_user_id,supply_id):
        '''
        :todo 创建支付
        :param order_id:订单ID
        :param order_no:订单序列号
        :param user_id:用户ID
        :param amount:金额
        :param recevie_address:送货地址
        :param item_id: 商品id
        :return:
        '''
        payorder = PayOrders()
        payorder.order_id = order_id
        payorder.order_no = order_no
        payorder.payment_id = ''.join([str(user_id),str(item_id),str(int(time.time()*10))])
        payorder.user_id = user_id
        payorder.drp_usere_id = drp_user_id
        payorder.supply_user_id = supply_id
        payorder.pay_status = 0
        payorder.amount  = amount
        payorder.brokerage = brokerage
        payorder.recevie_address = recevie_address
        self.db.add(payorder)
        self.db.flush()
        return payorder

    def get_order_by_order_id(self,order_id):
        '''
        根据ID获取订单
        :param order_id:
        :param user_id:
        :return:
        '''
        return self.rdb.query(Orders).filter(Orders.deleted==0,Orders.id==order_id).scalar()


    def get_payorder_by_payorder_id(self,user_id,payorder_id):
        pass

    def add_pay_logs_ehking(self,order_id,order_no,user_id,data):
        '''
        添加易汇金同步提交跳转地址等信息
        :param order_id:
        :param order_no:
        :param user_id:
        :param data:
        :return:
        '''
        payorder = PaylogsEhking()
        payorder.order_id = order_id
        payorder.order_no = order_no
        payorder.status = data['status']
        payorder.user_id = user_id
        payorder.requestId = data['requestId']
        payorder.merchantId  = data['merchantId']
        payorder.redirectUrl = data['redirectUrl']
        self.db.add(payorder)
        self.db.flush()
        self.db.commit()
        return payorder

    def get_pay_logs_ehking_by_order_id(self,order_no,user_id):
        '''
        查询该用户该笔订单是否支付过
        :param order_no:
        :param user_id:
        :return:
        '''
        return self.rdb.query(PaylogsEhking).filter(PaylogsEhking.deleted==0,PaylogsEhking.order_no==order_no,PaylogsEhking.user_id==user_id).scalar()

    def _list_itemOrders(self,order_id=None,**kwargs):
        '''
        订单商品查询
        :param order_id:
        :return:
        '''
        query = self.rdb.query(ItemOrders).filter(ItemOrders.deleted==0).order_by('gmt_created desc')
        if order_id:
            query = query.filter(ItemOrders.order_id==order_id)
        if kwargs.get('start_date'):
            query = query.filter(ItemOrders.gmt_created >= kwargs.get('start_date'))
        if kwargs.get('end_date'):
            query = query.filter(ItemOrders.gmt_created <= kwargs.get('end_date')+' 23:59:59')
        # if kwargs.get('start_price'):
        #     query = query.filter(ItemOrders.item_price >= kwargs.get('start_price'))
        # if kwargs.get('end_price'):
        #     query = query.filter(ItemOrders.item_price <= kwargs.get('end_price'))
        if kwargs.get('pay_status'):
            query = query.filter(ItemOrders.order_id.in_(self.rdb.query(Orders.id).
                                                         filter(Orders.deleted == 0,Orders.pay_status == kwargs.get('pay_status'))))
        # if kwargs.get('order_no'):
        #     order_id = self.rdb.query(Orders.id).filter(Orders.deleted == 0,Orders.order_no == kwargs.get('order_no'))
        #     query = query.filter(ItemOrders.order_id == order_id)
        if kwargs.get('item_n_t'):
            item_n_t = kwargs.get('item_n_t')
            query = query.filter(ItemOrders.item_id.in_(self.rdb.query(ItemDetail.id).filter(ItemDetail.deleted==0,or_(ItemDetail.item_no==item_n_t,ItemDetail.type==item_n_t))))
        if kwargs.get('category_id'):
            item_category_id = self.rdb.query(ItemCategory.id).filter(ItemCategory.id == kwargs.get('category_id')).scalar()
            if self.rdb.query(ItemCategory).filter(ItemCategory.deleted == 0,ItemCategory.parent_id == item_category_id).count()>0:
                query = query.filter(ItemOrders.item_id.
                                     in_(self.rdb.query(ItemDetail.id).filter(ItemDetail.deleted == 0,ItemDetail.category_id.
                                     in_(self.rdb.query(ItemCategory.id).filter(ItemCategory.deleted == 0,ItemCategory.parent_id == item_category_id)))))
            else:
                query = query.filter(ItemOrders.item_id.in_(self.rdb.query(ItemDetail.id).filter(ItemDetail.category_id == item_category_id)))
            # item_category = self.rdb.query(ItemCategory).filter(ItemCategory.name == kwargs.get('category_name')).scalar()
            # if item_category:
            #     query = query.filter(ItemDetail.category_id == item_category.id)
            # else:
            #     query = query.filter(ItemDetail.category_id == '')
        # if kwargs.get('content'):
        #     query = query.filter(or_(ItemDetail.brand.like("%"+kwargs.get('content')+"%"),ItemDetail.title.like("%"+kwargs.get('content')+"%")))
        return query
        # return self.rdb.query(ItemOrders).filter(ItemOrders.deleted==0,ItemOrders.order_id==order_id)

    def cancle_order_by_id(self,user_id,order_id,cancle_reason):
        '''
        取消订单   修改订单为取消    直接删除支付
        :param user_id:
        :param order_id:
        :return:
        '''
        orders = self.db.query(Orders).filter(Orders.deleted==0,Orders.user_id==user_id,Orders.id==order_id,Orders.status==1,Orders.pay_status==0).scalar()#(Orders.status==3,synchronize_session=False)
        pay_orders = self.db.query(PayOrders).filter(PayOrders.deleted==0,PayOrders.pay_status==0,PayOrders.order_id==order_id).scalar()#(PayOrders.pay_status==2,synchronize_session=False)
        if orders:
            orders.cancle_remark = cancle_reason
            orders.status=3
            self.db.add(orders)
            if pay_orders:
                pay_orders.pay_status=2
                self.db.add(pay_orders)
        #--取消订单 修改库存
        sql_format = 'update item_detail set sale_quantity=(sale_quantity+{0}) where id={1};'
        execute_sqls=[]
        for item in self.db.query(ItemOrders).filter(ItemOrders.order_id==orders.id):
            execute_sqls.append(sql_format.format(item.buy_nums,item.item_id))
        if execute_sqls:
            self.db.execute(''.join(execute_sqls))
        self.db.commit()

    def confirmation_receipt(self,user_id, order_id):
        '''
        用户确认收货 修改订单表里订单状态：status为2 已完成订单 ； 配货状态delivery_status为2 已签收
        （备注：order_status表里也会插入一条数据）
        :param user_id:
        :param order_id:
        :return:
        '''
        orders = self.db.query(Orders).filter(
            Orders.deleted == 0,
            Orders.user_id == user_id,
            Orders.id == order_id,
            Orders.status == 1,
            Orders.pay_status==1,
            Orders.delivery_status == 1).scalar()

        if orders:
            invoice_orders = self.db.query(InvoiceOrders).filter(InvoiceOrders.deleted==0,InvoiceOrders.order_id==orders.id,InvoiceOrders.status.in_([0,1]))
            for o in invoice_orders:
                o.status=2
                self.db.add(o)
            orders.status = 2
            orders.delivery_status = 2
            orders.completion_time = now()
            self.db.add(orders)

        self.db.commit()

    def confirmation_receipt_app(self,user_id, order_id):
        '''
        用户确认收货 修改订单表里订单状态：status为2 已完成订单 ； 配货状态delivery_status为2 已签收
        （备注：order_status表里也会插入一条数据）
        :param user_id:
        :param order_id:
        :return:
        '''
        orders = self.db.query(Orders).filter(
            Orders.deleted == 0,
            Orders.user_id == user_id,
            Orders.id == order_id,
            Orders.status == 1,
            Orders.pay_status==1,
            Orders.delivery_status == 1).scalar()

        if orders:
            invoice_orders = self.db.query(InvoiceOrders).filter(InvoiceOrders.deleted==0,InvoiceOrders.order_id==orders.id,InvoiceOrders.status.in_([0,1]))
            for o in invoice_orders:
                o.status=2
                self.db.add(o)
            orders.status = 2
            orders.delivery_status = 2
            orders.completion_time = datetime.datetime.now()
            self.db.add(orders)

        self.db.commit()

    def get_orders_info(self,**kwargs):
        '''
        todo:获取所有订单商品信息
        :return:
        '''
        query = self.rdb.\
            query(Orders.order_no,Orders.user_id,Orders.status,
                  Orders.pay_status,Orders.delivery_status,
                  Orders.recevie_address,Orders.payable_amount,
                  Orders.real_amount,Orders.order_from,Orders.gmt_created,
                  ItemOrders.id,ItemOrders.item_id,ItemOrders.item_price,ItemOrders.total_amount,ItemOrders.buy_nums,ItemOrders.order_id,
                  PayOrders.payment_id,PayOrders.other_payment_id,PayOrders.payment_time,
                  ItemDetail.item_no,ItemDetail.name,ItemDetail.brand,ItemDetail.type)\
            .outerjoin(ItemOrders,Orders.id==ItemOrders.order_id).outerjoin(PayOrders,Orders.id==PayOrders.order_id).outerjoin(ItemDetail,ItemOrders.item_id==ItemDetail.id).filter(Orders.deleted==0,ItemOrders.deleted==0,PayOrders.deleted==0,ItemDetail.deleted==0)
        # query = self.rdb.query(Orders.id,
        #                        Orders.order_no,
        #                        Orders.user_id,Orders.status,
        #                        Orders.pay_status,Orders.delivery_status,
        #                        Orders.recevie_address,Orders.payable_amount,
        #                        Orders.real_amount,Orders.tax_amount,Orders.order_from,
        #                        Orders.gmt_created).filter(Orders.deleted==0)

        if kwargs.get('order_status'):
            query = query.filter(Orders.status==kwargs.get('order_status'))
        if kwargs.get('pay_status'):
            query = query.filter(Orders.pay_status==kwargs.get('pay_status'))
        if kwargs.get('delivery_status'):
            query = query.filter(Orders.delivery_status==kwargs.get('delivery_status'))
        if kwargs.get('content'):
            content = kwargs.get('content')
            query = query.filter(or_(Orders.order_no==content,Orders.recevie_address.like("%"+content+"%")))
        if kwargs.get('pay_start_date'):
            query = query.filter(Orders.id.in_(self.rdb.query(PayOrders.order_id).filter(PayOrders.payment_time>=kwargs.get('pay_start_date')+' 00:00:00',PayOrders.deleted==0)))
        if kwargs.get('pay_end_date'):
            query = query.filter(Orders.id.in_(self.rdb.query(PayOrders.order_id).filter(PayOrders.payment_time<=kwargs.get('pay_end_date')+' 23:59:59',PayOrders.deleted==0)))
        if kwargs.get('start_date'):
            query = query.filter(Orders.gmt_created >= kwargs.get('start_date')+' 00:00:00')
        if kwargs.get('end_date'):
            query = query.filter(Orders.gmt_created <= kwargs.get('end_date')+' 23:59:59')
        return query

    def get_ItemsOrder_info(self,order_id):
        '''
        todo:
        :param order_id:
        :return:
        '''
        query = self.rdb.query(ItemOrders.item_id,ItemOrders.buy_nums,ItemOrders.item_price)\
            .filter(ItemOrders.deleted==0,ItemOrders.order_id==order_id)
        return query

    def mark_comment(self,user_id,order_no,assess_type):
        orders = self.db.query(Orders).filter(
                Orders.deleted == 0,
                Orders.user_id == user_id,
                Orders.id == order_no).scalar()
        if orders:
            if assess_type == 'one':
                orders.is_assess = 1
            else:
                orders.is_addition_assess = 1
            self.db.add(orders)
            self.db.commit()

    def get_category_id_by_order_id(self,order_id):
        query = self.rdb.query(ItemDetail.category_id,).join(ItemOrders,ItemDetail.id==ItemOrders.item_id).filter(ItemOrders.order_id==order_id)
        return query

    def add_settlement(self,admin_id,drp_usere_id,count,payment_no,content,settlement_no):
        try:
                settlement = Settlement()
                settlement.drp_usere_id = drp_usere_id
                settlement.payment_no = payment_no
                settlement.settlement_amount = count
                settlement.settlement_no = settlement_no
                settlement.admin_id = admin_id
                settlement.content = content
                self.db.add(settlement)
                self.db.commit()
        except Exception,e:
                return False
        return True

    def get_order_total_count(self):
        '''
        获取有效的订单总数
        :return:
        '''
        return self.rdb.query(Orders.id).filter(Orders.deleted==0,
                                                Orders.status==1,
                                                Orders.pay_status==1).count()

    def get_order_total_amount(self):
        '''
        获取订单总金额
        :return:
        '''

        return self.rdb.query(func.sum(PayOrders.amount)).filter(PayOrders.deleted==0,PayOrders.pay_status==1).scalar()


    def get_item_orders_list(self):
        '''
        销售排行（根据销售量）
        :return:
        '''
        mysql = '''
                select item_id, sum(buy_nums) as buy_nums ,sum(total_amount) as total_amount from item_orders
                where deleted=0 group by item_id order by buy_nums desc;'''
        query = self.rdb.execute(mysql)
        return query

    def drp_item_orders_list(self):
        '''
        分销商销售排行
        :param drp_usere_id:
        :return:
        '''
        mysql = '''
                select drp_usere_id, sum(buy_nums) as buy_nums ,sum(total_amount) as total_amount from item_orders
                where deleted=0 group by drp_usere_id order by buy_nums desc;'''
        query = self.rdb.execute(mysql)
        return query