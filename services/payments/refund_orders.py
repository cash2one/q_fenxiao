#encoding:utf-8
__author__ = 'binpo'
from models.orders_do import RefundOrders
from ..base_services import BaseService
from models.orders_do import *

class RefundOrdersService(BaseService):

    def query_by_id(self,id,status=None):
        '''
        根据id查询退款清单
        :param id:
        :return:
        '''
        return self.rdb.query(RefundOrders).filter(RefundOrders.deleted==0,RefundOrders.id==id).scalar()

    def _list(self,**kargs):

        refund_orders = self.rdb.query(RefundOrders).filter(RefundOrders.deleted==0)
        if kargs.get('order_by'):
            refund_orders = refund_orders.order_by(kargs.get('order_by'))
        else:
            refund_orders = refund_orders.order_by('gmt_created desc')
        if kargs.get('id',None):
            refund_orders = refund_orders.filter(RefundOrders.id==kargs.get('id'))
        return refund_orders

    def _add(self,*args,**kwargs):
        '''
        创建退款
        :param args:
        :param kwargs:
        :return:
        '''
        #order_id = kwargs.get('order_id')
        #user_id = kwargs.get('user_id')
        item_order = self.db.query(ItemOrders).filter(ItemOrders.deleted==0,ItemOrders.is_apply_refund!=True,ItemOrders.id==kwargs.get('item_order_id')).scalar()
        order_id = item_order.order_id
        order = self.db.query(Orders).filter(Orders.deleted==0,Orders.id==order_id).scalar()
        user_id = order.user_id
        pay_order = self.db.query(PayOrders).filter(PayOrders.deleted==0,PayOrders.order_id==order_id,PayOrders.user_id==user_id).scalar()
        refund_order = RefundOrders()
        refund_order.order_id = item_order.order_id
        refund_order.order_no = item_order.order_no
        refund_order.drp_usere_id = item_order.drp_usere_id
        refund_order.payment_id = pay_order.payment_id
        refund_order.other_payment_id = pay_order.other_payment_id
        refund_order.item_id = item_order.item_id
        refund_order.user_id = user_id
        refund_order.payment_time = pay_order.payment_time
        refund_order.order_create_time = pay_order.gmt_created
        refund_order.pay_status = 0
        refund_order.pay_type = pay_order.pay_type
        refund_order.content = kwargs.get('refund_reason')
        refund_order.apply_amount = kwargs.get('apply_amount')
        refund_order.refound_amount = kwargs.get('refound_amount')
        self.db.add(refund_order)
        self.db.flush()
        refund_order.refund_no = order.order_no+str(refund_order.id)
        self.db.add(refund_order)

        item_order.is_apply_refund=True
        order.pay_status = 2
        self.db.add(order)
        self.db.add(item_order)

        self.db.commit()
        return refund_order
