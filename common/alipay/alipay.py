# -*- coding: utf-8 -*-
import types
from urllib import urlencode, urlopen

from hashcompat import md5_constructor as md5
from common.alipay.config import settings


from Crypto.Hash import SHA
import base64
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5


def smart_str(s, encoding='utf-8', strings_only=False, errors='strict'):
    """
    Returns a bytestring version of 's', encoded as specified in 'encoding'.

    If strings_only is True, don't convert (some) non-string-like objects.
    """
    if strings_only and isinstance(s, (types.NoneType, int)):
        return s
    if not isinstance(s, basestring):
        try:
            return str(s)
        except UnicodeEncodeError:
            if isinstance(s, Exception):
                # An Exception subclass containing non-ASCII data that doesn't
                # know how to print itself properly. We shouldn't raise a
                # further exception.
                return ' '.join([smart_str(arg, encoding, strings_only,
                        errors) for arg in s])
            return unicode(s).encode(encoding, errors)
    elif isinstance(s, unicode):
        return s.encode(encoding, errors)
    elif s and encoding != 'utf-8':
        return s.decode('utf-8', errors).encode(encoding, errors)
    else:
        return s

# 网关地址
_GATEWAY = 'https://mapi.alipay.com/gateway.do?'

# 对数组排序并除去数组中的空值和签名参数
# 返回数组和链接串
def params_filter(params):
    ks = params.keys()
    ks.sort()
    newparams = {}
    prestr = ''
    for k in ks:
        v = params[k]
        k = smart_str(k, settings.ALIPAY_INPUT_CHARSET)
        if k not in ('sign','sign_type') and v != '':
            newparams[k] = smart_str(v, settings.ALIPAY_INPUT_CHARSET)
            prestr += '%s=%s&' % (k, newparams[k])
    prestr = prestr[:-1]
    return newparams, prestr


# 生成签名结果
def build_mysign(prestr, key, sign_type = 'MD5'):
    if sign_type == 'MD5':
        return md5(prestr + key).hexdigest()
    return ''


# 即时到账交易接口
def create_direct_pay_by_user(tn, subject, body, total_fee,is_qr_pay=False,return_url=None,notify_url=None,show_url=None):
    params = {}
    params['service']       = 'create_direct_pay_by_user'
    params['payment_type']  = '1'
    
    # 获取配置文件
    params['partner']           = settings.ALIPAY_PARTNER
    params['_input_charset']    = settings.ALIPAY_INPUT_CHARSET

    params['seller_email']      = settings.ALIPAY_SELLER_EMAIL
    params['return_url']        = return_url and return_url or settings.ALIPAY_RETURN_URL
    params['notify_url']        = notify_url and notify_url or settings.ALIPAY_NOTIFY_URL
    params['show_url']          = show_url and show_url or settings.ALIPAY_SHOW_URL
    
    # 从订单数据中动态获取到的必填参数
    params['out_trade_no']  = tn        # 请与贵网站订单系统中的唯一订单号匹配
    params['subject']       = subject   # 订单名称，显示在支付宝收银台里的“商品名称”里，显示在支付宝的交易管理的“商品名称”的列表里。
    params['body']          = body      # 订单描述、订单详细、订单备注，显示在支付宝收银台里的“商品描述”里
    params['total_fee']     = total_fee # 订单总金额，显示在支付宝收银台里的“应付总额”里
    
    # 扩展功能参数——网银提前
    params['paymethod'] = 'directPay'   # 默认支付方式，四个值可选：bankPay(网银); cartoon(卡通); directPay(余额); CASH(网点支付)
    params['defaultbank'] = ''          # 默认网银代号，代号列表见http://club.alipay.com/read.php?tid=8681379
    
    # 扩展功能参数——防钓鱼
    params['anti_phishing_key'] = ''
    params['exter_invoke_ip'] = ''
    if is_qr_pay:
        params['qr_pay_mode']=0
    
    # 扩展功能参数——自定义参数
    params['buyer_email'] = ''
    params['extra_common_param'] = ''
    
    # 扩展功能参数——分润
    params['royalty_type'] = ''
    params['royalty_parameters'] = ''
    
    params,prestr = params_filter(params)
    
    params['sign'] = build_mysign(prestr, settings.ALIPAY_KEY, settings.ALIPAY_SIGN_TYPE)
    params['sign_type'] = settings.ALIPAY_SIGN_TYPE

    return _GATEWAY + urlencode(params)


