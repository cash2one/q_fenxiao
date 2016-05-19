#encoding:utf-8
__author__ = 'binpo'

import urllib
try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse
try:
    import urllib.parse as urllib_parse
except ImportError:
    import urllib as urllib_parse


def get_oauth_user_info(request_url,**kwargs):
    """
    :todo 获取第三方登录的用户信心
    :param 获取路径
    :kwargs 请求参数
    """
    user_url = request_url+'?'+urllib_parse.urlencode(kwargs)
    response = urllib.urlopen(user_url)
    return  response.read()
