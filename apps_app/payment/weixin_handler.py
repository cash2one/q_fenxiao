#encoding:utf-8
__author__ = 'binpo'
from common.weixin_pay.wzhifuSDK import *
from common.base_handler import BaseHandler
import tornado
import sys
import datetime
import ujson
from models.user_do import Users
from utils.logs import LOG
from services.payments.payorder_services import PayOrderService
from setting import PAYMENT_BACK_HOST

pay_order_service = PayOrderService()

log = LOG('weixin_pay')
class WeixinPayment(BaseHandler):

    @tornado.web.authenticated
    def get(self,order_no, **kwargs):
        # bespeaker_payorder.set_db(self.db)
        user_id = self.current_user.get('id')
        pay_order_service.set_db(self.db)
        payorder = pay_order_service.get_payorder_by_order_no(order_no)
        if payorder:
            if payorder.pay_status==0:
                jsApi = JsApi_pub()
                url = jsApi.createOauthUrlForCode(PAYMENT_BACK_HOST+self.reverse_url('weixin_access_token',order_no))
                self.redirect(url)
            else:self.write('订单已经支付')
        else:
            self.write('或订单不存在')

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
        unifiedOrder.setParameter("body",pay_order.remark or '暂无商品描述') #商品描述
        timeStamp = time.time()
        out_trade_no = str(payorder.id)+"{0}".format(int(timeStamp*100))
        unifiedOrder.setParameter("out_trade_no", out_trade_no) #商户订单号
        payorder.other_payment_id = out_trade_no
        self.db.add(pay_order)
        self.db.commit()
        unifiedOrder.setParameter("total_fee", str((pay_order.amount)*100)) #总金额
        unifiedOrder.setParameter("notify_url", WxPayConf_pub.NOTIFY_URL) #通知地址
        unifiedOrder.setParameter("trade_type", "JSAPI") #交易类型
        prepay_id = unifiedOrder.getPrepayId()
        jsApi.setPrepayId(prepay_id)
        jsApiParameters = jsApi.getParameters()
        link_pub =  NativeLink_pub()
        qr_code_url = link_pub.getUrl()

        bespeaker_payorder.set_db(self.db)
        payorder = bespeaker_payorder.get_payorder_by_pay_id(pay_order_id)
        #self.echo('h5/orders/weixin_pay.html',{'pay_order_id':pay_order_id,'open_id':open_id,'payorder':payorder},layout='')
        self.redirect('/mobile/weixin/pay/orders/?pay_order_id='+str(pay_order_id)+'&open_id='+open_id)

class PayOrders(BaseHandler):

    @tornado.web.authenticated
    def get(self, *args, **kwargs):

        pay_order_id = self.get_argument('pay_order_id')

        open_id = self.get_argument('open_id')
        user_id = self.current_user.get('id')
        user = self.db.query(Users).filter(Users.id==user_id).scalar()
        if open_id:
            openid = open_id
        else:openid = user.weixin
        jsApi = JsApi_pub()
        # # redirect_url = ''
        # # jsApi.createOauthUrlForCode()
        # # openid = jsApi.getOpenid()
        unifiedOrder = UnifiedOrder_pub()
        unifiedOrder.set_ip(self.get_client_ip)
        unifiedOrder.setParameter("openid",openid) #open_id
        unifiedOrder.setParameter("body",pay_order.remark or '暂无商品描述') #商品描述
        timeStamp = time.time()
        out_trade_no = str(pay_order.id)+"{0}".format(int(timeStamp*100))
        unifiedOrder.setParameter("out_trade_no", out_trade_no) #商户订单号
        pay_order.weixin_pay_order_id = out_trade_no
        self.db.add(pay_order)
        self.db.commit()
        unifiedOrder.setParameter("total_fee", str((pay_order.total_price-pay_order.discount)*100)) #总金额
        unifiedOrder.setParameter("notify_url", WxPayConf_pub.NOTIFY_URL) #通知地址
        unifiedOrder.setParameter("trade_type", "JSAPI") #交易类型
        prepay_id = unifiedOrder.getPrepayId()
        jsApi.setPrepayId(prepay_id)
        jsApiParameters = jsApi.getParameters()
        link_pub =  NativeLink_pub()
        qr_code_url = link_pub.getUrl()
        self.echo('h5/orders/orders.html',{'open_id':open_id,'jsApiParameters':jsApiParameters,'pay_order':pay_order},layout='')


class APPPayOrders(BaseHandler):
    '''
    app支付 apicloud方法一
    '''
    @tornado.web.authenticated
    def get(self, pay_order_id):

        bespeaker_payorder.set_db(self.db)
        user_id = self.current_user.get('id')

        pay_order = bespeaker_payorder.get_payorder_by_pay_order_id(pay_order_id,user_id,0)
        if not pay_order:
            return self.write({'stat':'err', 'msg':'404'})

        user_service.set_db(self.db)
        user = self.db.query(Users).filter(Users.id==user_id).scalar()

        openid = user.weixin

        unifiedOrder = UnifiedOrder_pub()
        unifiedOrder.set_ip(self.get_client_ip)
        if openid:
            unifiedOrder.setParameter("openid",openid) #open_id

        unifiedOrder.setParameter("body",pay_order.remark) #商品描述
        timeStamp = time.time()
        out_trade_no = str(pay_order.id)+"{0}".format(int(timeStamp*100))
        unifiedOrder.setParameter("out_trade_no", out_trade_no) #商户订单号

        pay_order.weixin_pay_order_id = out_trade_no
        self.db.add(pay_order)
        self.db.commit()

        unifiedOrder.setParameter("total_fee", str((pay_order.total_price-pay_order.discount)*100)) #总金额
        unifiedOrder.setParameter("notify_url", WxPayConf_pub.NOTIFY_URL) #通知地址
        unifiedOrder.setParameter("trade_type", "APP") #交易类型
        try:
            jsApi = JsApi_pub()
            prepay_id = unifiedOrder.getPrepayId()
            jsApi.setPrepayId(prepay_id)
            jsApiParameters = jsApi.getParameters_APP()
        except Exception,e:
            self.captureException(sys.exc_info())
            return self.write_json({'stat':'err', 'msg': e.message})

        # sign = unifiedOrder.getSignURLStr(unifiedOrder.parameters)

        return self.write(ujson.dumps({'stat': 'ok', 'payorder_args':jsApiParameters}))

