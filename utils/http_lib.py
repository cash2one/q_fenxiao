#encoding:utf-8
__author__ = 'binpo'
import httplib
import logging
import urllib

def http_api(url,para,action,method="POST",json=None,accept="text/plain"):
    """
    url 调用的host
    para参数 以字典的形式
    action  调用的地址
    accept 参数接受的形式
    """
    conn = None
    try:
        params = urllib.urlencode(para)
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept":accept,'Authorization': 'Basic cm9vdEBkdWJibzpoZWxsMDVh'}
        conn = httplib.HTTPConnection(url)
        if json:
            conn.request(method,action,body=json,headers=headers)
        else:
            conn.request(method,action,params,headers=headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        print data
        return data
    except Exception,e:
        print e.message
    finally:
        if conn:
            conn.close()

# #data ={u'status': u'SUCCESS', u'remark': u'', u'totalRefundCount': u'0', u'serialNumber': u'c2aa8c10077e453db220f3cd6f319193', u'completeDateTime': u'2015-11-25 17:02:51', u'hmac': u'2ad6e6a98e77158229a50cf4ca72e97c', u'requestId': u'11144844184908', u'orderAmount': u'40500', u'orderCurrency': u'CNY', u'merchantId': u'120140267', u'totalRefundAmount': u'0'}
# data = {u"status":u"SUCCESS",u"remark":"",u"totalRefundCount":"0",u"serialNumber":u"a34a1072bad742e491be5049d29bdf2c",u"completeDateTime":u"2015-11-26 22:31:20",u"merchantId":u"120140267",u"requestId":u"51144854803074",u"orderAmount":u"37500",u"orderCurrency":u"CNY",u"hmac":u"d954fd199e9057204c80b850172a7c45",u"totalRefundAmount":u"0"}
# data1 = {u"status":u"SUCCESS",u"remark":"",u"totalRefundCount":"0",u"serialNumber":u"7b7708c3ac084e1d8fa612346ffcfa97",u"completeDateTime":u"2015-11-26 22:22:59",u"merchantId":u"120140267",u"requestId":u"51144854758733",u"orderAmount":u"37500",u"orderCurrency":u"CNY",u"hmac":u"10a6e4691ac756efbab5e2b8ac2743ae",u"totalRefundAmount":u"0"}
#
# import ujson
# jsondata=ujson.dumps(data)
# http_api('www.qqqg.com',{},'/order/ehking/payback/1/51144854803074.html',json=jsondata)
#
# jsondata=ujson.dumps(data1)
# http_api('www.qqqg.com',{},'/order/ehking/payback/1/51144854758733.html',json=jsondata)