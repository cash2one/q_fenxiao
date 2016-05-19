#encoding:utf-8
__author__ = 'binpo'

from image_validate_code import ImageHandler
from common.weibo_oauth.weibo_handler import *
from common.qq_oauth.qq_handler import *
from msg_handler import *
from tornado.web import url
from errors import *
from location_handler import LocationHandler,AdminLocationHandler
from card_check import CardCheckHandler
from common.weixin_oauth.weixin_handler import WeixinLoginHandler,WeixinloginHandlerCallback
from mweixin_oauth.m_weixin_handler import MWeixinLoginHandler

handlers = [

    ('/common/image_code/',ImageHandler),#图片验证码
    ('/common/msg/send/',MsgSendHandler),#手机消息
    ('/common/check_id_card/',CardCheckHandler),#身份证号码验证

    url('/common/location.html',LocationHandler,name='location'),#手机消息
    url('/common/admin/locations',AdminLocationHandler,name='admin_locations'),

    url('/common/phone/code/',PhoneCodeHandler,name='phone_validate_code'),#手机验证码

    ('/oauth/sinaweibo', WeiboLoginHandler),
    ('/oauth/sinaweibo/callback', WeiboLoginHandlerCallback),

    ('/oauth/wx/', WeixinLoginHandler),
    ('/m_oauth/m_wx/', MWeixinLoginHandler),

    ('/oauth/wx/callback',WeixinloginHandlerCallback),
    ('/oauth/qq', QQLoginHandler),
    ('/oauth/qq/callback',QQloginHandlerCallback),
    (r'/404', NotFoundHandler),
    (r'/500', InternalErrorHandler),

]
