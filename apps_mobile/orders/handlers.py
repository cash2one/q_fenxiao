#encoding:utf-8
__author__ = 'jinkuan'

from services.item.comments_services import CommentsServies
from services.item.item_services import ItemService
from services.users.user_services import UserServices
from services.orders.orders_services import OrderServices
from ..common_handler import CommonHandler
from common.permission_control import mobile_order_authenticated,mobile_user_authenticated
import traceback
import ujson

comment_service = CommentsServies()
item_service = ItemService()
order_services = OrderServices()

class DirectOrderHandle(CommonHandler):

    @mobile_order_authenticated
    def get(self,item_id, *args, **kwargs):
        '''
        直接购买时的确认页
        :param item_id:
        :param args:
        :param kwargs:
        :return:
        '''
        user_id = self.get_current_user().get('id')
        num = self.get_argument('tempBuyAmount') 
        item_service = ItemService(rdb=self.rdb)
        item = item_service.get_by_id(item_id)

        if item.sale_quantity<=item.warning_quantity:
            return self.echo('mobile/member/info.html',{'info':'库存不足'})
        user_service = UserServices(rdb=self.rdb)
        addresses = user_service.get_default_address(user_id)
        if addresses==None:
            addresses = user_service.get_one_address(user_id)
        item.num = int(num)
        drp_user_id = self.get_drp_user_id()
        drp_trade_item = item_service.get_drpTraderItems_by_id(drp_user_id,item_id)
        item.price = drp_trade_item.item_price
        total_account = item.total_price = int(num)*item.price
        self.echo('mobile/member/confirm.html',{'addresses':addresses,
                                                'items':[item],
                                                'total_account':total_account,
                                                'payable_amount':total_account,
                                                'total_tax':0,
                                                'is_cart':False,
                                                'is_abroad':'',
                                                'ware_house_ids':'',
                                                'house_ware_id':'',
                                                })

    def post(self,item_id, *args, **kwargs):
        pass

class OrdersHandler(CommonHandler):

    @mobile_order_authenticated
    def post(self,*args, **kwargs):
        '''
        订单确认提交页
        :param args:
        :param kwargs:
        :return:
        '''
        try:
            user_id = self.get_current_user().get('id')
            item_ids = self.get_arguments('item_id')
            item_accounts=self.get_arguments('item_account')
            address_id = self.get_argument('address_id','1')
            address= UserServices(rdb=self.rdb).get_address_by_id(user_id,address_id)
            user_remark = self.get_argument('remark','')
            is_cart = self.get_argument('is_cart',None)
            drp_user_id = self.get_drp_user_id()

            if is_cart:
                self.clear_item_cookie(item_ids)
            items = []
            items_dict = dict(zip(item_ids,item_accounts))

            total_item_count = 0  #商品总数
            payable_amount = 0
            order_brokerage = 0 #订单佣金

            item_service.set_rdb(self.rdb)
            item_service.set_db(self.db)

            for item in item_service.query_by_ids(item_ids).all():
                item.num = items_dict.get(str(item.id)) #商品数量

                if (int(item.sale_quantity) - int(item.num)) <= int(item.warning_quantity):
                    return self.echo('mobile/member/info.html',{'info':'库存不足'})

                drp_trade_item = item_service.get_drpTraderItems_by_id(drp_user_id,item.id)
                item.price = drp_trade_item.item_price #商品单价

                item.total_price = int(item.num)*item.price
                payable_amount = payable_amount+item.total_price  #商品总金额

                if item.is_drp_item == True: #分销商自己的商品
                    item_brokerage = 0
                else:
                    drp_min_price = item_service.query_drp_min_price_by_id(item.id)
                    item_brokerage = round(float(float(item.price) - float(drp_min_price)),2)
                    item_brokerage = item_brokerage*int(item.num)
                order_brokerage =order_brokerage + item_brokerage #商品佣金

                total_item_count = total_item_count+int(item.num)

                items.append(item)

            total_account = payable_amount

            supply_id = item.vendor_id #供应商,每个订单里商品的供应商都是一致的，每个订单只有一个供应商

            order_services.set_db(self.db)
            is_success,order,pay_order = order_services._add_order(
                    user_id = user_id,
                    drp_user_id = drp_user_id,
                    supply_id = supply_id,
                    payable_amount = payable_amount,
                    pay_amount = total_account,
                    discount_amount = 0,
                    user_remark = user_remark,
                    recevie_address = address.addressed(),
                    items = items,
                    recevie_address_id = address.id,
                    order_from = 'MOBILE_WEB',
                    brokerage = order_brokerage
                )
            if is_success:
                item_service.update_item_stock(items,operation = 'jianfa')#锁定库存
                self.redirect(self.reverse_url('pay_order',order.order_no))
        except Exception,e:
            self.db.rollback()
            self.echo('mobile/member/info.html',{'info':'程序错误:' + traceback.format_exc()})

    def delete(self,order_id, *args, **kwargs):
        '''
        取消订单操作
        :param order_id:
        :param args:
        :param kwargs:
        :return:
        '''
        user_id = self.get_current_user().get('id')
        order_services.set_db(self.db)
        cancle_reason = self.get_argument('cancle_reason','其它原因')
        order_services.cancle_order_by_id(user_id,order_id,cancle_reason)
        self.write_json({'state':200,'info':'操作成功'})

    def put(self,order_id,*args,**kwargs):
        '''
        确认收货操作
        :param order_id: 订单号
        :param args:
        :param kwargs:
        :return:
        '''
        user_id = self.get_current_user().get('id')
        order_services.set_db(self.db)
        order_services.confirmation_receipt(user_id,order_id)
        self.write_json({'state':200,'info':'操作成功'})

    def clear_item_cookie(self,items):
        '''
        todo:清除cookie中当前购买产品
        :param items:
        :return:
        '''
        cart_items = self.get_cookie('fenxiao_item_carts')
        if cart_items:
            cart_items = ujson.loads(cart_items)
            delete_items=[]
            for item in cart_items:
                if str(item.get('item_id')) in items:
                    delete_items.append(item)
            for item in delete_items:
                cart_items.remove(item)
        if cart_items:
            self.set_cookie('fenxiao_item_carts',ujson.dumps(cart_items),expires_days=7)
        else:
            self.clear_cookie('fenxiao_item_carts')

