#encoding:utf-8
__author__ = 'gaoaifei'

import types
import hmac,hashlib
import requests
from urllib import urlencode, urlopen
import ujson
import json
from utils.md5_util import hmac_md5,hmac_md5_php
from collections import OrderedDict

from common.ehkingpay.config import settings
from decimal import *

#即时到账交易接口
def create_pay_info(order_no, total_fee, name,card_type,card_num,productDetail,callbackUrl=None, notify_url=None):
    '''
    支付所需参数
    :param order_no: 订单号
    :param total_fee: 订单金额
    :param callbackUrl: 回调处理url
    :param notify_url: 服务器通知url
    :return:
    '''
    #拼接认证串
    # sign_str = settings.EHKING_MERCHANT_ID + str(int(round(total_fee*100))) + str(order_no) + 'CNY' + notify_url + callbackUrl
    #sign_str = settings.EHKING_MERCHANT_ID + str(int(round(total_fee*100)))  + 'CNY' + str(order_no) + notify_url + callbackUrl
    #hmac = hmac_md5_php(settings.EHKING_MERCHANT_KEY,sign_str)
    
    hmacSource = ""
    hmacSource+= settings.EHKING_MERCHANT_ID
    hmacSource+= str(int(round(total_fee*100)))
    hmacSource+= 'CNY'
    hmacSource+= str(order_no)
    hmacSource+= notify_url
    hmacSource+= callbackUrl
    hmacSource+= ''
    hmacSource+= ''
    for item in productDetail:
        hmacSource+=item.get('name')
        hmacSource+=str(item.get('quantity'))
        hmacSource+=str(item.get('amount'))
        hmacSource+=''
        hmacSource+=''
    hmacSource+= name
    hmacSource+= ''
    hmacSource+= card_num
    hmacSource+= ''
    hmacSource+= ''

    hmacSource+= 'CUSTOMS'
    hmacSource+= 'GOODSTRADE'
    hmacSource+= ''
    hmacSource+= ''
    hmac = hmac_md5_php(settings.EHKING_MERCHANT_KEY,hmacSource)

    enterparams = {
        "merchantId":settings.EHKING_MERCHANT_ID,#商户key
        "orderAmount":int(round(total_fee*100)),##订单金额 单位:分，1元=100分
        "orderCurrency":'CNY',#默认CNY（人民币）
        "requestId":order_no,
        "notifyUrl":notify_url,#服务器通知：支付成功后会向该地址发送两次成功通知，该地址可以带参数，如: “www.ehking.com/callback.action?test=test”. 注意：如不填notifyUrl的参数值支付成功后您的服务器将得不到支付成功的通知。
        "callbackUrl":callbackUrl,#页面回调：支付成功后会向该地址发送两次成功通知，该地址可以带参数，如: “www.ehking.com/callback.action?test=test”. 注意：如不填callbackUrl的参数值支付成功后您的浏览器页面将得不到支付成功的通知。
        "remark":'',
        "paymentModeCode":'',#支付方式编码
        "productDetails":productDetail,#商品信息 name quantity amount不能为空
        "payer": {
            "name":name,#必填
            "phoneNum": "",
            "idNum":card_num,#必填 身份证号
            "bankCardNum":"",
            "Email":""
        },#申报信息
        "cashierVersion":'CUSTOMS',
        "forUse":'GOODSTRADE',
        "merchantUserId":'',
        'bindCardId':'',
        'hmac':hmac
    }
    jsonstr = ujson.dumps(enterparams)
    headers = {'content-type':'application/vnd.ehking-v1.0+json'}
    resp = requests.post("https://api.ehking.com/onlinePay/order",data = jsonstr, headers = headers)
    # print resp.text
    result = ujson.loads(resp.content)
    # print result
    if result['status']=='REDIRECT':
        return result
    else:
        return False

def checkHmac(data):
    '''
    验证hmac是否有效
    :param data: 数据字典
    :return:
    '''
    hmacSource = ''
    hmacSource += data.get("merchantId")
    hmacSource += data["requestId"]
    hmacSource += data["serialNumber"]
    hmacSource += data["totalRefundCount"]
    hmacSource += data["totalRefundAmount"]
    hmacSource += data["orderCurrency"]
    hmacSource += data["orderAmount"]
    hmacSource += data["status"]
    hmacSource += data["completeDateTime"]
    hmacSource += data["remark"]
    hmac = hmac_md5_php(settings.EHKING_MERCHANT_KEY, hmacSource)
    if hmac==data['hmac']:
        if data['status']=='SUCCESS':
            return True,'支付成功'
        elif data['status'] == 'FAILED' or data['status'] == 'CANCEL':
            return False,'支付失败'
        elif data['status'] == 'INIT':
            return False,'用户在支付页未付款'
        else:
            return False,'Unknow error'
    else:
        return False,'验签错误'