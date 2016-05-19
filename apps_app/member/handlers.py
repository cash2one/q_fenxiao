#encoding:utf-8
__author__ = 'jinkuan'
from ..member import AppUserCenterHandler
from common.base_handler import AppBaseHandler
from services.orders.orders_services import OrderServices
from services.users.user_services import UserServices
from services.member.collection_service import MemberCollectionsServices
from services.locations.location_services import LocationServices
from models.location_do import *
from models.orders_do import Orders
from models.user_do import Users
import json

order_service = OrderServices()
user_service = UserServices()
collection_service = MemberCollectionsServices()
location_service = LocationServices()

class AppMemberCenterHandler(AppBaseHandler):

    def get(self, *args, **kwargs):
        '''
        todo:个人中心首页面
        :param args:
        :param kwargs:
        :return:
        '''
        user_id = self.get_current_user().get('id')
        phone = self.rdb.query(Users.phone).filter(Users.deleted==0,Users.id==user_id).scalar()
        order_service.set_rdb(self.rdb)
        tmp_query = order_service._list(user_id=user_id)
        waiting_pay = tmp_query.filter(Orders.status==1,Orders.pay_status==0).count()#待付款
        waiting_deliver = tmp_query.filter(Orders.pay_status==1,Orders.delivery_status==0).count()#待发货
        waiting_recieve = tmp_query.filter(Orders.pay_status==1,Orders.delivery_status==1).count()#待收货
        waiting_assess = tmp_query.filter(Orders.status==2,Orders.delivery_status==2).count()#待评价
        self.write_json({'stat':200,
                         'data':{'waiting_pay':waiting_pay,
                                 'waiting_deliver':waiting_deliver,
                                 'waiting_recieve':waiting_recieve,
                                 'waiting_assess':waiting_assess,
                                 'nick_name':phone[:3]+'****'+phone[7:]},
                         'info':''})

class AppMemberOrdersHandler(AppBaseHandler):

    def get(self, *args, **kwargs):
        '''
        todo:app个人中心订单
        :param args:
        :param kwargs:
        :return:
        '''
        user_id = self.get_current_user().get('id')
        order_service.set_rdb(self.rdb)
        status = self.get_argument('status','')
        query = order_service._list(user_id = user_id, state=status)
        data = self.get_page_data(query)
        tmp_query = order_service._list(user_id=user_id)
        waiting_pay = tmp_query.filter(Orders.status==1,Orders.pay_status==0).count()#待付款
        waiting_deliver = tmp_query.filter(Orders.pay_status==1,Orders.delivery_status==0).count()#待发货
        waiting_recieve = tmp_query.filter(Orders.pay_status==1,Orders.delivery_status==1).count()#待收货
        waiting_assess = tmp_query.filter(Orders.delivery_status==2,Orders.is_assess==False).count()#待评价
        page_url = self.get_page_url(self.get_argument('page',1))
        self.write_json({
                        'stat':200,
                        'info':'',
                        "data":{
                                "has_next":True and data.page_num - data.page > 0 or False,
                                "status":status,
                                "page_url":page_url,
                                "result":[{'id':d.id,
                                            'order_no':d.order_no,
                                            'gmt_created':d.gmt_created,
                                            'real_amount':d.real_amount, #实付金额
                                            'tax_amount':d.tax_amount,#税费
                                            'status':d.status,#订单状态 1:生成订单 2:完成订单 3:取消订单 4:作废订单
                                            'pay_status':d.pay_status,#支付状态 0:未付款 1: 已付款 2:申请退款 3: 已退款,
                                            'delivery_status':d.delivery_status,#配送状态 0:未发货 1: 已发货 2:已签收 3:申请退货 4:已退货
                                            'is_assess':d.is_assess,#是否已经评价
                                            'items':[{
                                                    'id':item.id,
                                                    'main_pic':item.main_pic,
                                                    'price':item.price,#销售价格
                                                    'title':item.title,#商品标题
                                                    'buy_nums':item.buy_nums,#购买数量
                                                    'total_price':item.item_price
                                                     }
                                                     for item in order_service.query_item_by_order_id(d.id)]
                                            }
                                           for d in data.result]
                                },
                        'waiting_pay':waiting_pay,
                        'waiting_deliver':waiting_deliver,
                        'waiting_recieve':waiting_recieve,
                        'waiting_assess':waiting_assess})

