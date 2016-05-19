#encoding:utf-8
__author__ = 'wangjinkuan'

from common.base_handler import AdminBaseHandler
from apps_admin.common_handler import CommonHandler
from services.payments.payorder_services import PayOrderService
from services.orders.orders_services import OrderServices
from conf.orders_conf import PAYMENT_STATUS,PAY_TYPE
from services.express.express_services import ExpressServices
from services.distributor.distributor_service import DistributorUserservice
from services.merchant.merchant_services import MerchantService
import os

payorder_service = PayOrderService()
order_service = OrderServices()
distributor_service = DistributorUserservice()
merchant_services = MerchantService()

class PaymentHandler(CommonHandler):

    def get(self, *args, **kwargs):
        payorder_service.set_rdb(self.rdb)
        start_date = self.get_argument('start_date','')
        end_date = self.get_argument('end_date','')
        order_no = self.get_argument('order_no','')
        pay_status = self.get_argument('pay_status','')
        pay_type = self.get_argument('pay_type','')
        supply_user_id = self.get_argument('supply_user_id','')
        drp_usere_id = self.get_argument('drp_usere_id','')
        settlement = self.get_argument('settlement','')

        distributor_service.set_rdb(self.rdb)

        distributors = distributor_service.get_all_distributor_users(type=0) #分销商
        vendors = distributor_service.get_all_distributor_users(type=1)#供应商

        query = payorder_service._list(order_no=order_no,pay_type=pay_type,pay_status=pay_status,start_date=start_date,
                                       end_date=end_date,supply_user_id=supply_user_id,drp_usere_id=drp_usere_id,settlement=settlement)
        payOrders = self.get_page_data(query)
        self.echo('admin/payment/payment_list.html',
                  {'data':payOrders,
                   'PAYMENT_STATUS':PAYMENT_STATUS,
                   'PAY_TYPE':PAY_TYPE,
                   'pay_type':pay_type,
                   'order_no':order_no,
                   'pay_status':pay_status,
                   'start_date':start_date,
                   'supply_user_id':supply_user_id,
                   'drp_usere_id':drp_usere_id,
                   'distributors':distributors,
                   'vendors':vendors,
                   'end_date':end_date,
                   'settlement':settlement,
                   'count':query.count()
                  })

class PaymentErrorDealHandler(AdminBaseHandler):
    def get(self,order_no, **kwargs):
        payorder_service.set_rdb(self.rdb)
        payorder_service.set_db(self.db)
        pay_order = payorder_service.get_payorder_by_order_no(order_no)
        if pay_order.pay_status==0:
            is_success,info = payorder_service.set_paysuccess(pay_order.id,pay_order.order_no,1,pay_type=7,other_payment_id=other_payment_id)
            if is_success:
                order_service.set_rdb(self.db)
                express_service = ExpressServices(db=self.db)
                items = order_service.query_item_by_order_id(order_id=pay_order.order_id)
                order = order_service.get_order_by_order_id(pay_order.order_id)
                express_service._add(order)
                yh_order_obj = YhOrderApi(self.db)
                yh_order_obj.create_order_params(pay_order,order,items)
                yh_order_obj.start()
                self.write('OK')
            else:
                self.write('更新支付状态成功')

import xlwt
class PaymentExcelHandler(CommonHandler):
    def get(self, *args, **kwargs):
        self.get_paras_dict()
        payorder_service.set_rdb(self.rdb)
        query = payorder_service._list(**self.qdict)
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('pay',cell_overwrite_ok=True)
        try:
            ws.write(0,0,u'订单号')
            ws.write(0,1,u'支付ID')
            ws.write(0,2,u'第三方支付号')
            ws.write(0,3,u'支付状态')
            ws.write(0,4,u'支付类型')
            ws.write(0,5,u'支付金额')
            ws.write(0,6,u'支付时间')
            ws.write(0,7,u'分销商')
            ws.write(0,8,u'佣金是否结算')
            ws.write(0,9,u'佣金金额')
            ws.write(0,10,u'结算编码')
            index = 1
            for data in query:
                ws.write(index,0,data.order_no)
                ws.write(index,1,data.payment_id)
                ws.write(index,2,data.other_payment_id)
                if data.pay_status == 0:
                    ws.write(index,3,u'等待支付')
                elif data.pay_status == 1:
                    ws.write(index,3,u'支付成功')
                else:
                    ws.write(index,3,u'取消支付')

                if data.pay_type == 7:
                    ws.write(index,4,u'通联支付')
                elif data.pay_type == 8:
                    ws.write(index,4,u'易汇金')
                elif data.pay_type == 6:
                    ws.write(index,4,u'微信支付')
                elif data.pay_type == 9:
                    ws.write(index,4,u'支付宝')
                else:
                    ws.write(index,4,u'')

                ws.write(index,5,data.amount)
                if data.payment_time:
                    ws.write(index,6,data.payment_time.strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    ws.write(index,6,'')
                ws.write(index,7,self.get_distributors_by_id(data.drp_usere_id))
                if not data.settlement:
                    ws.write(index,8,u'否')
                else:
                    ws.write(index,8,u'是')

                ws.write(index,9,data.brokerage)
                ws.write(index,10,data.settlement_no)
                index += 1


            wb.save('pay.xls')
            _file_dir = os.path.abspath("")
            _file_path = "%s/%s" % (_file_dir, 'pay.xls')
            self.set_header('Content-Type', 'application/force-download')
            self.set_header('Content-Disposition', 'attachment; filename=%s' % 'pay.xls')
            with open(_file_path, "rb") as f:
                while True:
                    _buffer = f.read(4096)
                    if _buffer:
                        self.write(_buffer)
                    else:
                        f.close()
                        self.finish()
                        return
        except Exception,e:
            print e.message
        # self.get_paras_dict()
        # payorder_service.set_rdb(self.rdb)
        # query = payorder_service._list(**self.qdict)
        # try:
        #     csvfile = file('pay.csv', 'wb')
        #     writer = csv.writer(csvfile)
        #     writer.writerow(['订单号','支付ID','第三方支付号','支付状态','支付类型','支付金额','支付时间'])
        #     lst_data = []
        #     for data in query:
        #         if data.pay_status == 0:
        #             p_status = u'等待支付'
        #         elif data.pay_status == 1:
        #             p_status = u'支付成功'
        #         else:
        #             p_status = u'取消支付'
        #         if data.pay_type == 7:
        #             p_type = u'通联支付'
        #         elif data.pay_type == 8:
        #             p_type = u'易宝支付'
        #         elif data.pay_type == 6:
        #             p_type = u'微信支付'
        #         elif data.pay_type == 9:
        #             p_type = u'支付宝'
        #         else:
        #             p_type = ''
        #         lst_data.append([data.order_no,data.payment_id,data.other_payment_id,p_status,p_type,data.amount,data.payment_time])
        #     for data in lst_data:
        #         writer.writerow(data)
        #     csvfile.close()
        #     _file_dir = os.path.abspath("")
        #     _file_path = "%s/%s" % (_file_dir, 'pay.csv')
        #     self.set_header('Content-Type', 'application/force-download')
        #     self.set_header('Content-Disposition', 'attachment; filename=%s' % 'pay.csv')
        #     with open(_file_path, "rb") as f:
        #         while True:
        #             _buffer = f.read(4096)
        #             if _buffer:
        #                 self.write(_buffer)
        #             else:
        #                 f.close()
        #                 self.finish()
        #                 return
        # except Exception,e:
        #     print e.message