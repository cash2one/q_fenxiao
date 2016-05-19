__author__ = 'gaoaifei'

import requests

data = {"returnDatetime":"20151229105107","signMsg":"A793A008D3F5DB7B66B6FE8A9EDD4945","ext1":"","orderAmount":"48800","issuerId":"","signType":"0","payType":"0","errorCode":"","language":"1","orderDatetime":"20151229104946","version":"v1.0","payResult":"1","payDatetime":"20151229105107","paymentOrderId":"201512291050038325","orderNo":"148145135738638","payAmount":"48800","merchantId":"109020201511072","ext2":""}

url = 'http://www.qqqg.com/order/allinpay/payback/12/1212.html'
req = requests.post((url),data=data,timeout=3 , verify=False)
req.read()