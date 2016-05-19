#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'gaoaifei'


from common.base_handler import AdminBaseHandler
from services.users.user_services import UserServices
from services.orders.orders_services import OrderServices
user_service = UserServices()
order_service = OrderServices()

class MemberReport(AdminBaseHandler):
    def get(self):
        '''
        会员报表统计
        :return:
        '''
        user_service.set_rdb(self.rdb)
        #会员总数
        member_total = user_service.get_users_total_count()
        user_service.set_db(self.db)
        #有订单的会员数
        member_order_count = user_service.get_member_order_count()
        member_order_count = member_order_count.scalar()
        #会员订单总数
        order_service.set_rdb(self.rdb)
        order_count = order_service.get_order_total_count()
        #  会员购买率 （会员购买率 = 有订单会员数 ÷ 会员总数）
        purchase_rate = float(float(member_order_count)/float(member_total))
        # 会员购物总额
        total_amount = order_service.get_order_total_amount()
        # 每会员订单数 = 会员订单总数 ÷ 会员总数
        order_purchase_rate = float(float(order_count)/float(member_total))
        # 每会员购物额 = 会员购物总额 ÷ 会员总数
        amount_purchase_rate = float(float(total_amount)/float(member_total))
        self.echo('admin/reports/member_report.html',{ 'member_total':member_total,
                                                       "member_order_count":member_order_count,
                                                       'order_count':order_count,
                                                       'purchase_rate':purchase_rate,
                                                       'total_amount':total_amount,
                                                       'order_purchase_rate':order_purchase_rate,
                                                       'amount_purchase_rate':amount_purchase_rate})