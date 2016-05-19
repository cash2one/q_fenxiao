# -*- coding: utf-8 -*-
import types
from urllib import urlencode, urlopen

from hashcompat import md5_constructor as md5
from common.allinpay.config import settings


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


#生成签名结果
def build_md5_sign(prestr):
    return md5(prestr).hexdigest().upper()


#即时到账交易接口  18659219272
def create_pay_info(order_no, product_name, body, total_fee,gmt_created,card_num,user_name,return_url=None,notify_url=None):
    params=[]
    params.append({"inputCharset":1})
    params.append({"pickupUrl":return_url})
    params.append({"receiveUrl":notify_url})
    params.append({"version":'v1.0'})
    params.append({"language":1})
    params.append({"signType":'0'})
    params.append({"merchantId":settings.ALLIN_PARTNER})

    params.append({"payerName":user_name})
    params.append({"payerEmail":'' })                  #付款人邮件联系方式  可空
    params.append({"payerTelephone":''})              #付款人电话联系方式  可空
    params.append({"payerIDCard":card_num})                #付款人类型及证件号 填写规则：证件类型+证件号码再使用通联公钥加密。（加密请参考示例代码） 证件类型仅支持01-身份证 跨境支付商户若采用直连模式，必须填写该值


    params.append({"pid":'' })                         #合作伙伴的商户号 可空
    params.append({"orderNo":order_no})             #商户订单号
    params.append({"orderAmount":int(round(total_fee*100))   })        #商户订单金额    整型数字，金额与币种有关 如果是人民币，则单位是分，即10元提交时金额应为1000 如果是美元，单位是美分，即10美元提交时金额为1000
    params.append({"orderCurrency":156})
    params.append({"orderDatetime":gmt_created})
    params.append({"orderExpireDatetime":''})
    params.append({"productName":product_name})        #商品名称

    params.append({"productNum":'' })                  #数量 可为空
    params.append({"productId":'' })                   #商品代码

    params.append({"productPrice":''})
    params.append({"productDesc":body})
    params.append({"ext1":""})
    params.append({"ext2":""})
    params.append({"extTL":""})
    params.append({"payType":0})                   #支付方式    固定选择值：0、1、4、11、23、28
                                                            #接入互联网关时，默认为间连模式，填0
                                                            #若需接入外卡支付，只支持直连模式，即固定上送payType=23，
                                                            # issuerId=visa或mastercard 0代表未指定支付方式，
                                                            #即显示该商户开通的所有支付方式 1个人储蓄卡网银支付 4企业网银支付 11个人信用卡网银支付
                                                            #23外卡支付
                                                            #28认证支付 非直连模式，设置为0；直连模式，值为非0的固定选择值

    params.append({"issuerId":''})
    params.append({"pan":''})
    params.append({"tradeNature":'GOODS'})
    params.append({'key':'Raychina88'})
    keys=[]
    for p in params:
        if p.values()[0]!='':
            keys.append(p.keys()[0]+'='+str(p.get(p.keys()[0])))
    sign_str = '&'.join(keys)
    #print sign_str
    params.append({'signMsg':build_md5_sign(sign_str)})
    params.append({'customsExt':''})
    print params
    return params

def refund_pay_info(ip,key,order_no,order_datetime,refund_amount,refund_order_no):
    params = {}
    serverUrl = 'https://service.allinpay.com/gateway/index.do'
    serverIP = ip
    key = 'Raychina88'
    #print ip,key,order_no,order_datetime,type(refund_amount)
    params['merchantId']=merchantId = settings.ALLIN_PARTNER
    params['version']=version = 'v2.3'
    params['signType']=signType = '0'
    params['orderNo']=orderNo = order_no
    params['orderDatetime']=orderDatetime = order_datetime
    params['refundAmount']=refundAmount = int(refund_amount*100)
    params['mchtRefundOrderNo']=refund_order_no
    bufSignSrc = ""#//组签名原串

    if version != "":
        bufSignSrc = bufSignSrc+"version="+version+"&"
    if signType != "":
        bufSignSrc = bufSignSrc+"signType="+signType+"&"
    if merchantId != "":
        bufSignSrc = bufSignSrc+"merchantId="+merchantId+"&"
    if orderNo != "":
        bufSignSrc = bufSignSrc+"orderNo="+orderNo+"&"
    if refundAmount != "":
        bufSignSrc = bufSignSrc+"refundAmount="+str(refundAmount)+"&"
    if orderDatetime != "":
        bufSignSrc = bufSignSrc+"orderDatetime="+orderDatetime+"&"
    if key != "":
        bufSignSrc = bufSignSrc+"key="+key
    print bufSignSrc
    signMsg = build_md5_sign(bufSignSrc)
    params['signMsg']= signMsg.upper()
    return params


def notify_verify(params):
    md5key = settings.ALLINPAY_KEY      #测试商户的key! 请修改。
    merchantId=params["merchantId"]
    version=params['version']
    language=params['language']
    signType=params['signType']
    payType=params['payType']
    issuerId=params['issuerId']
    paymentOrderId=params['paymentOrderId']
    orderNo=params['orderNo']
    orderDatetime=params['orderDatetime']
    orderAmount=params['orderAmount']
    payDatetime=params['payDatetime']
    payAmount=params['payAmount']
    ext1=params['ext1']
    ext2=params['ext2']
    payResult=params['payResult']
    errorCode=params['errorCode']
    returnDatetime=params['returnDatetime']
    signMsg=params["signMsg"]

    bufSignSrc=""
    if merchantId != "":
        bufSignSrc=bufSignSrc+"merchantId="+merchantId+"&"
    if version != "":
        bufSignSrc=bufSignSrc+"version="+version+"&"
    if language != "":
        bufSignSrc=bufSignSrc+"language="+language+"&"
    if signType != "":
        bufSignSrc=bufSignSrc+"signType="+signType+"&"
    if payType != "":
        bufSignSrc=bufSignSrc+"payType="+payType+"&"
    if issuerId != "":
        bufSignSrc=bufSignSrc+"issuerId="+issuerId+"&"
    if paymentOrderId != "":
        bufSignSrc=bufSignSrc+"paymentOrderId="+paymentOrderId+"&"
    if orderNo != "":
        bufSignSrc=bufSignSrc+"orderNo="+orderNo+"&"
    if orderDatetime != "":
        bufSignSrc=bufSignSrc+"orderDatetime="+orderDatetime+"&"
    if orderAmount != "":
        bufSignSrc=bufSignSrc+"orderAmount="+orderAmount+"&"
    if payDatetime != "":
        bufSignSrc=bufSignSrc+"payDatetime="+payDatetime+"&"
    if payAmount != "":
        bufSignSrc=bufSignSrc+"payAmount="+payAmount+"&"
    if ext1 != "":
        bufSignSrc=bufSignSrc+"ext1="+ext1+"&"
    if ext2 != "":
        bufSignSrc=bufSignSrc+"ext2="+ext2+"&"
    if payResult != "":
        bufSignSrc=bufSignSrc+"payResult="+payResult+"&"
    if errorCode != "":
        bufSignSrc=bufSignSrc+"errorCode="+errorCode+"&"
    if returnDatetime != "":
        bufSignSrc=bufSignSrc+"returnDatetime="+returnDatetime
    # md5dddd =
    #signType 0 验签
    if signMsg==build_md5_sign(bufSignSrc+"&key="+md5key):
        if payResult =='1':
            return True,'支付成功'
        else:
            return False,'支付不成功'
    else:
        return False,'验签错误'


