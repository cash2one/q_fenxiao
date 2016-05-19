#encoding:utf-8
__author__ = 'jinkuan'

from services.item.comments_services import CommentsServies
from services.item.item_services import ItemService
# from services.item.ware_house_services import WareHouseServices
from services.users.user_services import UserServices
from services.orders.orders_services import OrderServices
from services.payments.payorder_services import PayOrderService
from apps_app.common_handler import CommonHandler
from common.allinpay.allinpay import create_pay_info
from setting import PAYMENT_BACK_HOST
from models.item_do import ItemDetail
import sys
import datetime
import ujson
import rsa
import base64

comment_service = CommentsServies()
item_service = ItemService()
order_services = OrderServices()
# house_service = WareHouseServices()
payorder_service = PayOrderService()

class AppShoppingCartHandler(CommonHandler):
    def get(self, *args, **kwargs):
        user = self.get_current_user()
        cart_key = 'shopping_cart_'+str(user.get('id'))
        dict_carts = self.mcache.get(cart_key)
        cart_keys = []
        if dict_carts:
            for key in dict_carts:
                cart_keys.append(key)
        query = self.rdb.query(ItemDetail).filter(ItemDetail.deleted==0,ItemDetail.id.in_(cart_keys))
        items = []
        for item in query:
            dict = self.obj_to_dict(item,['id','title','main_pic','price','tax_rate'])
            dict.update(img= dict.pop('main_pic').split(';')[0])
            if user.get('is_bussiness') and item.bussiness_price and item.bussiness_price>0:
                dict['price'] = item.bussiness_price
            dict['item_num'] = dict_carts[item.id]
            items.append(dict)
        self.write_json({'stat':200,'data':{'items':items,'cart_count':query.count()},'info':''})

    def post(self, *args, **kwargs):
        operation = self.get_argument('operation')
        user_id = self.get_current_user().get('id')
        item_id = self.get_argument('item_id')
        cart_key = 'shopping_cart_'+str(user_id)
        dict_carts = self.mcache.get(cart_key)
        item_id = int(item_id)
        if operation == 'add':
            item_service.set_rdb(self.rdb)
            item = item_service.get_by_id(item_id)
            if item.sale_quantity <= item.warning_quantity:
                self.write_json({'stat':201,'info':'商品库存不足，无法加入购物车!'})
                return
            if not dict_carts:
                dict_carts = {item_id:1}
            else:
                if item_id not in dict_carts:
                    dict_carts.update({item_id:1})
                else:
                    value = dict_carts.get(item_id)
                    dict_carts.update({item_id:value+1})
        elif operation == 'decrease':
            value = dict_carts.get(item_id)
            dict_carts.update({item_id:value-1})
        else:
            dict_carts.pop(item_id)
        self.mcache.set(cart_key,dict_carts,3600*24*7)
        self.write_json({'stat':200,'info':'设置成功'})

class ShoppingCartCalculateHandler(CommonHandler):
    def get(self, *args, **kwargs):
        user_id = self.get_current_user().get('id')
        cart_key = 'shopping_cart_'+str(user_id)
        dict_carts = self.mcache.get(cart_key)
        shopping_cart_nums = 0
        if dict_carts:
            for key in dict_carts:
                shopping_cart_nums = shopping_cart_nums+dict_carts[key]
        self.write_json({'stat':200,'data':shopping_cart_nums,'info':''})

class AppCreateOrderHandler(CommonHandler):
    def post(self,*args, **kwargs):
        '''
        订单生成页
        :param args:
        :param kwargs:
        :return:
        '''
        try:
            user = self.get_current_user()
            param_dict = self.request.arguments
            item_ids = param_dict.get('item_ids[]')
            item_accounts = param_dict.get('item_nums[]')
            address_id = param_dict.get('address_id')[0]
            address= UserServices(rdb=self.rdb).get_address_by_id(user.get('id'),address_id)
            items = []
            items_dict = dict(zip(item_ids,item_accounts))
            total_tax = 0         #总关税
            total_item_count = 0  #商品总数
            payable_amount = 0  #商品总金额
            house_ware_name = ''
            item_service.set_rdb(self.rdb)
            item_service.set_db(self.db)
            for item in self.rdb.query(ItemDetail).filter(ItemDetail.deleted==0,ItemDetail.is_online==True,ItemDetail.id.in_(item_ids)):
                if item.sale_quantity<=item.warning_quantity:
                    return self.write_json({'stat':201,'info':item.name+'库存不足'})
                item.num = items_dict.get(str(item.id))
                if user.get('is_bussiness'):
                    if item.bussiness_price and item.bussiness_price>0:
                        item.total_price = int(item.num)*item.bussiness_price
                    else:
                        item.total_price = int(item.num)*item.price
                    item.bussiness_buy=True
                else:
                    item.bussiness_buy=False
                    item.total_price = int(item.num)*item.price
                payable_amount = payable_amount+item.total_price
                total_tax += float(item.total_price*item.tax_rate)/100
                total_item_count = total_item_count+int(item.num)
                items.append(item)

            order_services.set_db(self.db)
            if total_tax<=50:
                total_account = payable_amount
            else:
                total_account = payable_amount + total_tax

            if total_account>1000 and total_item_count>1:
                return self.write_json({'stat':201,'info':'单次购物金额不能超过1000,建议拆成多个订单'})

            is_success,order,pay_order = order_services._add_order(
                    user_id = user.get('id'),
                    payable_amount = payable_amount,
                    pay_amount = total_account,
                    discount_amount = 0,
                    tax_amount = total_tax,
                    recevie_address = address.addressed(),
                    house_ware_name = house_ware_name,
                    items = items,
                    recevie_address_id = address.id,
                    order_from = 'app'
                )
            if is_success:
                item_service.update_item_stock(items,operation = 'jianfa')#锁定库存
                # payorder_service.set_rdb(self.rdb)
                # pay_order = payorder_service.get_payorder_by_order_id(order.id,user.get('id'))
                # if pay_order.pay_status==0:
                #     gmt_created = datetime.datetime.strftime(pay_order.gmt_created,'%Y%m%d%H%M%S')
                #     payback_url = self.reverse_url('allinpay_payment_payback',order.id,order.order_no)
                #     params = create_pay_info_app(pay_order.order_no,'','', pay_order.amount,gmt_created,
                #                              return_url=PAYMENT_BACK_HOST+payback_url,notify_url=PAYMENT_BACK_HOST+payback_url)
                #     temp_params = ''
                #     for param in params:
                #         temp_params += str(param.keys()[0])+'='+str(param[param.keys()[0]])+'&'
                #     temp_params = temp_params[0:-1]

                cart_key = 'shopping_cart_'+str(user.get('id'))
                dict_carts = self.mcache.get(cart_key)
                if dict_carts:
                    for item_id in item_ids:
                        item_id = int(item_id)
                        if item_id in dict_carts:
                            dict_carts.pop(item_id) #删除购物车中的商品
                    self.mcache.set(cart_key,dict_carts,3600*24*7)
                self.write_json({'stat':200,
                                 'data':{'pay_url':'http://m.qqqg.com/h5/order/allinpay/'+str(user.get('id'))+'/'+str(order.id)+'/'+str(order.order_no)+'.html',
                                         'pay_mount':pay_order.amount
                                        }
                               })
        except Exception,e:
            print e.message
            self.db.rollback()
            self.captureException(sys.exc_info())

