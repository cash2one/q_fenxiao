#encoding:utf-8
__author__ = 'gaoaifei'

from search.whooshsearch import *
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import MySQLdb

# 创建索引
create_item_search_index()

try:
    conn=MySQLdb.connect(host="localhost",user="root",passwd="111111",db="haitao")
    cur=conn.cursor()
    cur.execute(' select show_id,category_id,title,summary from item_detail where deleted=0 and show_id!=0 ')
    results=cur.fetchall()
    cur.close()
    conn.close()
except MySQLdb.Error,e:
     print "Mysql Error %d: %s" % (e.args[0], e.args[1])

for res in results:
    add_item_search_index(res[0],res[1],res[2],'/',res[3])