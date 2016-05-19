#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'gaoaifei'


from common.base_handler import AdminBaseHandler
from services.orders.orders_services import OrderServices
from services.item.item_services import ItemService
order_service = OrderServices()
item_service = ItemService()


class SalesReport(AdminBaseHandler):
    def get(self, *args, **kwargs):
        order_service.set_rdb(self.rdb)
        query = order_service.get_item_orders_list()
        # data = self.get_page_data(query)
        self.echo('admin/reports/sales_reports.html',{
            'data':query
        })

    def get_item_detail_by_item_id(self,item_id, name):
        item_service.set_rdb(self.rdb)
        item = item_service.get_itemDetail_by_id(item_id)
        if name=='name':
            return item.title
        else:
            return item.type
