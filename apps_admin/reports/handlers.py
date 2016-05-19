#encoding:utf-8
__author__ = 'binpo'

from common.base_handler import AdminBaseHandler
from reports_sql import *
from utils.datetime_util import datetime_format

class DailyReports(AdminBaseHandler):
    def get(self):
        start,end = datetime_format(format='%Y-%m-%d'),datetime_format(format='%Y-%m-%d %H:%M:%S')
        start,end = '2015-09-29','2016-01-07'
        # print daily_orders_reports_sql.format(start,end)
        orders = self.db.execute(daily_orders_reports_sql.format(start,end))
        # print [{"date":str(o[1])} for o in orders]
        reports = str([{"date":str(o[1]),"value":int(o[0])} for o in orders])
        pays = self.db.execute(month_orders_reports_sql.format(start,end))
        self.echo('admin/reports/month_reports.html',{'orders':orders,"pays":pays,'reports':reports})


import datetime

class MonthReports(AdminBaseHandler):
    def get(self, *args, **kwargs):
        start,end = datetime_format(format='%Y-%m-%d',input_time=datetime.datetime.now()+datetime.timedelta(days=-31)),\
                    datetime_format(format='%Y-%m-%d %H:%M:%S')

        orders = self.db.execute(month_orders_reports_sql.format(start,end))
        # for order in orders:
        #     print order[1]
        reports = str([{"date":str(o[1]),"value":int(o[0])} for o in orders])
        #     print o
        # print  month_pay_reports_sql.format(start,end)

        pays = self.db.execute(month_pay_reports_sql.format(start,end))
        # for p in pays:
        #     print p
        self.echo('admin/reports/month_reports.html',{'orders':orders,"pays":pays,'reports':reports})


