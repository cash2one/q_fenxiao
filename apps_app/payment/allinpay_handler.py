#encoding:utf-8
__author__ = 'wangjinkuan'

from services.orders.orders_services import OrderServices
from services.payments.payorder_services import PayOrderService
from apps_app.common_handler import CommonHandler
from common.allinpay.allinpay import create_pay_info
from setting import PAYMENT_BACK_HOST
import datetime
import rsa
import base64
import ujson

order_services = OrderServices()
payorder_service = PayOrderService()

class AllinPayPaymentHandler(CommonHandler):
    def get(self,user_id,order_id,order_no):
        payorder_service.set_rdb(self.rdb)
        pay_order = payorder_service.get_payorder_by_order_id(order_id,user_id)
        order_services.set_rdb(self.rdb)
        order = order_services.get_order_no(order_no,user_id)
        user_address = ujson.loads(order.recevie_address)
        card_num = user_address.get('card_num')
        card_num = '01'+card_num
        # 身份证号rsa加密
        pubkey = rsa.PublicKey(149380992406927500716241361923785654160314473712177262569404352542855462290905900996898820349830223450863291102361998356737565352204766003197145257743784108967049311092979500247005291724928627891055953026325337822510580077557484401424165589043287424587640610886383070856297739481742150528531012906820072406507, 65537)
        crypto = rsa.encrypt(str(card_num), pubkey)
        card_num_rsa = base64.b64encode(crypto)
        user_name = user_address.get('user_name')
        if pay_order.pay_status == 0:
            gmt_created = datetime.datetime.strftime(pay_order.gmt_created,'%Y%m%d%H%M%S')
            payback_url = self.reverse_url('allinpay_payment_payback',order_id,order_no)

            params = create_pay_info(pay_order.order_no,'','', pay_order.amount,gmt_created,card_num_rsa,user_name,
                                     return_url=PAYMENT_BACK_HOST+payback_url,
                                     notify_url=PAYMENT_BACK_HOST+payback_url)

            self.echo('mobile/pay/allinpayment.html',{'params':params})