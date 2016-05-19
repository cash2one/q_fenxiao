#encoding:utf-8
__author__ = 'jinkuan'

from apps_mobile.common_handler import CommonHandler
from common.base_handler import MobileBaseHandler
from services.orders.orders_services import OrderServices
from services.users.user_services import UserServices
from services.member.collection_service import MemberCollectionsServices
from models.orders_do import Orders
import sys
import datetime
import json
from data_cache.express_company_cache import ExpressCompanyCache
order_service = OrderServices()
user_service = UserServices()
collection_service = MemberCollectionsServices()

class AddressHandler(CommonHandler):

    def get(self, *args, **kwargs):
        '''
        地址列表
        :param args:
        :param kwargs:
        :return:
        '''
        user_id = self.get_current_user().get('id')
        user_service.set_rdb(self.rdb)
        addresses = user_service.get_address(user_id).all()
        self.write_json({'state':200,'msg':'ok',
                         'parent_category_id':'',
                         'menu':3,
                         'addresses': [{key:getattr(d,key) for key in d.columns()} for d in addresses]})

    def post(self, *args, **kwargs):
        pass

class MemberOrdersHandler(CommonHandler):
    def get(self, *args, **kwargs):
        self.echo('mobile/order/orders.html')

    def post(self, *args, **kwargs):
        '''
        :param args:
        :param kwargs:
        :return:
        '''
        user_id = self.get_current_user().get('id')
        order_service.set_rdb(self.rdb)
        status = self.get_argument('state','')
        query = order_service._list(user_id = user_id, state=status)
        data = self.get_page_data(query)
        tmp_query = order_service._list(user_id=user_id)
        #tmp_query = order_service.query_orders(user_id = user_id)
        waiting_pay = tmp_query.filter(Orders.status==1,Orders.pay_status==0).count()#待付款
        waiting_deliver = tmp_query.filter(Orders.pay_status==1,Orders.delivery_status==0).count()#待发货
        waiting_recieve = tmp_query.filter(Orders.pay_status==1,Orders.delivery_status==1).count()#待收货
        waiting_assess = tmp_query.filter(Orders.delivery_status==2,Orders.is_assess==False).count()#待评价
        page_url = self.get_page_url(self.get_argument('page',1))
        try:
            self.write_json({
                        'state':200,
                        'msg':'success',
                        'parent_category_id':'',
                        "data":{ "page_num":data.page_num,
                                 "page_size":data.page_size,
                                 "page":data.page,
                                 "page_start":data.page_start,
                                 "page_end":data.page_end,
                                 "result":[{'id':d.id,
                                            'order_no':d.order_no,
                                            'gmt_created':d.gmt_created,#(d.gmt_created).strptime("%Y-%m-%d %H:%M:%S"),
                                            'real_amount':d.real_amount, #实付金额
                                            'tax_amount':0,#税费
                                            'status':d.status,#订单状态 1:生成订单 2:完成订单 3:取消订单 4:作废订单
                                            'pay_status':d.pay_status,#支付状态 0:未付款 1: 已付款 2:申请退款 3: 已退款,
                                            'delivery_status':d.delivery_status,#配送状态 0:未发货 1: 已发货 2:已签收 3:申请退货 4:已退货
                                            'house_ware_name':'',
                                            'recevie_address':json.loads(d.recevie_address),
                                            'is_assess':d.is_assess,#是否已经评价
                                            'items':[{
                                                            'id':item.id,
                                                            'main_pic':item.main_pic,
                                                            'price':item.price,#销售价格
                                                            'orgin_price':item.orgin_price,#原价
                                                            'inner_price':item.inner_price,#国内参考价格
                                                            'title':item.title,#商品标题
                                                            'buy_nums':item.buy_nums,#购买数量
                                                            'top_category_id':item.top_category_id,
                                                            'item_price':item.item_price,#商品单价
                                                            'total_amount':item.total_amount,#商品总金额 这个商品
                                                            'item_no':item.item_no,#商品序号 和仓库保存一致,录入的时候人工录入
                                                            'name':item.name,#商品名称
                                                            'brand':item.brand,#品牌名称
                                                            'amount':item.amount#eg:一箱方便面,6袋  子包装单位和个数
                                                     }
                                                     for item in order_service.query_item_by_order_id(d.id)]
                                            }
                                           for d in data.result]
                                 },
                        'waiting_pay':waiting_pay,
                        'waiting_deliver':waiting_deliver,
                        'waiting_recieve':waiting_recieve,
                        'waiting_assess':waiting_assess,
                        'status':status,
                        'page_url':page_url,
                        'menu':1})
        except Exception,e:
            self.write_json({'stat':400,'info':e.message})


