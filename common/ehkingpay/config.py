#encoding:utf-8
__author__ = 'gaoaifei'

class settings:
  # 安全检验码
  EHKINGPAY_KEY = 'Raychina88'

  LOGGING_PAYMENT = 'EHKINGpay_payment.log'

  LOGGING_ERROR_PAYMENT = 'payment_error.log'

  EHKING_INPUT_CHARSET = 'utf-8'

  # 合作身份者ID及key
  EHKING_MERCHANT_ID = '120140267'
  EHKING_MERCHANT_KEY = 'ceb5b4155eee48cda71668bfe7f384f6'

  EHKING_SIGN_TYPE = 'MD5'

  # 付完款后跳转的页面（同步通知） 要用 http://格式的完整路径，不允许加?id=123这类自定义参数    点击跳转
  EHKING_RETURN_URL='http://127.0.0.1:8010/orders/pay/payback/'

  # 交易过程中服务器异步通知的页面 要用 http://格式的完整路径，不允许加?id=123这类自定义参数    后台自动调用
  EHKING_NOTIFY_URL='http://127.0.0.1:8010/orders/pay/payback/'

  EHKING_SHOW_URL=''

  # 访问模式,根据自己的服务器是否支持ssl访问，若支持请选择https；若不支持请选择http
  EHKING_TRANSPORT='https'
