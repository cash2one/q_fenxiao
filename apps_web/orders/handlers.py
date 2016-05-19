#encoding:utf-8
__author__ = 'binpo'

import tornado.web
from common.base_handler import BaseHandler
from services.item.comments_services import CommentsServies
from services.item.item_services import ItemService

from services.users.user_services import UserServices
from services.orders.orders_services import OrderServices
import ujson
import sys
from ..common_handler import CommonHandler
from data_cache.user_cache import UserCache
from utils.logs import LOG
import datetime
_log = LOG('order_address_logs')

comment_service = CommentsServies()
item_service = ItemService()
order_services = OrderServices()
user_cache = UserCache()


class OrdersHandler(BaseHandler):

    @tornado.web.authenticated
    def post(self,*args, **kwargs):
        '''
        订单提交页面
        :param args:
        :param kwargs:
        :return:
        '''
        try:
            user_id = self.get_current_user().get('id')
            user = self.get_current_user()
            item_ids = self.get_arguments('item_id')
            is_abroad = bool(self.get_argument('is_abroad')) #是否为跨境电商 1 是 0国内
            item_accounts=self.get_arguments('item_account')
            address_id = self.get_argument('address_id','1')
            address= UserServices(rdb=self.rdb).get_address_by_id(user_id,address_id)
            user_remark = self.get_argument('remark','')
            is_cart = self.get_argument('is_cart',None)
            house_id = self.get_argument('house_ware_id')
            if is_cart: #点击购买时产生一个order，从购物车中来，要删除存储的购买商品，如果“直接购买”则忽略
                self.clear_item_cookie(item_ids)
            items = []
            items_dict = dict(zip(item_ids,item_accounts))
            total_account = 0   #总金额
            total_tax=0         #总关税
            total_item_count=0  #商品总数
            payable_amount = 0  #商品总金额
            house_ware_name = ''
            item_service.set_rdb(self.rdb)
            item_service.set_db(self.db)
            category_ids=[]

            for item in item_service.query_by_ids(item_ids):
                is_unpay=True
                is_abroad = item.is_abroad
                if item.is_abroad:
                    category_ids.append(item.category_id)
                    is_unpay = user_cache.user_daily_pay_check(item.category_id,address.card_num)
                if not is_unpay:
                    self.echo('order/info.html',{'state':400,'info':'此收货用户还有未支付订单,请先支付未支付订单，或者换其他收货人'})
                    # self.write_json({'state':400,'info':'此收货用户还有未支付订单,请先支付未支付订单，或者换其他收货人'})
                    return
                is_payed = True
                if item.is_abroad:
                    is_payed = user_cache.user_daily_buy_check(item.category_id,address.card_num)
                if not is_payed:
                    self.echo('order/info.html',{'state':400,'info':'此收货用户今天已经买过了,请换其他收货人'})
                    # self.write_json({'state':400,'info':'此收货用户今天已经买过了,请换其他收货人'})
                    return
                if item.sale_quantity<=item.warning_quantity:
                    self.echo('order/info.html',{'state':400,'info':'库存不足'})
                    # self.write_json({'state':400,'info':'库存不足'})
                    return
                    #return self.echo('order/info.html',)

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
            if total_tax<=50 or is_abroad==False:#当是国内电商提交时，不用收税
                total_account = payable_amount
            else:
                total_account = payable_amount + total_tax

            #跨境电商才有此限制
            if is_abroad==True:
                if total_account>1000 and total_item_count>1:
                    self.echo('order/info.html',{'info':'单次购物金额不能超过1000,建议拆成多个订单'})
                    #self.write_json({'state':400,
                    return

            (fok,font_card_url),(bok,back_card_url) = upload_card(self,'font_card'),upload_card(self,'back_card')
            if fok:
                address.card_img1 = font_card_url
            if bok:
                address.card_img2 = back_card_url
            if fok and bok:
                self.db.add(address)
                self.db.commit()
            is_success,order,pay_order = order_services._add_order(
                user_id=user_id,
                payable_amount=payable_amount,
                pay_amount=total_account,
                discount_amount=0,
                tax_amount=total_tax,
                user_remark=user_remark,
                recevie_address = address.addressed(),
                house_ware_name = house_ware_name,
                items=items,
                recevie_address_id = address.id,
                order_from='PC_WEB',
                is_abroad = is_abroad,
                house_ware_id = house_id
                )
            if is_success:
                item_service.update_item_stock(items,operation='jianfa')#锁定库存
                #--------------------单一商品处理方式-----------------------
                for c in category_ids:
                    # category = item_service.get_category_name_by_id(c)
                    # if category.is_abroad:
                    user_cache.set_daily_pay_cache(c,address.card_num,order_id=order.id)
                #print self.reverse_url('pay_order',order.order_no)
                info = 'user_id:'+str(user_id)+\
                   '   address_id:'+address_id+\
                   '   province:'+address.province+\
                   '   city:'+address.city+\
                   '   area:'+address.area+\
                   '   address:'+address.address+\
                   '   time:'+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+\
                   '   address_json:'+ujson.dumps(address.addressed())+\
                   '   order_no:'+order.order_no
                _log.info(info)
                #self.write_json({'state':200,'info':self.reverse_url('pay_order',order.order_no)})
                #return
                self.redirect(self.reverse_url('pay_order',order.order_no))
        except Exception,e:
            self.db.rollback()
            self.captureException(sys.exc_info())
            #self.write_json({'state':400,'info':'程序错误'+e.message})
            self.echo('order/info.html',{'info':'程序错误'+e.message})

    @tornado.web.authenticated
    def get(self,item_id, *args, **kwargs):
        '''
        点击直接购买页面渲染数据内容
        :param item_id:
        :param args:
        :param kwargs:
        :return:
        '''
        user_id = self.get_current_user().get('id')
        user = self.get_current_user()
        num = self.get_argument('item_account')
        item_service = ItemService(rdb=self.rdb)
        item = item_service.get_by_id(item_id)
        is_abroad = item.is_abroad
        house_ware_id = item.ware_house_id
        if item.sale_quantity<=item.warning_quantity:
            return self.echo('order/info.html',{'info':'库存不足'})
        user_service = UserServices(rdb=self.rdb)
        addresses = user_service.get_address(user_id=user_id)
        item.num = int(num)

        item.bussiness_buy=False
        if user.get('is_bussiness'):
            item.bussiness_buy=True
            if item.bussiness_price and item.bussiness_price>0:
                total_account = item.total_price = int(num)*item.bussiness_price
            else:
                total_account = item.total_price = int(num)*item.price
        else:
            total_account = item.total_price = int(num)*item.price
        total_tax = float(item.total_price*item.tax_rate)/100
        if total_tax<=50 or is_abroad==False: #当税率小于等于50 and 国内电商时总金额不需要税钱
            pass
        else:
            total_account = total_account + total_tax
        self.echo('order/order.html',{'addresses':addresses,
                                      'items':[item],
                                      'total_account':total_account,
                                      'is_cart':False,
                                      'total_tax':total_tax,
                                      'house_ware_id':house_ware_id,
                                      'is_abroad':is_abroad},layout='order/order_base.html')

    @tornado.web.authenticated
    def delete(self,order_id, *args, **kwargs):
        '''
        取消订单操作
        :param order_id:
        :param args:
        :param kwargs:
        :return:
        '''
        user_id = self.get_current_user().get('id')
        cancle_reason = self.get_argument('cancle_reason','其它原因')
        order_services.set_db(self.db)
        user_cache.delete_user_daily_pay(order_id)
        order_services.cancle_order_by_id(user_id,order_id,cancle_reason)
        self.write_json({'state':200,'info':'操作成功'})

    @tornado.web.authenticated
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
        cart_items = self.get_cookie('item_carts')
        if cart_items:
            cart_items = ujson.loads(cart_items)
            delete_items=[]
            for item in cart_items:
                if str(item.get('item_id')) in items:
                    delete_items.append(item)
            for item in delete_items:
                cart_items.remove(item)
        if cart_items:
            self.set_cookie('item_carts',ujson.dumps(cart_items),expires_days=7)
        else:
            self.clear_cookie('item_carts')