class MemberOrderDetailHandler(CommonHandler):

    def get(self, order_no, *args, **kwargs):
        '''
        查看订单详情页
        :param order_id: 订单id
        '''
        user_id = self.get_current_user().get('id')
        order_service.set_rdb(self.rdb)
        order = order_service.get_order_no(order_no,user_id)
        items = order_service.query_item_by_order_no(order_no = order_no)
        is_bussiness = self.get_current_user().get('is_bussiness')
        data = {'order':order,'items':items,'is_bussiness':is_bussiness}
        self.echo('mobile/order/order_detail.html',data)


class MemberAddressHandler(CommonHandler):
    '''
    设置默认收货地址
    '''
    def get(self, *args, **kwargs):
        try:
            address_id = self.get_argument('address_id')
            operatioin = self.get_argument('operation',None)
            user_id = self.get_current_user().get('id')
            user_service.set_db(self.db)
            if operatioin=='query':
                user_service.set_rdb(self.rdb)
                address = user_service.get_address_by_id(user_id,address_id)
                self.write(address.addressed())
            else:
                user_service.set_default_address(address_id,user_id)
                self.write_json({'state':200,'info':'设置成功'})
        except Exception,e:
            self.captureException(sys.exc_info())
            self.write_json({'state':400,'info':e.message})

    def post(self, *args, **kwargs):
        '''
        添加／编辑收货地址
        :param args:
        :param kwargs:
        :return:
        '''
        try:
            self.get_paras_dict()
            user_service.set_db(self.db)
            user_id = self.get_current_user().get('id')
            '''
                name=self.qdict.get('name'),
                card_num=self.qdict.get('card_num'),
                phone=self.qdict.get('phone'),
                province=self.qdict.get('province'),
                city=self.qdict.get('city'),
                area=self.qdict.get('area'),
                address=self.qdict.get('address'))
            '''
            address_id = self.get_argument('address_id',None)
            card_num = self.qdict.get('card_num')
            user_address = user_service.add_recieve_address(
                user_id,
                name=''.join(self.qdict.get('name').split()),
                card_num= card_num and card_num.upper() or '' ,
                phone=self.qdict.get('phone').strip(),
                province=self.qdict.get('province').strip(),
                city=self.qdict.get('city'),
                area=self.qdict.get('area'),
                address=self.qdict.get('address').strip(),
                address_id=address_id)
            self.write_json({'state':200,'info':'成功','addressId':user_address.id})
        except Exception,e:
            self.captureException(sys.exc_info())
            self.write_json({'state':400,'info':e.message,'addressId':''})

    def delete(self, *args, **kwargs):
        '''
        删除地址
        :param args:
        :param kwargs:
        :return:
        '''
        address_id = self.get_argument('address_id')
        user_id = self.get_current_user().get('id')
        user_service.set_db(self.db)
        user_service.delete_address(address_id,user_id)
        self.write_json({'state':200,'info':'删除成功'})

class MemberCollectionHandler(CommonHandler):

    def get(self, *args, **kwargs):
        user_id = self.get_current_user().get('id')
        collection_service.set_rdb(self.rdb)
        collections = collection_service.get_collections_by_user_id(user_id)
        self.echo('member/collection.html',{'collections':collections})

    def post(self, *args, **kwargs):
         pass


class OrderCancleHandler(CommonHandler):

    def get(self,order_id,*args, **kwargs):
        self.write('ok')


from models.express_do import InvoiceOrders
from utils.kuaidi import kuaidi_query,kuaidi_query_2
import ujson

# 查看物流信息
class OrderExpressCheck(CommonHandler):

    def get(self, *args, **kwargs):
        if self.request.uri.startswith('/app'):
            self.echo('app/order/track.html')
        else:
            self.echo('mobile/order/track.html')

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

            # content = kuaidi_query(company.get('code'),invoice_order.express_no)
            # express_data = ujson.loads(content)
            # condition = express_data.get('condition','')
            # is_check = express_data.get('ischeck','')
            # express_content = express_data.get('data')
            # if not express_content:
            #     content = express_data.get('message','')
            #     data = {'state':201,'data':content}
            # else:
            #     if (condition and condition=='F00') and is_check=='1':
            #         invoice_order.express_content = ujson.dumps(express_content)
            #         invoice_order.status=2
            #         self.db.add(invoice_order)
            #         self.db.commit()
            #     data['data']=express_content
            #     data['WaybillNumber']=invoice_order.express_no
            #     data['company_name']=company.get('name')

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

class AppMeHandler(MobileBaseHandler):
    def get(self, *args, **kwargs):
        self.echo('app/member/me.html')