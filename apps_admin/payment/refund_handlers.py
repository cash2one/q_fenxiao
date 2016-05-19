#encoding:utf-8
__author__ = 'binpo'
from common.base_handler import AdminBaseHandler
from apps_admin.common_handler import CommonHandler
from services.payments.refund_orders import RefundOrdersService
from services.orders.orders_services import OrderServices
from common.allinpay.allinpay import refund_pay_info
import datetime
import requests
import traceback

order_service = OrderServices()
refund_service = RefundOrdersService()

class AllinPayRefundHandlers(CommonHandler):

    def get(self,*args, **kwargs):
        self.get_paras_dict()
        refund_service.set_rdb(self.rdb)
        query = refund_service._list(**self.qdict)
        data = self.get_page_data(query)
        self.echo('admin/refund/refund_list.html',{'data':data,'params':self.qdict})

    def post(self, *args, **kwargs):
        pass


class OrderRefundHandler(AdminBaseHandler):

    def get(self,order_id, *args, **kwargs):
        operation=self.get_argument('operation',None)
        if operation=='refund_items':
            # '参数为 order_id'
            order_service.set_rdb(self.rdb)
            order_items = order_service.query_buy_items_by_order_id(order_id)
            self.echo('admin/refund/refund_items.html',{'items':order_items,'order_id':order_id})
        elif operation=='refund':
            #'参数为 order_id'
            from models.orders_do import ItemOrders
            item_order_id = self.get_argument('item_id')# itemorders_id
            order_items = order_service.query_item_orders_by_id(item_order_id)
            #item = order_items.filter(ItemOrders.item_id==item_id).scalar()
            self.echo('admin/refund/refund_form.html',{'order_items':order_items,'order_id':item_order_id})
        else:
            #'参数为 refund_id'
            order_service.set_rdb(self.rdb)
            refund_service.set_rdb(self.rdb)
            refund = refund_service.query_by_id(order_id)               #退单
            items = order_service.query_item_by_item_id(refund.item_id,refund.order_id)#退款商品
            self.echo('admin/refund/refund_detail.html',{'refund':refund,'items':items})
        #else:
        #     #'参数为 refund_id'
        #     refund_service.set_rdb(self.rdb)
        #     refund = refund_service.query_by_id(order_id)
        #     refund_url = 'https://service.allinpay.com/gateway/index.do'
        #     params = refund_pay_info(self.get_client_ip,'',refund.order_no,datetime.datetime.strftime(refund.order_create_time,'%Y%m%d%H%M%S'),refund.refound_amount,refund.refund_no)
        #     #requests.pyopenssl.connection
        #     resp = requests.post((refund_url),data=params)
        #     result = resp.content
        #     if 'ERRORCODE' in result and 'ERRORMSG' in result:
        #         self.write_json({'state':401,'info':result})
        #     else:
        #         refund.pay_status = 2
        #         self.db.add(refund)
        #         self.write_json({'state':200,'info':'已提交退款'})
        #    self.write('请求不存在')
            #self.echo('admin/refund/allinpay_refund.html',{'params':params,'refund':refund})

    def post(self, *args, **kwargs):
        #{'buy_nums': '1', 'file-2': '11111.jpg', 'money': '388.0',
        # 'refund_item_img': 'C:\\fakepath\\11111.jpg',
        # 'item_count': '1', 'reason': 'sdsdsd', 'total_ammout': '388.0'}
        self.get_paras_dict()
        refund_service.set_db(self.db)
        order_service.set_rdb(self.rdb)
        #order = order_service.get_order_by_order_id(self.qdict.get('order_id'))
        # order_id = kwargs.get('order_id')
        # user_id = kwargs.get('user_id')
        # refund_order.content = kwargs.get('refund_reason')
        # refund_order.apply_amount = kwargs.get('apply_amount')
        # refund_order.refound_amount = kwargs.get('apply_amount')
        # #refund_money
        refund_service._add(item_order_id=self.qdict.get('item_order_id',None),refund_reason=self.qdict.get('reason'),apply_amount=self.qdict.get('refund_money'),
                            refound_amount=self.qdict.get('refund_money'),drp_usere_id=self.qdict.get('drp_usere_id'))
        self.redirect(self.reverse_url('refund_list'))
            #order_items.filter()
            # self.echo('admin/refund/refund_form.html',{'items':order_items})
        # refund_service.set_rdb(self.rdb)
        # refund_order = refund_service.query_by_id(refund_order_id)
        # if refund_order:
        #     self.echo('admin/pament')


from libs.wxpay import  WXpay
from models.orders_do import PayOrders

class RefundDealHandler(AdminBaseHandler):
     def get(self,refund_id, *args, **kwargs):
        #'参数为 refund_id'
        refund_service.set_rdb(self.rdb)
        refund = refund_service.query_by_id(refund_id)

        if not refund:
            self.write_json({'state':400,'info':'退款不存在'})
        elif refund and refund.pay_status!=0:
            self.write_json({'state':400,'info':'退款已处理'})
        else:
            if refund.pay_type==7:
                refund_url = 'https://service.allinpay.com/gateway/index.do'
                params = refund_pay_info(self.get_client_ip,'',refund.order_no,datetime.datetime.strftime(refund.order_create_time,'%Y%m%d%H%M%S'),refund.refound_amount,refund.refund_no)
                #requests.pyopenssl.connection
                resp = requests.post((refund_url),data=params)
                result = resp.content
                if 'ERRORCODE' in result and 'ERRORMSG' in result:
                    self.write_json({'state':401,'info':result})
                else:
                    refund.pay_status = 2
                    refund.handling_time = datetime.datetime.now()
                    self.db.add(refund)
                    self.db.commit()
                    self.write_json({'state':200,'info':'已提交退款'})
            elif refund.pay_type==8:
                self.write_json({'state':200,'info':'易宝支付退款正在开发'})
            elif refund.pay_type==5:
                wx_pay = WXpay()
                wx_pay.ip = self.get_client_ip

                # out_trade_no=None
                # transaction_id=None
                # total_fee=None
                # refund_fee=None
                pay_order = self.rdb.query(PayOrders).filter(PayOrders.other_payment_id==refund.other_payment_id).scalar()

                out_trade_no = pay_order.order_no
                transaction_id = pay_order.other_payment_id
                total_fee = pay_order.amount
                refund_fee = refund.refound_amount
                refound_status=None
                try:
                    refound_status = wx_pay.refundorder(out_trade_no=out_trade_no,transaction_id=transaction_id,total_fee=total_fee,refund_fee=refund_fee)
                    if refound_status:
                        refund.pay_status = 2
                        refund.handling_time = datetime.datetime.now()
                        self.db.add(refund)
                        self.db.commit()
                        self.write_json({'state':200,'info':'微信退款成功'})
                    else:
                        self.write_json({'state':200,'info':'微信退款失败'})
                except:
                    self.write_json({'state':200,'info':traceback.format_exc()})


