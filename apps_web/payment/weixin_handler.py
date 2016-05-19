#encoding:utf-8
__author__ = 'binpo'
from common.weixin_pay.wzhifuSDK import *
from common.base_handler import BaseHandler
import tornado
from models.user_do import Users
import tornado.web
from services.payments.payorder_services import PayOrderService
from services.orders.orders_services import OrderServices

import ujson,sys
from services.express.express_services import ExpressServices
from services.logs.logs_services import LogsServices
from utils.logs import LOG
from data_cache.user_cache import UserCache

from setting import PAYMENT_BACK_HOST
import StringIO
from conf.weixin_pay_conf import js_wxpay,qr_wxpay
pay_order_service = PayOrderService()
order_service = OrderServices()

pay_log = LOG('weixin_pay')


payorder_service = PayOrderService()
order_service = OrderServices()
user_cache = UserCache()

class WeixinPayment(BaseHandler):

    @tornado.web.authenticated
    def get(self,order_no, **kwargs):
        # bespeaker_payorder.set_db(self.db)
        user_id = self.current_user.get('id')
        pay_order_service.set_rdb(self.rdb)
        order_service.set_rdb(self.rdb)
        order = order_service.get_order_no(order_no,user_id)
        payorder = pay_order_service.get_payorder_by_order_no(order_no)

        ################################
        # timeStamp = time.time()
        # out_trade_no = order_no#str(payorder.id)+"{0}".format(int(timeStamp*100))
        # order_service.set_rdb(self.rdb)
        # items = order_service.query_item_by_order_no(order_no)
        # for item in items:
        #     product = {
        #         'attach':item.title ,
        #         'body': item.summary,
        #         'out_trade_no': out_trade_no,
        #         'total_fee': payorder.amount,
        #     }
        #     break
        # qr_wxpay.ip = self.get_client_ip
        # qr_pay_code = qr_wxpay._generate_unfiedorder_url(product)
        # img = qr_wxpay.generate_product_qr(product)
        # img_io = StringIO.StringIO()
        #################################
        self.echo('order/weixin.html',{'pay_order':payorder,'order':order,'order_no':order_no},layout='order/order_base.html')

    @tornado.web.authenticated
    def post(self, order_no, **kwargs):
        pay_order_service.set_rdb(self.rdb)
        payorder = pay_order_service.get_payorder_by_order_no(order_no)
        if payorder:
            if payorder.pay_status==0:
                self.write_json({'state':400,'info':''})
            else:
                self.write_json({'state':200,'info':self.reverse_url('pay_order',order_no)})
        else:
            self.write_json({'state':400,'info':'或订单不存在'})

class WeixinAccessToken(BaseHandler):

    def get(self,order_no,**kwargs):

        code = self.get_argument('code')
        jsApi = JsApi_pub()
        jsApi.code = code
        open_id = jsApi.getOpenid()
        user_id = self.current_user.get('id')
        user = self.db.query(Users).filter(Users.id==user_id).scalar()
        # if open_id:
        #     openid = open_id
        # else:openid = user.weixin
        pay_order_service.set_db(self.db)
        payorder = pay_order_service.get_payorder_by_order_no(order_no)

        jsApi = JsApi_pub()
        # # redirect_url = ''
        # # jsApi.createOauthUrlForCode()
        # # openid = jsApi.getOpenid()
        unifiedOrder = UnifiedOrder_pub()
        unifiedOrder.set_ip(self.get_client_ip)
        unifiedOrder.setParameter("openid",open_id) #open_id
        unifiedOrder.setParameter("body",'') #商品描述
        timeStamp = time.time()
        out_trade_no = str(payorder.id)+"{0}".format(int(timeStamp*100))
        unifiedOrder.setParameter("out_trade_no", out_trade_no) #商户订单号
        payorder.other_payment_id = out_trade_no
        self.db.add(payorder)
        self.db.commit()

        unifiedOrder.setParameter("total_fee", str(int(payorder.amount)*100)) #总金额
        unifiedOrder.setParameter("notify_url", WxPayConf_pub.NOTIFY_URL) #通知地址
        unifiedOrder.setParameter("trade_type", "JSAPI") #交易类型

        prepay_id = unifiedOrder.getPrepayId()
        jsApi.setPrepayId(prepay_id)
        jsApiParameters = jsApi.getParameters()

        link_pub =  NativeLink_pub()
        link_pub.parameters = jsApiParameters
        link_pub.setParameter(jsApiParameters,jsApiParameters)
        qr_code_url = link_pub.getUrl()
        print qr_code_url
        #self.redirect(qr_code_url)

        # bespeaker_payorder.set_db(self.db)
        # payorder = bespeaker_payorder.get_payorder_by_pay_id(pay_order_id)
        # #self.echo('h5/orders/weixin_pay.html',{'pay_order_id':pay_order_id,'open_id':open_id,'payorder':payorder},layout='')
        # self.redirect('/mobile/weixin/pay/orders/?pay_order_id='+str(pay_order_id)+'&open_id='+open_id)

