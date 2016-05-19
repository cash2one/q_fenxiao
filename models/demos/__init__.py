__author__ = 'binpo'
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import create_engine, MetaData,ForeignKey

mysql_engine = create_engine('mysql://root:111111@192.168.88.67:3306/haitao?charset=utf8',encoding = "utf-8",echo =True)
Session = sessionmaker(bind=mysql_engine)
session = Session()
'INSERT INTO orders (gmt_created, gmt_modified, deleted, order_no, user_id, status, pay_status, delivery_status, ' \
'payable_amount, real_amount, discount_amount, transport_anmount, tax_amount, voucher, ' \
'pay_time, completion_time, user_remark, admin_remark, order_type, house_ware_name, recevie_address,' \
' recevie_address_id, is_asyn) VALUES ' \
'(now(), now(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
[{'user_id': None, 'order_no': None, 'completion_time': None, 'pay_time': None, 'delivery_status': None, 'recevie_address_id': None}]
