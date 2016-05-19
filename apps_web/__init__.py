#encoding:utf-8
__author__ = 'binpo'

from tornado.web import url
from apps_web.demo import *
from home import HomeHandler,HealthCheckHandler,TmsHandler
handlers=[]
handlers=[
     url(r"/",HomeHandler, name="home_handler"),
     url(r"/index.html",HomeHandler, name="home_handler"),
     url(r"/index.php",HomeHandler, name="home_handler"),
     url(r"/json", JsonHandler, name="json_handler"),
#     url(r"/asyn", AsynHandler, name="asyn_handler"),
#     url(r"/avanta",AvatarHandlerSample, name="avata_handler"),
#
#
#
]

from items.urls import _handlers
handlers.extend(_handlers)

from reg.urls import _handlers
handlers.extend(_handlers)

from member.urls import _handlers
handlers.extend(_handlers)

from orders.urls import _handlers
handlers.extend(_handlers)

#通联支付
from payment.urls import _handlers
handlers.extend(_handlers)

#易汇金
from payment.urls import _handlers as ehking_handlers
handlers.extend(ehking_handlers)

from help.urls import _handlers
handlers.extend(_handlers)

from fileupload.url import _handlers
handlers.extend(_handlers)

# from whooshsearch.urls import _handlers
# handlers.extend(_handlers)

handlers.append(url(r"/ok.html",HealthCheckHandler, name="health_handler"),)#健康检查
handlers.append(url(r"/([\w\W]*)",TmsHandler, name="all_handler"),)