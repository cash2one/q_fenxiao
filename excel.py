#encoding:utf-8
__author__ = 'wangjinkuan'

from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from services.orders.orders_services import OrderServices
import xlwt,xlrd,os
from models.orders_do import Orders

order_service = OrderServices()

mysql_engine = create_engine('mysql://root:sunwang@localhost:3306/haitao?charset=utf8',encoding = "utf-8",echo =True)

Session = sessionmaker(bind=mysql_engine)
session = Session()

def build_excel():
    data = xlrd.open_workbook(os.path.dirname(__file__)+'/order_1208.xls')
    table = data.sheets()[0]
    order_nos = {}
    for rownum in range(1,table.nrows):
        order_nos[table.cell_value(rowx=rownum, colx=2)] = table.cell_value(rowx=rownum, colx=10)
    order_service.set_rdb(session)
    query = order_service.get_orderItems_info()
    query = query.filter(Orders.order_no.in_(order_nos))
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('sales',cell_overwrite_ok=True)
    try:
        ws.write(0,0,u'日期')
        ws.write(0,1,u'订单号')
        ws.write(0,2,u'商品序号')
        ws.write(0,3,u'商品名称')
        ws.write(0,4,u'商品单价')
        ws.write(0,5,u'数量')
        ws.write(0,6,u'商品总价')
        ws.write(0,7,u'扣款金额')
        index = 1
        current_order_id,pre_order_id=None,None
        item_no,item_name,buy_nums,item_price,item_total_price,total_price = None,None,None,None,None,None
        for data in query:
            current_order_id=data.order_id
            if current_order_id==pre_order_id:
                item_no = item_no+";"+str(data.item_no)
                item_name = item_name+";"+data.name
                buy_nums = str(buy_nums)+";"+str(data.buy_nums)
                item_price = str(item_price)+";"+str(data.item_price)
                item_total_price = str(item_total_price)+";"+str(data.total_amount)
                ws.write(index-1,2,item_no)
                ws.write(index-1,3,item_name)
                ws.write(index-1,4,item_price)
                ws.write(index-1,5,buy_nums)
                ws.write(index-1,6,item_total_price)
            else:
                ws.write(index,0,data.gmt_created.strftime("%Y-%m-%d %H:%M:%S"))
                ws.write(index,1,data.order_no)
                ws.write(index,2,data.item_no)
                ws.write(index,3,data.name)
                ws.write(index,4,data.item_price)
                ws.write(index,5,data.buy_nums)
                ws.write(index,6,data.total_amount)
                ws.write(index,7,order_nos[data.order_no])
                #记录数据
                item_no = data.item_no
                item_name = data.name
                buy_nums = data.buy_nums
                item_price = data.item_price
                item_total_price = data.total_amount
                index += 1
            pre_order_id=current_order_id
        wb.save('sales.xls')
    except Exception,e:
        print e

build_excel()