# 国际支付
def create_forex_trade(order_no, item_title, body, total_fee,return_url=None,notify_url=None):
    params = {}
    params['service']       = 'create_forex_trade'
    # 获取配置文件
    params['partner']           = settings.ALIPAY_PARTNER
    params['return_url']        = return_url and return_url or settings.ALIPAY_RETURN_URL
    params['notify_url']        = notify_url and notify_url or settings.ALIPAY_NOTIFY_URL

    # 从订单数据中动态获取到的必填参数
    params['out_trade_no']  = order_no        # 请与贵网站订单系统中的唯一订单号匹配
    params['subject']       = item_title   # 订单名称，显示在支付宝收银台里的“商品名称”里，显示在支付宝的交易管理的“商品名称”的列表里。
    params['body']          = body      # 订单描述、订单详细、订单备注，显示在支付宝收银台里的“商品描述”里
    params['total_fee']     = total_fee # 订单总金额，显示在支付宝收银台里的“应付总额”里
    params['currency']      = 'USD'

    #编码
    params['_input_charset']  = settings.ALIPAY_INPUT_CHARSET

    # print params
    params,prestr = params_filter(params)

    params['sign'] = build_mysign(prestr, settings.ALIPAY_KEY, settings.ALIPAY_SIGN_TYPE)
    params['sign_type'] = settings.ALIPAY_SIGN_TYPE
    return params

# 纯担保交易接口
def create_partner_trade_by_buyer (tn, subject, body, price):
    params = {}
    # 基本参数
    params['service']       = 'create_partner_trade_by_buyer'
    params['partner']           = settings.ALIPAY_PARTNER
    params['_input_charset']    = settings.ALIPAY_INPUT_CHARSET
    params['notify_url']        = settings.ALIPAY_NOTIFY_URL
    params['return_url']        = settings.ALIPAY_RETURN_URL

    # 业务参数
    params['out_trade_no']  = tn        # 请与贵网站订单系统中的唯一订单号匹配
    params['subject']       = subject   # 订单名称，显示在支付宝收银台里的“商品名称”里，显示在支付宝的交易管理的“商品名称”的列表里。
    params['payment_type']  = '1'
    params['logistics_type'] = 'POST'   # 第一组物流类型
    params['logistics_fee'] = '0.00'
    params['logistics_payment'] = 'BUYER_PAY'
    params['price'] = price             # 订单总金额，显示在支付宝收银台里的“应付总额”里
    params['quantity'] = 1              # 商品的数量
    params['seller_email']      = settings.ALIPAY_SELLER_EMAIL
    params['body']          = body      # 订单描述、订单详细、订单备注，显示在支付宝收银台里的“商品描述”里
    params['show_url'] = settings.ALIPAY_SHOW_URL
    
    params,prestr = params_filter(params)
    
    params['sign'] = build_mysign(prestr, settings.ALIPAY_KEY, settings.ALIPAY_SIGN_TYPE)
    params['sign_type'] = settings.ALIPAY_SIGN_TYPE
    
    return _GATEWAY + urlencode(params)

# 确认发货接口
def send_goods_confirm_by_platform (tn):
    params = {}

    # 基本参数
    params['service'] = 'send_goods_confirm_by_platform'
    params['partner'] = settings.ALIPAY_PARTNER
    params['_input_charset'] = settings.ALIPAY_INPUT_CHARSET

    # 业务参数
    params['trade_no']  = tn
    params['logistics_name'] = u'怎么装物流'   # 物流公司名称
    params['transport_type'] = u'POST'
    
    params,prestr = params_filter(params)
    
    params['sign'] = build_mysign(prestr, settings.ALIPAY_KEY, settings.ALIPAY_SIGN_TYPE)
    params['sign_type'] = settings.ALIPAY_SIGN_TYPE
    
    return _GATEWAY + urlencode(params)