class WeixinQcodeHandler(BaseHandler):
    '''微信网站二维码支付'''

    @tornado.web.authenticated
    def get(self,order_no, **kwargs):
        # pay_order_service.set_db(self.db)
        pay_order_service.set_rdb(self.rdb)
        payorder = pay_order_service.get_payorder_by_order_no(order_no)
        timeStamp = time.time()
        out_trade_no = order_no#str(payorder.id)+"{0}".format(int(timeStamp*100))
        order_service.set_rdb(self.rdb)
        items = order_service.query_item_by_order_no(order_no)
        for item in items:
            product = {
                'attach':item.title ,
                'body': item.summary,
                'out_trade_no': out_trade_no,
                'total_fee': payorder.amount,
            }
            break
        qr_wxpay.ip = self.get_client_ip
        img = qr_wxpay.generate_product_qr(product)
        img_io = StringIO.StringIO()
        # img.save(img_io)  # 直接将生成的QR放在了内存里, 请根据实际需求选择放在内存还是放在硬盘上
        # img_io.seek(0)
        # print img_io
        img.save(img_io)  # 直接将生成的QR放在了内存里, 请根据实际需求选择放在内存还是放在硬盘上
        img_data = img_io.getvalue()
        img_io.close()
        self.set_header('Content-Type','image/png')
        self.write(img_data)


