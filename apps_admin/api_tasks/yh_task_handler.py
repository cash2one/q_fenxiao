#encoding:utf-8
__author__ = 'binpo'

from common.base_handler import AdminBaseHandler

from services.payments.payorder_services import PayOrderService
from services.orders.orders_services import OrderServices

payorder_service = PayOrderService()
order_service = OrderServices()

class YhTaskHandler(AdminBaseHandler):

    def get(self, *args, **kwargs):
        order_no = self.get_argument('order_no')
        payorder_service.set_rdb(self.db)
        pay_order = payorder_service.get_payorder_by_order_no(order_no)
        order_id = pay_order.order_id
        payorder_service.set_db(self.db)
        order_service.set_rdb(self.rdb)
        items = order_service.query_item_by_order_id(order_id=order_id)
        order = order_service.get_order_by_order_id(order_id)
        if not order.is_asyn:
            yh_order_obj = YhOrderApi(self.db)
            if not order.is_abroad:
                order_type='3'
            else:order_type='0'
            yh_order_obj.create_order_params(pay_order,order,items,order_type=order_type)
            yh_order_obj.start()

        self.write('调用成功')