class MyError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class WeixinPayCallBack(BaseHandler):

    def set_default_headers(self):
        self.set_header("X-XSRFToken",self.xsrf_token)

    def get(self):
        self.post()

    def post(self, *args, **kwargs):
        notify_pub = Notify_pub()
        notify_pub.saveData(self.request.body)
        self.get_paras_dict()
        params = notify_pub.data
        if notify_pub.checkSign():
            wechat_data = notify_pub.data
            out_trade_no = params['out_trade_no']
            total_fee = int(params['total_fee'])
            #trade_state = params['trade_state']
            #return_msg = params['return_msg']
            result_code =  params['return_code']
            bespeaker_payorder.set_db(self.db)
            pay_order = bespeaker_payorder.get_payorder_by_weixin_pay_id(out_trade_no)
            if pay_order:
                if pay_order.state==0:
                    if result_code=='SUCCESS' and int(total_fee) == int(pay_order.total_price-pay_order.discount)*100:
                        company = self.db.query(DecorateCompany).filter(DecorateCompany.user_id==pay_order.merchant_id).scalar()
                        if company.type  and int(company.type) == 5:    #安装维修时，无效验收，直接进入已验收状态
                            pay_order.state = 2
                        else:
                            pay_order.state = 1
                        #更新代金券使用状态
                        if pay_order.voucher_id:
                            uservouchers_service.set_db(self.db)
                            u_v = uservouchers_service.get_user_vouchers(user_id=pay_order.user_id, voucher_id=pay_order.voucher_id, is_used=0)
                            u_v = u_v.first()
                            uservouchers_service.update_voucher(u_v.id, is_used=1)

                            #增加历史记录
                            dic__history = {}
                            dic__history['user_id'] = pay_order.user_id
                            dic__history['voucher_id'] = pay_order.voucher_id
                            uservouchers_service.add_user_voucher_history(**dic__history)

                        pay_order.pay_type = 3
                        pay_order.pay_date = datetime.datetime.now()
                        pay_order.gmt_modified = datetime.datetime.now()
                        self.db.add(pay_order)
                        self.db.commit()
                        logger.info('微信支付成功,修改订单状态')
                        try:
                            #调用celery, 创建评论的消息
                            msg_data = {
                                'text_type':'private',
                                'sender_id':3772,  #发送者id
                                'info_type':4,
                                'title': '订单中心', #消息标题
                                'link': '#' , #消息链接
                                'data': PAY_ORDER_PAYSUCCESS_TMP%(str(pay_order.name),str(pay_order.schedule)),  #消息内容
                                'code_type':'order',
                                'receiver_id':pay_order.merchant_id
                            }
                            create_user_message.apply_async(kwargs=msg_data)

                            content = PAY_ORDER_PAYSUCCESS_TMP%(pay_order.name,str(pay_order.schedule))
                            company = self.db.query(DecorateCompany).filter(DecorateCompany.user_id==pay_order.merchant_id).scalar()
                            send_phone_msg(company.order_phone,content)
                            if int(pay_order.create_srouce) == 2:
                                send_phone_msg(pay_order.phone, PAY_ORDER_199_USER_TMP)

                        except Exception:
                            self.captureException(sys.exc_info())
                        self.write('OK')
            else:
                raise MyError('订单不存在')
        else:
            raise MyError('签名不正确')

            '''
            微信返回值demo
            #  <xml><appid><![CDATA[wx8748a996a8eca249]]></appid>
            <bank_type><![CDATA[CFT]]></bank_type>
            <cash_fee><![CDATA[100]]></cash_fee>
            <fee_type><![CDATA[CNY]]></fee_type>
            <is_subscribe><![CDATA[Y]]></is_subscribe>
            <mch_id><![CDATA[1232450902]]></mch_id>
            <nonce_str><![CDATA[os4wday681yyb0fnml6kls04pdxtyw1c]]></nonce_str>
            <openid><![CDATA[ofeGgjqRcIK6vgSzrZbA_aTLmPCI]]></openid>
            <out_trade_no><![CDATA[89144048644835]]></out_trade_no>
            <result_code><![CDATA[SUCCESS]]></result_code>
            <return_code><![CDATA[SUCCESS]]></return_code>
            <sign><![CDATA[A51548FFF94DAFC364C8154E692358E9]]></sign>
            <time_end><![CDATA[20150825150733]]></time_end>
            <total_fee>100</total_fee>
            <trade_type><![CDATA[JSAPI]]></trade_type>
            <transaction_id><![CDATA[1009560143201508250705312056]]></transaction_id>
            </xml>
            '''