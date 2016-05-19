#encoding:utf-8
__author__ = 'binpo'
def fahuo():
    data = {"token":"p9boLc9NygNU/8mc+7JhJA==","data":[{"express_company_code":"yuantong","express_no":"801635822496","order_no":"19144427469922"}]}
    import ujson

    # return data
    import requests
    json_data = {"data":ujson.dumps(data)}
    r = requests.post("http://www.qqqg.com/api/batch_express",data=json_data)
    result = r.content
    print result


from common.allinpay.allinpay import create_pay_info,notify_verify,settings
from services.payments.payorder_services import PayOrderService
from services.orders.orders_services import OrderServices
import logging
from apps_api.yh_order_api import YhOrderApi
from services.express.express_services import ExpressServices

from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker


mysql_engine = create_engine('mysql://root:111111@localhost:3306/haitao?charset=utf8',encoding = "utf-8",echo =True)

Session = sessionmaker(bind=mysql_engine)
session = Session()

logger =logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.FileHandler(settings.LOGGING_PAYMENT))

payorder_service = PayOrderService()
order_service = OrderServices()

def qingguan():

    order_id=100
    payorder_service.set_rdb(session)
    pay_order = payorder_service.get_payorder_by_order_no('19144437190866')
    order_id = pay_order.order_id
    try:
        order_service.set_rdb(session)
        express_service = ExpressServices(db=session)
        items = order_service.query_item_by_order_id(order_id=order_id)
        order = order_service.get_order_by_order_id(order_id)
        express_service._add(order)
    except Exception,e:
        print e.message
    try:
        yh_order_obj = YhOrderApi(session)
        yh_order_obj.create_order_params(pay_order,order,items)
        yh_order_obj.start()
    except:
        pass

qingguan()