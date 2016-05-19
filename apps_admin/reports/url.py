#encoding:utf-8
__author__ = 'binpo'

from tornado.web import url
from handlers import *

_handlers = [
    url(r'/admin/reports/one_day_reports',DailyReports,name='daily_reports'),
    url(r'/admin/reports/one_month_reports',MonthReports,name='month_reports'),
]

from  member_handlers import *
_handlers.extend([
    url(r'/admin/reports/member_report',MemberReport,name='member_report'),
])

from  sales_handlers import *
_handlers.extend([
    url(r'/admin/reports/sales_report',SalesReport,name='sales_report'),
])



from  drp_handlers import *
_handlers.extend([
    url(r'/admin/reports/drp_report',DrpReport,name='drp_report'),
])