#encoding:utf-8
__author__ = 'binpo'
# from apps_api.yh_order_api import YhOrderApi
#
# from sqlalchemy import create_engine, MetaData,ForeignKey
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm.session import sessionmaker
# from models.orders_do import PayOrders
#
# mysql_engine = create_engine('mysql://root:111111@localhost:3306/haitao?charset=utf8',encoding = "utf-8",echo =True)
# Session = sessionmaker(bind=mysql_engine)
# session = Session()
# pay_order = session.query(PayOrders).first()
# from services.orders.orders_services import OrderServices
# order_service = OrderServices(rdb=session,db=session)
# items = order_service.query_item_by_order_id(order_id=pay_order.order_id)
# order = order_service.get_order_by_order_id(pay_order.order_id)
# order_api = YhOrderApi(session)
# order_api.create_order_params(pay_order,order,items)
# order_api.send_order_to_yh()
table_format = "ALTER TABLE `{0}` ENGINE=MyISAM, ROW_FORMAT=DEFAULT;"

f = open('tables','r')
content = f.readline()
while content:
    tablename = content.replace('|','').split()[0]
    print table_format.format(tablename)
    content = f.readline()


