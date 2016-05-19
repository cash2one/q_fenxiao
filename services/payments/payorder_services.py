#encoding:utf-8
__author__ = 'binpo'
from ..base_services import BaseService
from models.orders_do import PayOrders,Orders,RefundOrders,ItemOrders,Settlement
from sqlalchemy import func
from utils.logs import LOG
import traceback
pay_log = LOG('pay_success_error_logs')

class PayOrderService(BaseService):

    def get_payorder_by_order_id(self,order_id,user_id):
        '''
        根据订单id查询支付订单
        :param order_id:
        :param pay_order_id:
        :param user_id:
        :return:
        '''
        return self.rdb.query(PayOrders).filter(PayOrders.order_id==order_id,PayOrders.user_id==user_id).scalar()


    def get_payorder_by_pay_id(self,pay_order_id,user_id):
        '''
        根据订单id查询支付订单
        :param order_id:
        :param pay_order_id:
        :param user_id:
        :return:
        '''
        return self.rdb.query(PayOrders).filter(PayOrders.id==pay_order_id,PayOrders.user_id==user_id).scalar()


    # def get_payorder_by_order_id(self,order_id,pay_order_id,user_id):
    #     '''
    #     根据订单id查询支付订单
    #     :param order_id:
    #     :param pay_order_id:
    #     :param user_id:
    #     :return:
    #     '''
    #     return self.rdb.query(PayOrders).filter(PayOrders.order_id==order_id,PayOrders.user_id==user_id).scalar()
    #

    def get_payorder_by_id(self,pay_order_id,user_id):
        '''
        根据id查询支付订单
        :param order_id:
        :param pay_order_id:
        :param user_id:
        :return:
        '''
        return self.rdb.query(PayOrders).filter(PayOrders.id==pay_order_id,PayOrders.user_id==user_id).scalar()


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
        根据ID获取订单
        :param order_id:
        :param user_id:
        :return:
        '''
        return self.rdb.query(Orders).filter(Orders.deleted==0,Orders.order_no==order_no,Orders.user_id==user_id).scalar()

    def get_count_item_by_order_id(self,order_id):
        '''
        订单商品种类总数
        :param order_id:
        :return:
        '''
        return self.rdb.query(func.count('*')).filter(ItemOrders.order_id==order_id).limit(1).scalar()


    def get_itemorders_by_order_id(self,order_id):
        '''
        订单商品查询
        :param order_id:
        :return:
        '''
        return self.rdb.query(ItemOrders).filter(ItemOrders.deleted==0,ItemOrders.order_id==order_id)

    def get_payorder_by_order_no(self,order_no):
        '''
        根据订单号 获取支付订单
        :param order_no:
        :return:
        '''
        return self.rdb.query(PayOrders).filter(PayOrders.deleted==0,PayOrders.order_no==order_no).scalar()

    def set_paysuccess(self,payorder_id,order_no,pay_status,pay_type=None,other_payment_id=None,payment_time=None):
        '''
        修改订单状态
        :param payorder_id:   支付单号
        :param order_no:      订单序列号
        :param pay_status:      支付状态
        :param pay_type:        支付类型
        :param other_payment_id: 第三方产生的订单号
        :return:
        '''
        try:
            payorder = self.db.query(PayOrders).filter(PayOrders.deleted==0,PayOrders.pay_status==0,PayOrders.order_no==order_no,PayOrders.id==payorder_id).scalar()
            order = self.db.query(Orders).filter(Orders.deleted==0,Orders.order_no==order_no).scalar()
            if payorder and order:
                payorder.pay_status = pay_status
                if pay_type:
                    payorder.pay_type = pay_type
                if other_payment_id:
                    payorder.other_payment_id = other_payment_id
                payorder.payment_time = payment_time
                order.pay_status = pay_status
                if pay_status==1:
                    order.delivery_status = 0
                    order.pay_time = payment_time

                self.db.add(payorder)
                self.db.add(order)
                self.db.commit()
            return True,'OK'
        except Exception,e:
            pay_log.warning(traceback.format_exc())
            self.db.rollback()
            return False,e.message

    def _list(self,**kwargs):
        '''
        todo:获取支付单list
        :param kwargs:
        :return:
        '''
        query = self.rdb.query(PayOrders).filter(PayOrders.deleted == 0)
        if kwargs.get('drp_usere_id'):
            query = query.filter(PayOrders.drp_usere_id == kwargs.get('drp_usere_id'))
        if kwargs.get('settlement','')!='':
            query = query.filter(PayOrders.settlement == kwargs.get('settlement'))
        if kwargs.get('order_id'):
            query = query.filter(PayOrders.order_id == kwargs.get('order_id'))
        if kwargs.get('order_no'):
            query = query.filter(PayOrders.order_no == kwargs.get('order_no'))
        if kwargs.get('pay_type'):
            query = query.filter(PayOrders.pay_type == kwargs.get('pay_type'))
        if kwargs.get('pay_status'):
            query = query.filter(PayOrders.pay_status == kwargs.get('pay_status'))
        if kwargs.get('supply_user_id'):
            query = query.filter(PayOrders.supply_user_id == kwargs.get('supply_user_id'))
        if kwargs.get('drp_usere_id'):
            query = query.filter(PayOrders.drp_usere_id == kwargs.get('drp_usere_id'))
        if kwargs.get('settlement'):
            query = query.filter(PayOrders.settlement == kwargs.get('settlement'))
        if kwargs.get('start_date'):
            query = query.filter(PayOrders.payment_time >= kwargs.get('start_date')+' 00:00:00')
        if kwargs.get('end_date'):
            query = query.filter(PayOrders.payment_time <= kwargs.get('end_date')+' 23:59:59')
        if kwargs.get('order_by'):
            query = query.order_by(kwargs.get('order_by'))
        else:
            query = query.order_by('gmt_created desc')
        return query

    def settlements(self,drp_user_id=None):
        query = self.rdb.query(Settlement)#
        if drp_user_id:
            query = query.filter(Settlement.drp_usere_id==drp_user_id)
        query = query.order_by('gmt_created desc')
        return query