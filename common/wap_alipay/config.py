#-*- coding:utf-8 -*-
# from Crypto.PublicKey import RSA
class settings:
    # 安全检验码，以数字和字母组成的32位字符
    ALIPAY_KEY = 'cqgnenntxoeh5qrxlgm1s4zs6n0k9ai3'

    LOGGING_PAYMENT = 'payment.log'

	#字符编码格式 目前支持 gbk 或 utf-8
    ALIPAY_INPUT_CHARSET = 'utf-8'

    # 合作身份者ID，以2088开头的16位纯数字
    ALIPAY_PARTNER = '2088811040118677'

    # 签约支付宝账号或卖家支付宝帐户
    ALIPAY_SELLER_EMAIL = 'zhifu@zenmez.com'

    # 付完款后跳转的页面（同步通知） 要用 http://格式的完整路径，不允许加?id=123这类自定义参数    点击跳转
    ALIPAY_RETURN_URL='http://192.168.88.224:8010/orders/pay/payback/'

    # 交易过程中服务器异步通知的页面 要用 http://格式的完整路径，不允许加?id=123这类自定义参数    后台自动调用
    ALIPAY_NOTIFY_URL='http://192.168.88.224:8010/orders/pay/payback/'

    ALIPAY_SHOW_URL=''

    # 访问模式,根据自己的服务器是否支持ssl访问，若支持请选择https；若不支持请选择http
    ALIPAY_TRANSPORT='https'

    ALI_PUBLIC_KEY  = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCnxj/9qwVfgoUh/y2W89L6BkRAFljhNhgPdyPuBV64bfQNN1PjbCzkIM6qRdKBoLPXmKKMiFYnkd6rAoprih3/PrQEB/VsW8OoM8fxn67UDYuyBTqA23MML9q1+ilIZwBC2AQ2UBVOrFXfFl75p6/B5KsiNG9zpgmLCUYuLkxpLQIDAQAB"
    ALIPAY_SIGN_TYPE = "RSA"

    LOGGING_ERROR_PAYMENT = 'payment_error.log'