class AppOrdersHandler(CommonHandler):
    def get(self, *args, **kwargs):
        user_id = self.get_current_user().get('id')
        order_services.set_rdb(self.rdb)
        status = self.get_argument('state','')
        if status == '5':
            status = ''
        data = order_services._list(user_id = user_id, state=status)
        # data = self.get_page_data(query)
        lst_orders = []
        for d in data:
            dict_order = {}
            dict_order['id'] = d.id
            dict_order['pay_mount'] = d.real_amount
            dict_order['payable_amount'] = d.payable_amount
            dict_order['gmt_created'] = d.gmt_created.strftime("%Y-%m-%d %H:%M:%S")
            dict_order['status'] = d.status
            dict_order['pay_status'] = d.pay_status
            dict_order['delivery_status'] = d.delivery_status
            dict_order['is_assess'] = d.is_assess
            dict_order['order_no'] = d.order_no
            dict_order['tax_amount'] = d.tax_amount
            receive_address = ujson.loads(d.recevie_address)
            dict_order['name'] = receive_address.get('user_name')
            dict_order['phone'] = receive_address.get('phone')
            dict_order['province'] = receive_address.get('province')
            dict_order['city'] = receive_address.get('city')
            dict_order['area'] = receive_address.get('area')
            dict_order['address'] = receive_address.get('address')
            if d.status == 1:
                payorder_service.set_rdb(self.rdb)
                pay_order = payorder_service.get_payorder_by_order_id(d.id,user_id)
                if pay_order.pay_status==0:
                    dict_order['pay_url'] = 'http://m.qqqg.com/h5/order/allinpay/'+str(user_id)+'/'+str(d.id)+'/'+str(d.order_no)+'.html'
            query = order_services.query_item_by_order_id(d.id)
            lst_items = []
            order_item_nums = 0
            for item in query:
                dict_item = {}
                dict_item['main_pic'] = item.main_pic.split(';')[0]
                dict_item['title'] = item.title
                dict_item['total_amount'] = item.item_price
                dict_item['single_nums'] = item.buy_nums
                dict_item['name'] = item.name
                dict_item['tax_rate'] = item.tax_rate
                order_item_nums += item.buy_nums
                lst_items.append(dict_item)
            dict_order['items'] = lst_items
            dict_order['order_item_nums'] = order_item_nums
            lst_orders.append(dict_order)
        self.write_json({'stat':200,'data':lst_orders,'info':'success'})

    def post(self, *args, **kwargs):
        '''
        todo:
        :param args:
        :param kwargs:
        :return:
        '''
        operation = self.get_argument('operation')
        user_id = self.get_current_user().get('id')
        order_id = self.get_argument('order_id')
        order_services.set_db(self.db)
        if operation == 'delete':
            cancle_reason = self.get_argument('cancle_reason','其它原因')
            order_services.cancle_order_by_id(user_id,order_id,cancle_reason)
            self.write_json({'stat':200,'info':'操作成功'})
        else:
            order_services.confirmation_receipt_app(user_id,order_id)
            self.write_json({'stat':200,'info':'操作成功'})

class AppDefaultAddressHandler(CommonHandler):
    def post(self, *args, **kwargs):
        '''
        todo:获取默认收获地址
        :param args:
        :param kwargs:
        :return:
        '''
        data = {}
        user_id = self.get_current_user().get('id')
        user_service = UserServices(rdb=self.rdb)
        addresses = user_service.get_default_address(user_id)
        if addresses:
            data = {
                     'address_id':addresses and addresses.id or '',
                     'name':addresses and addresses.name or '',
                     'province':addresses and addresses.province or '',
                     'city':addresses and addresses.city or '',
                     'area':addresses and addresses.area or '',
                     'address':addresses and addresses.address or '',
                     'phone':addresses and addresses.phone or '',
                    }
        self.write_json({'stat':200,'data':data})