class MyError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class WeixinPayNotify(BaseHandler):

    def check_xsrf_cookie(self):
        pass

    def get(self):
        self.post()

    def post(self, *args, **kwargs):

        xml_str = self.request.body
        pay_log.warning(ujson.dumps(xml_str))
        payorder_service.set_rdb(self.rdb)
        order_service.set_rdb(self.rdb)
        order_service.set_db(self.db)
        payorder_service.set_db(self.db)
        ret, ret_dict = qr_wxpay.verify_notify(xml_str)
        try:
            LogsServices(db=self.db).new_api_logs(
                logs_type=3,
                key_params=ret_dict.get('out_trade_no'),
                reqeust_url=self.request.host,
                params=xml_str,
                action='post',
                result='',
                status=1,
                error=''
            )
        except:
            pass

        # 在这里添加订单更新逻辑
        if ret:
            order_no = ret_dict.get('out_trade_no')
            total_fee = ret_dict.get('total_fee')

            other_payment_id = ret_dict.get('transaction_id')
            payment_time = ret_dict.get('time_end')
            pay_order = payorder_service.get_payorder_by_order_no(order_no)
            order_id = pay_order.order_id

            if int(total_fee)==int(round(pay_order.amount*100)):
                order = order_service.get_order_by_order_id(order_id)
                if pay_order.pay_status!=1:
                    is_success,info = payorder_service.set_paysuccess(pay_order.id,pay_order.order_no,1,pay_type=6,
                                                                      other_payment_id=other_payment_id,
                                                                      payment_time=payment_time)
                    if is_success:
                        try:
                            user_cache.delete_user_daily_pay(order_id)
                            address = ujson.loads(order.recevie_address)
                            categories = order_service.get_category_id_by_order_id(order_id)
                            for c in categories:
                                user_cache.set_daily_buy_cache(c.category_id,address.get('card_num'))
                        except:
                            pass

                        try:
                            express_service = ExpressServices(db=self.db)
                            items = order_service.query_item_by_order_id(order_id=order_id)
                            express_service._add(order)
                        except Exception,e:
                            self.captureMessage('物流信息:')
                            self.captureException(sys.exc_info())
                        self.write('OK')
                    else:
                        pay_log.warning('支付成功修改状态失败 人工处理:'+ujson.dumps(self.qdict)+' error:'+info)
                        LogsServices(db=self.db).create_task(
                            task_type=3,
                            key_params=order_no,
                            reqeust_url=self.request.host+self.request.uri,
                            params=ujson.dumps(self.qdict),
                            action='post',
                            result='',
                            status=0,
                            error=info
                        )
                        self.captureException(info)
                        self.captureMessage('支付成功修改状态失败 人工处理:'+ujson.dumps(self.qdict))
                        self.write('OK')
                        # logger.error(info)
                        #
                        # self.write('error')
            else:
                pay_log.warning('支付金额不匹配')
                self.captureMessage('支付金额不匹配:'+ujson.dumps(self.qdict))
                raise tornado.web.HTTPError(400)

            ret_dict = {
                'return_code': 'SUCCESS',
                'return_msg': 'OK',
            }
            ret_xml = qr_wxpay.generate_notify_resp(ret_dict)
            pay_log.info(ret_xml)
        else:
            ret_dict = {
                'return_code': 'FAIL',
                'return_msg': 'verify error',
            }
            ret_xml = qr_wxpay.generate_notify_resp(ret_dict)
        self.write(ret_xml)


        # notify_pub = Notify_pub()
        # notify_pub.saveData(self.request.body)
        # self.get_paras_dict()
        # params = notify_pub.data
        # if notify_pub.checkSign():
        #     wechat_data = notify_pub.data
        #     out_trade_no = params['out_trade_no']
        #     total_fee = int(params['total_fee'])
        #     #trade_state = params['trade_state']
        #     #return_msg = params['return_msg']
        #     result_code =  params['return_code']
        #     bespeaker_payorder.set_db(self.db)
        #     pay_order = bespeaker_payorder.get_payorder_by_weixin_pay_id(out_trade_no)
        #     if pay_order:
        #         if pay_order.state==0:
        #             if result_code=='SUCCESS' and int(total_fee) == int(pay_order.total_price-pay_order.discount)*100:
        #                 company = self.db.query(DecorateCompany).filter(DecorateCompany.user_id==pay_order.merchant_id).scalar()
        #                 if company.type  and int(company.type) == 5:    #安装维修时，无效验收，直接进入已验收状态
        #                     pay_order.state = 2
        #                 else:
        #                     pay_order.state = 1
        #                 #更新代金券使用状态
        #                 if pay_order.voucher_id:
        #                     uservouchers_service.set_db(self.db)
        #                     u_v = uservouchers_service.get_user_vouchers(user_id=pay_order.user_id, voucher_id=pay_order.voucher_id, is_used=0)
        #                     u_v = u_v.first()
        #                     uservouchers_service.update_voucher(u_v.id, is_used=1)
        #
        #                     #增加历史记录
        #                     dic__history = {}
        #                     dic__history['user_id'] = pay_order.user_id
        #                     dic__history['voucher_id'] = pay_order.voucher_id
        #                     uservouchers_service.add_user_voucher_history(**dic__history)
        #
        #                 pay_order.pay_type = 3
        #                 pay_order.pay_date = datetime.datetime.now()
        #                 pay_order.gmt_modified = datetime.datetime.now()
        #                 self.db.add(pay_order)
        #                 self.db.commit()
        #                 logger.info('微信支付成功,修改订单状态')
        #                 try:
        #                     #调用celery, 创建评论的消息
        #                     msg_data = {
        #                         'text_type':'private',
        #                         'sender_id':3772,  #发送者id
        #                         'info_type':4,
        #                         'title': '订单中心', #消息标题
        #                         'link': '#' , #消息链接
        #                         'data': PAY_ORDER_PAYSUCCESS_TMP%(str(pay_order.name),str(pay_order.schedule)),  #消息内容
        #                         'code_type':'order',
        #                         'receiver_id':pay_order.merchant_id
        #                     }
        #                     create_user_message.apply_async(kwargs=msg_data)
        #
        #                     content = PAY_ORDER_PAYSUCCESS_TMP%(pay_order.name,str(pay_order.schedule))
        #                     company = self.db.query(DecorateCompany).filter(DecorateCompany.user_id==pay_order.merchant_id).scalar()
        #                     send_phone_msg(company.order_phone,content)
        #                     if int(pay_order.create_srouce) == 2:
        #                         send_phone_msg(pay_order.phone, PAY_ORDER_199_USER_TMP)
        #
        #                 except Exception:
        #                     self.captureException(sys.exc_info())
        #                 self.write('OK')
        #     else:
        #         raise MyError('订单不存在')
        # else:
        #     raise MyError('签名不正确')
        #
        #     '''
        #     微信返回值demo
        #     #  <xml><appid><![CDATA[wx8748a996a8eca249]]></appid>
        #     <bank_type><![CDATA[CFT]]></bank_type>
        #     <cash_fee><![CDATA[100]]></cash_fee>
        #     <fee_type><![CDATA[CNY]]></fee_type>
        #     <is_subscribe><![CDATA[Y]]></is_subscribe>
        #     <mch_id><![CDATA[1232450902]]></mch_id>
        #     <nonce_str><![CDATA[os4wday681yyb0fnml6kls04pdxtyw1c]]></nonce_str>
        #     <openid><![CDATA[ofeGgjqRcIK6vgSzrZbA_aTLmPCI]]></openid>
        #     <out_trade_no><![CDATA[89144048644835]]></out_trade_no>
        #     <result_code><![CDATA[SUCCESS]]></result_code>
        #     <return_code><![CDATA[SUCCESS]]></return_code>
        #     <sign><![CDATA[A51548FFF94DAFC364C8154E692358E9]]></sign>
        #     <time_end><![CDATA[20150825150733]]></time_end>
        #     <total_fee>100</total_fee>
        #     <trade_type><![CDATA[JSAPI]]></trade_type>
        #     <transaction_id><![CDATA[1009560143201508250705312056]]></transaction_id>
        #     </xml>
        #     '''