class ShoppingCartHandler(BaseHandler,CommonHandler):

    def get(self, *args, **kwargs):
        user_id = self.get_current_user() and self.get_current_user().get('id') or ''
        item_id = self.get_argument('item_id')
        item_num = self.get_argument('item_num')
        item_service.set_rdb(self.rdb)
        item = item_service.get_by_id(item_id)
        carts = self.get_cookie('item_carts')
        cart_item = {
            'user_id':user_id,
            'item_id':item.id,
            'item_num':item_num,
            'ware_house_id':item.ware_house_id
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
        self.set_cookie('item_carts',ujson.dumps(carts),expires_days=7)
        self.write_json({'state':200,'account':item_account})

    def put(self, *args, **kwargs):
        user_id = self.get_current_user() and self.get_current_user().get('id') or ''
        item_id = self.get_argument('item_id')
        item_num = self.get_argument('item_num',1)
        item_service.set_rdb(self.rdb)
        item = item_service.get_by_id(item_id)
        carts = self.get_cookie('item_carts')
        cart_item={
            'user_id':user_id,
            'item_id':item.id,
            'item_num':item_num,
            'ware_house_id':item.ware_house_id
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
        self.set_cookie('item_carts',ujson.dumps(carts),expires_days=7)
        self.write_json({'state':200,'account':item_account})

    def delete(self, *args, **kwargs):

        item_id = self.get_argument('item_id',None)
        carts = self.get_cookie('item_carts')
        if carts:
            carts = ujson.loads(carts)
            for cookie_item in carts:
                if int(cookie_item.get('item_id')) == int(item_id):
                    carts.remove(cookie_item)
        item_account=0
        if len(carts)>0:
            item_account=sum([int(cookie_item['item_num']) for cookie_item in carts])
        self.set_cookie('item_carts',ujson.dumps(carts),expires_days=7)
        self.write_json({'state':200,'account':item_account,'info':'购物车删除成功'})

        # carts = self.get_cookie('item_carts')
        # if not carts:
        #     self.echo('order/cart.html',{'items':None,'ware_house_ids':None,'item_keys':None},layout='')
        # else:
        #     carts = ujson.loads(carts)
        #     #items=[]
        #     item_ids = [c.get('item_id') for c in carts]
        #     item_service.set_rdb(self.rdb)
        #     items = item_service.query_by_ids(item_ids)
        #     item_keys={item.get('item_id'):item.get('item_num') for item in carts}
        #     ware_house_ids = list(set([c.get('ware_house_id') for c in carts]))
        #     self.echo('order/cart.html',{'items':items,'ware_house_ids':ware_house_ids,'item_keys':item_keys},layout='')

from common.permission_control import authenticated
class ShoppingCartCaculateHandler(BaseHandler,CommonHandler):

    #@tornado.web.authenticated
    def get(self, *args, **kwargs):
        carts = self.get_cookie('item_carts')
        if not carts:
            self.echo('order/cart.html',{'items':None,'ware_house_ids':None,'item_keys':None},layout='order/order_base.html')
        else:
            carts = ujson.loads(carts)
            #items=[]
            item_ids = [c.get('item_id') for c in carts]
            item_service.set_rdb(self.rdb)
            items = item_service.query_by_ids(item_ids)
            item_keys={item.get('item_id'):item.get('item_num') for item in carts}
            ware_house_ids = list(set([c.get('ware_house_id') for c in carts]))

            self.echo('order/cart.html',{'items':items,'ware_house_ids':ware_house_ids,'item_keys':item_keys},layout='order/order_base.html')

    @authenticated
    def post(self, *args, **kwargs):
        '''
        购物车确定购买页面到结算页面
        :param args:
        :param kwargs:
        :return:
        '''
        item_ids = self.get_arguments('item_id')
        is_abroad = self.get_argument('is_abroad')
        user_id = self.get_current_user().get('id')
        user = self.get_current_user()
        # num = self.get_arguments('num')
        item_service = ItemService(rdb=self.rdb)
        user_service = UserServices(rdb=self.rdb)
        addresses = user_service.get_address(user_id=user_id)
        cart_items = ujson.loads(self.get_cookie('item_carts'))
        item_keys={item.get('item_id'):item.get('item_num') for item in cart_items}
        total_account=0

        total_tax=0         #总关税
        total_item_count=0  #商品总数
        payable_amount = 0  #商品总金额

        items=[]
        #if isinstance(item_ids,(list,tuple)):
        for item in item_service.query_by_ids(item_ids):
            house_ware_id = item.ware_house_id
            item.num = item_keys.get(item.id)

            if user.get('is_bussiness'):
                if item.bussiness_price and item.bussiness_price>0:
                    item.total_price = int(item.num)*item.bussiness_price
                else:
                    item.total_price = int(item.num)*item.price
                item.bussiness_buy=True
            else:
                item.bussiness_buy=False
                item.total_price = int(item.num)*item.price

            # item.total_price = int(item.num)*item.price
            payable_amount = payable_amount+item.total_price

            total_tax += float(item.total_price*item.tax_rate)/100   #关税计算
            total_item_count = total_item_count+int(item.num)
            items.append(item)

        if total_tax<=50 or is_abroad==False:
            total_account = payable_amount
        else:
            total_account = payable_amount + total_tax
        if is_abroad==True:
            if total_account>1000 and total_item_count>1:
                self.echo('order/info.html',{'info':'单次购物金额不能超过1000,建议拆成多个订单'})

        self.echo('order/order.html',{'addresses':addresses,
                                      'items':items,
                                      'total_account':total_account,
                                      'is_cart':True,
                                      'total_tax':total_tax,
                                      'is_abroad':is_abroad,
                                      'house_ware_id':house_ware_id},layout='order/order_base.html')


    def get_ware_house_by_id(self,ware_house_id):
        '''
        todo
        :param ware_house_id:
        :return:
        '''
        ware_house_service.set_rdb(self.rdb)
        ware_house = ware_house_service.get_by_id(ware_house_id)
        return ware_house


class UserDailyBuyCheck(BaseHandler):

    def get(self):
        pass


from tornado.options import options
from setting import ACCESS_ID,SECRET_ACCESS_KEY
import oss2
from utils.random_utils import get_chars
from utils.datetime_util import datetime_format
import re

#RE_SPECIAL_STR = re.compile(r'[~!@#$%^&*()))_+=:;",<>{}\]\[\-\s]') #特殊字符串替换
RE_SPECIAL_STR = re.compile(r'[^\w.]') #特殊字符串替换

#600861
def upload_card(http_handle,param_name):

    file_metas=http_handle.request.files.get(param_name)

    if http_handle.request.files == {} or param_name not in http_handle.request.files:
        return False,'参数不存在'
    avatar_file = http_handle.request.files[param_name][0]

    name_prefix = datetime_format(format='%H%M%S')+get_chars()
    meta =file_metas[0]

    meta['filename'] = RE_SPECIAL_STR.sub('0',meta['filename'])
    #filename = name_prefix+meta['filename']
    save_name = name_prefix + meta['filename']
    contents = meta['body']

    # import StringIO
    # output = StringIO.StringIO()
    # meta.save(output)
    # contents = output.getvalue()
    # output.close()
    endpoint = 'http://oss-cn-hangzhou.aliyuncs.com'
    auth = oss2.Auth(ACCESS_ID,SECRET_ACCESS_KEY)
    bucket = oss2.Bucket(auth, endpoint, 'qqqg')

    # Bucket中的文件名（key）为storage.txt
    # key = 'story.txt'
    # bucket.put_object(key,'hello world')
    # 上传
    bucket.put_object(save_name,contents)
    return True,options.IMG_DOMAIN+'/'+save_name