class ShoppingCartHandler(CommonHandler):

    def get(self, *args, **kwargs):
        try:
            user_id = self.get_current_user().get('id')
            item_id = self.get_argument('item_id')
            item_num = self.get_argument('item_num')
            item_service.set_rdb(self.rdb)
            item = item_service.get_by_id(item_id)
            carts = self.get_cookie('fenxiao_item_carts')
            cart_item={
                'user_id':user_id,
                'item_id':item.id,
                'item_num':item_num
            }
            item_account = 0
            if carts:
                carts = ujson.loads(carts)
                is_exist = False
                for cookie_item in carts:
                    if int(cookie_item.get('item_id')) == int(item_id):
                        is_exist=True
                        cookie_item['item_num'] = int(cookie_item.get('item_num'))+int(item_num)
                if not is_exist:
                    carts.append(cart_item)
            else:
                carts=[]
                carts.append(cart_item)
            if len(carts)>0:
                item_account=sum([int(cookie_item['item_num']) for cookie_item in carts])
            self.set_cookie('fenxiao_item_carts',ujson.dumps(carts),expires_days=7)
            self.write_json({'state':200,'account':item_account})
        except Exception,e:
            self.write_json({'state':400,'info':e.message})

    def put(self, *args, **kwargs):
        user_id = self.get_current_user().get('id')
        item_id = self.get_argument('item_id')
        item_num = self.get_argument('item_num',1)
        item_service.set_rdb(self.rdb)
        item = item_service.get_by_id(item_id)
        carts = self.get_cookie('fenxiao_item_carts')
        cart_item={
            'user_id':user_id,
            'item_id':item.id,
            'item_num':item_num,
        }
        item_account = 0
        if carts:
            carts = ujson.loads(carts)
            is_exist = False
            for cookie_item in carts:
                if int(cookie_item.get('item_id')) == int(item_id):
                    is_exist=True
                    cookie_item['item_num'] = int(item_num)<1 and 1 or int(item_num)
            if not is_exist:
                carts.append(cart_item)
        else:
            carts=[]
            carts.append(cart_item)
        if len(carts)>0:
            item_account=sum([int(cookie_item['item_num']) for cookie_item in carts])
        self.set_cookie('fenxiao_item_carts',ujson.dumps(carts),expires_days=7)
        self.write_json({'state':200,'account':item_account})

