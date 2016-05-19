#encoding:utf-8
__author__ = 'binpo'

from tornado.web import url
from apps_admin.home import AdminHandler,IndexHandler
from apps_admin.item.urls import _handlers as item_handlers
from apps_admin.order.urls import _handlers as order_handlers
from login import *

handlers = [
    url(r'/', IndexHandler,name='site_index_html'),
    url(r'/admin/index', AdminHandler,name='index_html'),
    url(r'/admin/login', LoginHandler,name='login'),
    url(r'/admin/logout', LoginOutHandler,name='login_out'),

]

handlers.extend(item_handlers)
handlers.extend(order_handlers)

from permission.url import _handlers
handlers.extend(_handlers)

from account.url import _handlers
handlers.extend(_handlers)

from fileupload.url import _handlers
handlers.extend(_handlers)

from logs.urls import _handlers
handlers.extend(_handlers)

from api_tasks.url import _handlers
handlers.extend(_handlers)

from apps_admin.payment.urls import _handlers as payment_handler
handlers.extend(payment_handler)

from apps_admin.system.urls import handlers as sys_temhandlers
handlers.extend(sys_temhandlers)

from apps_admin.users.urls import _handlers as user_handlers
handlers.extend(user_handlers)

from apps_admin.item.urls import _handlers as brand_handler
handlers.extend(brand_handler)

from apps_admin.sites.urls import _handlers as site_handler
handlers.extend(site_handler)

from apps_admin.comment.urls import _handlers as comment_handler
handlers.extend(comment_handler)

from apps_admin.advertising.urls import _handlers as ad_handler
handlers.extend(ad_handler)

from apps_admin.coupon.urls import _handlers as cp_handler
handlers.extend(cp_handler)

from apps_admin.attributes.urls import _handlers as attributes_handlers
handlers.extend(attributes_handlers)

from apps_admin.employee.urls import _handlers as employee_handlers
handlers.extend(employee_handlers)

#报表
from apps_admin.reports.url import _handlers as reports_handlers
handlers.extend(reports_handlers)

# 会员统计
from apps_admin.reports.url import _handlers as member_handlers
handlers.extend(member_handlers)

#销售排行统计
from apps_admin.reports.url import _handlers as sales_handlers
handlers.extend(sales_handlers)

#分销商排行统计
from apps_admin.reports.url import _handlers as drp_handlers
handlers.extend(drp_handlers)

#运单列表
from apps_admin.express.urls import _handlers
handlers.extend(_handlers)

#分销商
from apps_admin.distributor.urls import _handlers
handlers.extend(_handlers)

#佣金结算
from apps_admin.comm.urls import _handlers
handlers.extend(_handlers)




#
# handlers.append(url(r'/([\w\W]*).html', TmsHandler,name='tms'))
# handlers.append(url(r'/([\w\W]*)', HomeHandler,name='home'))