class AppMemberAddressHandler(AppBaseHandler):

    def get(self, *args, **kwargs):
        '''
        todo:收货地址操作
        :param args:
        :param kwargs:
        :return:
        '''
        user_id = self.get_current_user().get('id')
        user_service.set_rdb(self.rdb)
        addresses = user_service.get_address(user_id).all()
        self.write_json({'stat':200,
                         'addresses': [{
                                        'address_id':d.id,
                                        'name':d.name,
                                        'province':d.province,
                                        'province_code':d.province_code,
                                        'city':d.city,
                                        'city_code':d.city_code,
                                        'area':d.area,
                                        'area_code':d.area_code,
                                        'phone':d.phone,
                                        'address':d.address,
                                        'card_num':d.card_num,
                                        'is_default':d.is_default}
                                       for d in addresses],
                         'info':''
                        })

    def post(self, *args, **kwargs):
        '''
        todo:
        :param args:
        :param kwargs:
        :return:
        '''
        operation = self.get_argument('operation',None)
        user_id = self.get_current_user().get('id')
        if operation == 'default':
            address_id = self.get_argument('address_id')
            user_service.set_db(self.db)
            user_service.set_default_address(address_id,user_id)
            self.write_json({'stat':200,'info':'设置成功'})
        elif operation == 'add':
            self.get_paras_dict()
            user_service.set_db(self.db)
            user_id = self.get_current_user().get('id')
            address_id = self.get_argument('address_id',None)
            province_code=self.qdict.get('province_code')
            city_name=self.qdict.get('city_name').strip()
            area_name=self.qdict.get('area_name').strip()
            province_id = self.rdb.query(Province.id).filter(Province.deleted==0,Province.yh_code==province_code).scalar()
            if not province_id:
                return self.write_json({'stat':201,'info':'请重新选择省，目前该地址不支持配送该省'})
            city_id = self.rdb.query(City.id).filter(City.deleted==0,City.father==province_id,City.name.like('%'+city_name+'%')).scalar()
            if not city_id:
                return self.write_json({'stat':201,'info':'请重新选择市，目前该地址不支持配送该市'})
            area_id = self.rdb.query(Area.id).filter(Area.deleted==0,Area.father==city_id,Area.name.like('%'+area_name+'%')).scalar()
            if not area_id:
                return self.write_json({'stat':201,'info':'请重新选择区，目前该地址不支持配送该区'})
            user_address = user_service.add_recieve_address(user_id,
                                                            name=''.join(self.qdict.get('name').split()),
                                                            card_num=self.qdict.get('card_num').upper(),
                                                            phone=self.qdict.get('phone').strip(),
                                                            province=province_id,
                                                            city=city_id,
                                                            area=area_id,
                                                            address=self.qdict.get('address').strip(),
                                                            address_id=address_id)
            self.write_json({'stat':200,'info':'添加成功','data':user_address.id})

        elif operation == 'delete':
            address_id = self.get_argument('address_id')
            user_id = self.get_current_user().get('id')
            user_service.set_db(self.db)
            user_service.delete_address(address_id,user_id)
            self.write_json({'stat':200,'info':'删除成功'})

from models.express_do import InvoiceOrders
from utils.kuaidi import kuaidi_query,kuaidi_query_2
import ujson
from data_cache.express_company_cache import ExpressCompanyCache

# 查看物流信息
class AppOrderExpressCheck(AppBaseHandler):

    def get(self, *args, **kwargs):
        self.echo('h5/order/track.html')

    def post(self,order_no, *args, **kwargs):
        user_id = self.get_current_user().get('id')
        invoice_order = self.db.query(InvoiceOrders).\
            filter(InvoiceOrders.deleted==0,InvoiceOrders.order_no==order_no,InvoiceOrders.user_id==user_id).scalar()
        content = ''
        data={'state':200,'data':[]}
        company = ExpressCompanyCache().get_express_company_info(invoice_order.express_company_id)
        if invoice_order and invoice_order.status==2 and invoice_order.express_content:
            content = invoice_order.express_content
            data['data'] = ujson.loads(content)
            data['WaybillNumber']=invoice_order.express_no
            data['company_name']=company.get('name')
        else:
            content = kuaidi_query_2(company.get('code'),invoice_order.express_no)
            express_data = ujson.loads(content)
            express_content = express_data.get('data')
            status = express_data.get('status')
            if status==1:
                data['WaybillNumber'] = invoice_order.express_no
                data['company_name'] = company.get('name')
                data['data'] = '暂时没有物流信息'
                data['status'] = 201
            else:
                if status==4:
                    invoice_order.express_content = ujson.dumps(express_content)
                    invoice_order.status=2
                    self.db.add(invoice_order)
                    self.db.commit()
                data['data']=express_content
                data['WaybillNumber']=invoice_order.express_no
                data['company_name']=company.get('name')
        self.write_json(data)