def notify_verify(post):
    # 初级验证--签名
    _,prestr = params_filter(post)
    mysign = build_mysign(prestr, settings.ALIPAY_KEY, settings.ALIPAY_SIGN_TYPE)
    if mysign != post.get('sign'):
        return False
    
    # 二级验证--查询支付宝服务器此条信息是否有效
    params = {}
    params['partner'] = settings.ALIPAY_PARTNER
    params['notify_id'] = post.get('notify_id')
    if settings.ALIPAY_TRANSPORT == 'https':
        params['service'] = 'notify_verify'
        gateway = 'https://mapi.alipay.com/gateway.do'
    else:
        gateway = 'http://notify.alipay.com/trade/notify_query.do'
    veryfy_result = urlopen(gateway, urlencode(params)).read()
    if veryfy_result.lower().strip() == 'true':
        return True
    return False
# post={"trade_no":"2016030421001003250242549712","sign":"a8c3eb2cb8f258b02b8165ed902805e7",
#       "currency":"USD","out_trade_no":"48145707130701","total_fee":"1.07",
#       "sign_type":"MD5","trade_status":"TRADE_FINISHED"}
# notify_verify(post)

import os
_current_path = os.path.dirname(__file__)

_private_key = _current_path+'/rsa_private_key.pem'
_alipay_public_key = _current_path+'/alipay_public_key.pem'


def create_forex_trade_for_app(order_no,item_title,body,total_fee,notify_url=None):
    params = {}

    params['service'] = 'mobile.securitypay.pay'
    params['partner'] = settings.ALIPAY_PARTNER
    params['_input_charset'] = settings.ALIPAY_INPUT_CHARSET
    params['notify_url'] = notify_url and notify_url or settings.ALIPAY_NOTIFY_URL_APP
    params['out_trade_no'] = order_no
    params['subject'] = item_title
    params['payment_type'] = '1' #默认值 1:商品购买
    params['seller_id'] = settings.ALIPAY_PARTNER
    params['total_fee'] = total_fee
    params['forex_biz'] = 'FP'
    params['currency'] = 'USD'
    params['body'] = body

    params,prestr = params_filter(params)

    # with open(_file_path,'rb') as privatefile:
    #     p = privatefile.read()
    #     privkey = rsa.PrivateKey.load_pkcs1(p)

    with open(_private_key,'rb') as privatefile:
        key = privatefile.read()
        rsakey = RSA.importKey(key)
        signer = PKCS1_v1_5.new(rsakey)
        digest = SHA.new()
        digest.update(prestr)
        sign = signer.sign(digest)
        signature = base64.b64encode(sign)


    params['sign'] = signature
    params['sign_type'] = settings.ALIPAY_SIGN_TYPE_APP

    return params


# [0:32:16] not in asn1Spec: TagMap:
# posMap:
# [0:0:2] -> Integer,


#支付宝app回调验证
def notify_verify_for_app(post):

    _,message = params_filter(post)
    signature = post.get('sign')

    with open(_alipay_public_key,'rb') as publicfile:
        key = publicfile.read()
        rsakey = RSA.importKey(key)
        verifier = PKCS1_v1_5.new(rsakey)
        digest = SHA.new()
            # Assumes the data is base64 encoded to begin with
        digest.update(message)
        is_verify = verifier.verify(digest, base64.b64decode(signature))

    # with open(_file_path,'rb') as publicfile:
    #     p = publicfile.read()
    #     pubkey = rsa.PublicKey.load_pkcs1(p)
    #     try:
    #         is_verify = rsa.verify(message,base64.b64decode(signature),pubkey)
    #     except Exception,e:
    #         is_verify = False
    #
    if not is_verify:
        return False

    params = {}
    params['partner'] = settings.ALIPAY_PARTNER
    params['notify_id'] = post.get('notify_id')
    if settings.ALIPAY_TRANSPORT == 'https':
        params['service'] = 'notify_verify'
        gateway = 'https://mapi.alipay.com/gateway.do'
    else:
        gateway = 'http://notify.alipay.com/trade/notify_query.do'
    veryfy_result = urlopen(gateway, urlencode(params)).read()
    if veryfy_result.lower().strip() == 'true':
        return True
    return False