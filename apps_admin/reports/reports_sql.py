#encoding:utf-8
__author__ = 'binpo'

#当日
daily_orders_reports_sql='select count(*),DATE_FORMAT(gmt_created,"%k") as h from orders where pay_status=1 and gmt_created between "{0}" and "{1}" group by h'


daily_pay_reports_sql = 'select sum(amount) as c ,DATE_FORMAT(gmt_created,"%k") as h from pay_orders where pay_status=1 and gmt_created between "{0}" and "{1}" group by h'


#当月
month_orders_reports_sql='select count(*),DATE_FORMAT(gmt_created,"%Y-%m-%d") as d from orders where pay_status=1 and gmt_created between "{0}" and "{1}" group by d'

month_pay_reports_sql = 'select sum(amount),DATE_FORMAT(gmt_created,"%Y-%m-%d") as d from pay_orders where pay_status=1 and gmt_created between "{0}" and "{1}" group by d'