class ShoppingCartCaculateHandler(CommonHandler):

    def get(self, *args, **kwargs):
        self.echo('mobile/member/cart.html')

    def put(self, *args, **kwargs):
        '''
        购物车列表
        :param args:
        :param kwargs:
        :return:
        '''
        try:
            drp_user_id = self.get_drp_user_id()
            carts = self.get_cookie('fenxiao_item_carts')
            total_count = 0 #购物车总数
            if not carts:
                self.write_json({'state':200,'items':[],'total_count':total_count})
            else:
                carts = ujson.loads(carts)
                item_ids = [c.get('item_id') for c in carts]
                item_keys = {item.get('item_id'):item.get('item_num') for item in carts}
                item_service.set_rdb(self.rdb)

                total_item_count = 0
                user_service = UserServices(rdb=self.rdb)
                
                vendors = user_service.get_vendors()
                vendor_list = []
                for vendor in vendors:
                    good_counts,total_price,tax_acount = 0,0,0 #每个订单下的商品数 购物车总数 总价 税务（分销系统没有税收）
                    items = item_service.query_by_vendorIds(item_ids,vendor.id).all() #每个供应商对应的商品信息
                    
                    if len(items) > 0:
                        dict = []
                        for d in items:
                            
                            #供应商信息
                            dataVendor = {'name':vendor.user_name,
                                          'vendor_id':vendor.id,
                                         }

                            good_counts += int(item_keys[d.id])
                            total_item_count += int(item_keys[d.id])

                            drp_trade_item = item_service.get_drpTraderItems_by_id(drp_user_id,d.id)
                            price = drp_trade_item.item_price
                            total_price += float(price)*float(item_keys[d.id])

                            #购物车商品信息
                            data = {'id':d.id,
                                    'show_id':d.show_id,
                                    'item_no':d.item_no,
                                    'name':d.name,
                                    'title':d.title,
                                    'orgin_price':d.orgin_price,
                                    'price':price,
                                    'inner_price':d.inner_price,
                                    'main_pic':d.main_pic,
                                    'is_online':d.is_online,
                                    'quantity':d.quantity,
                                    'min_limit_quantity':d.min_limit_quantity,
                                    'max_limit_quantity':d.max_limit_quantity,
                                    'amount':item_keys[d.id], #添加商品数
                                    }
                                    
                            dict.append(data)

                        dataVendor['items'] = dict
                        dataVendor['good_counts'] = good_counts
                        dataVendor['total_price'] = total_price
                        vendor_list.append(dataVendor)
                self.write_json({'state':200,'total_count':total_item_count,'items':vendor_list})
        except Exception,e:
            self.write_json({'stat':400,'info':e.message})

    def delete(self, *args, **kwargs):
        item_ids = self.get_argument('item_id',None)
        carts = self.get_cookie('fenxiao_item_carts')
        if carts:
            carts = ujson.loads(carts)
            for item_id in item_ids.split(';'):
                for cookie_item in carts:
                    if int(cookie_item.get('item_id')) == int(item_id):
                        carts.remove(cookie_item)
        item_account = 0
        if len(carts) > 0:
            item_account = sum([int(cookie_item['item_num']) for cookie_item in carts])
        self.set_cookie('fenxiao_item_carts',ujson.dumps(carts),expires_days=7)
        self.write_json({'state':200,'account':item_account,'info':'购物车删除成功'})

    def post(self, *args, **kwargs):
        '''
        提交页面
        :param args:
        :param kwargs:
        :return:
        '''
        try:
            self.get_paras_dict()
            item_ids = self.get_arguments('item_id')
            tempBuyAmount = self.qdict.get('tempBuyAmount')
            wherefrom = self.qdict.get('from')
            user_id = self.get_current_user().get('id')

            item_service = ItemService(rdb=self.rdb)
            user_service = UserServices(rdb=self.rdb)
            addresses = user_service.get_default_address(user_id=user_id)

            if addresses==None:
                addresses = user_service.get_one_address(user_id)
            if wherefrom=='cart':
                cart_items = ujson.loads(self.get_cookie('fenxiao_item_carts'))
                item_keys = {item.get('item_id'):item.get('item_num') for item in cart_items}

            total_item_count = 0  #商品总数
            payable_amount = 0  #商品总金额
            items=[]
            drp_user_id = self.get_drp_user_id()
            for item in item_service.query_by_ids(item_ids):
                if wherefrom=='cart':
                    item.num = item_keys.get(item.id)
                else:
                    item.num = tempBuyAmount
                drp_trade_item = item_service.get_drpTraderItems_by_id(drp_user_id,item.id)
                item.price = drp_trade_item.item_price
                item.total_price = int(item.num)*int(item.price)

                payable_amount = payable_amount+item.total_price

                total_item_count = total_item_count+int(item.num)

                items.append(item)

            total_account = payable_amount
            self.echo('mobile/member/confirm.html',{
                'addresses':addresses,
                'items':items,
                'ware_house_ids':'',
                'total_account':total_account,
                'payable_amount':payable_amount,
                'is_cart':True,
                })

        except Exception,e:
            self.db.rollback()
            self.echo('mobile/member/info.html',{'info':'程序错误:' + traceback.format_exc()})