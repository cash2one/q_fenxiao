#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'gaoaifei'


from sqlalchemy import create_engine
ENGINE = "mysql://root@127.0.0.1:3306/fenxiao?charset=utf8"
eng = create_engine(ENGINE)
con = eng.connect()
aql = '''select count(id) from users;'''
rs = con.execute(aql)
print rs.fetchone()

con.close()



from utils.db_connection import DbConnection

db= DbConnection()
db.get_conn()
db.get_cur()
sql ='''
select count(u.id) as total from users  as u  join orders as o  on(u.id = o.user_id)
where o.deleted=0 and u.deleted=0 and o.status=1 and o.pay_status=1 and o.delivery_status=1;'''
db.cur.execute(sql)
# print dir(db.cur)
for r in db.cur.fetchall():
    print r