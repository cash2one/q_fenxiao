#encoding:utf-8
__author__ = 'gaoaifei'
from ..member import UserCenterHandler
from services.orders.orders_services import OrderServices
from services.users.user_services import UserServices
from services.item.item_services import *
from models.orders_do import Orders
from services.member.collection_service import MemberCollectionsServices
from services.item.comments_services import CommentsServies
from services.locations.location_services import LocationServices
from conf.cache_key import COLLECTION_CACHE_KEY
from utils.cache_manager import MemcacheManager
from utils.logs import LOG
_log = LOG('locations_log')

import sys
from data_cache.express_company_cache import ExpressCompanyCache
order_service = OrderServices()
user_service = UserServices()
collection_service = MemberCollectionsServices()
item_service = ItemService()
comment_service = CommentsServies()

class AddressHandler(UserCenterHandler):

    def get(self, *args, **kwargs):
        '''
        地址列表页
        :param args:
        :param kwargs:
        :return:
        '''
        user_id = self.get_current_user().get('id')
        user_service.set_rdb(self.rdb)
        addresses = user_service.get_address(user_id)
        self.echo('member/my_address.html',{'parent_category_id':'','menu':3,'addresses':addresses})


    def post(self, *args, **kwargs):
        pass

class MemberOrdersHandler(UserCenterHandler):
    '''
    我的订单页
    '''
    def get(self, *args, **kwargs):
         try:
            user_id = self.get_current_user().get('id')
            order_service.set_rdb(self.rdb)
            state = self.get_argument('state','')
            query = order_service._list(user_id=user_id,state=state)
            data = self.get_page_data(query)
            tmp_query = order_service._list(user_id=user_id)
            waiting_pay= tmp_query.filter(Orders.status==1,Orders.pay_status==0).count()
            waiting_deliver = tmp_query.filter(Orders.pay_status==1,Orders.delivery_status==0).count()
            waiting_recieve = tmp_query.filter(Orders.pay_status==1,Orders.delivery_status==1).count()
            waiting_assess = tmp_query.filter(Orders.delivery_status==2,Orders.is_assess==False).count()
            page_url = self.get_page_url(self.get_argument('page',1))
            self.echo('member/my_order.html',{'parent_category_id':'',
                                              'data':data,
                                              'order_service':order_service,
                                              'waiting_pay':waiting_pay,
                                              'waiting_deliver':waiting_deliver,
                                              'waiting_recieve':waiting_recieve,
                                              'waiting_assess':waiting_assess,
                                              'state':state,
                                              'page_url':page_url,
                                              'menu':1
                                              })
         except Exception,e:
             print e.message

    def get_item_old_price(self,order_id,item_id):
        order_service.set_rdb(self.rdb)
        orders = order_service.get_item_old_price(order_id,item_id)
        return orders.item_price

class MemberOrderDetailHandler(UserCenterHandler):
    '''
    查看订单详情
    '''
    def get(self,order_no, *args, **kwargs):
        user_id = self.get_current_user().get('id')
        order_service.set_rdb(self.rdb)
        order = order_service.get_order_no(order_no,user_id)
        items = order_service.query_item_by_order_no(order_no=order_no)
        self.echo('order/order_detail.html',{'order':order,'items':items},layout='order/order_base.html')



class MemberAddressHandler(UserCenterHandler):

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

            location_service = LocationServices(rdb=self.db)
            province = location_service.get_by_id('province',self.qdict.get('province'))
            city = location_service.get_by_id('city',self.qdict.get('city'))
            area = location_service.get_by_id('area',self.qdict.get('area'))
            info = 'user_id:'+str(user_id)+\
                   '   receive_name:'+self.qdict.get('name')+\
                   '   receive_phone:'+self.qdict.get('phone')+\
                   '   location_id:'+str(self.qdict.get('province'))+","+str(self.qdict.get('city'))+","+str(self.qdict.get('area'))+\
                   '   location_name:'+province.name+","+city.name+","+area.name
            if area.father != city.id:
                info = info+'   status:n'
                _log.info(info)
                self.write_json({'status':'n','info':'请核对您的地址'})
                return
            else:
                _log.info(info)
            font_card_url,back_card_url= '',''#upload_card(self,'font_card'),upload_card(self,'back_card')
            user_address = user_service.add_recieve_address(user_id,
                                                            name=''.join(self.qdict.get('name').strip().split()),
                                                            card_num=self.qdict.get('card_num').upper(),
                                         phone=self.qdict.get('phone').strip(),
                                         province=self.qdict.get('province').strip(),
                                         city=self.qdict.get('city'),
                                         area=self.qdict.get('area'),
                                         address=''.join(self.qdict.get('address').strip().split()),
                                         address_id=address_id,
                                         font_card=font_card_url,
                                            back_card=back_card_url
                                         )
            self.write_json({'status':'y','info':'成功','addressId':user_address.id})
        except Exception,e:
            self.captureException(sys.exc_info())
            self.write_json({'status':'n','info':e.message,'addressId':''})

    def delete(self, *args, **kwargs):
        address_id = self.get_argument('address_id')
        user_id = self.get_current_user().get('id')
        user_service.set_db(self.db)
        user_service.delete_address(address_id,user_id)
        self.write_json({'state':200,'info':'删除成功'})

        # data={"error":0,
        #         "url":options.IMG_DOMAIN+'/'+save_name,
        #         'msg':u'上传成功',
        #         'id':str(12),
        #         "jsonrpc" : "2.0",
        #         "result" : True
        #      }
class MemberCollectionHandler(UserCenterHandler):

    def get(self, *args, **kwargs):
        '''
        我的收藏商品列表
        :param args:
        :param kwargs:
        :return:
        '''
        user_id = self.get_current_user().get('id')
        collection_service.set_rdb(self.rdb)
        collections = collection_service.get_collections_by_user_id(user_id)
        data = self.get_page_data(collections)
        collection_count = collections.count()
        self.echo('member/collection.html',{'collections':data,'collection_count':collection_count,'menu':2})

    def post(self, *args, **kwargs):
        '''
        添加收藏 1、入库 2、添加缓存
        :param args:
        :param kwargs:
        :return:
        '''
        try:
            self.get_paras_dict()
            item_id = self.qdict.get('item_id')
            user_id = self.get_current_user().get('id')
            # 添加缓存
            self.set_collection_cache(item_id,user_id)

            collection_service.set_rdb(self.rdb)
            collection = collection_service.check_item_is_collection(item_id,user_id)
            if not collection:
                collection_service.set_db(self.db)
                collection_service.add_collection(item_id,user_id)
            self.write_json({'state':200,'msg':'收藏成功'})
        except Exception,e:
            self.captureException(sys.exc_info())
            self.write_json({'state':400,'info':e.message,'addressId':''})

    def delete(self, *args, **kwargs):
        '''
        取消收藏：1、物理删除数据库中的收藏记录；2、删除对应的缓存
        :param args:
        :param kwargs:
        :return:
        '''
        self.get_paras_dict()
        item_id = self.qdict.get('item_id')
        user_id = self.get_current_user().get('id')
        # 删除缓存
        self.collection_delete(item_id,user_id)
        collection_service.set_db(self.db)
        collection_service.cancle_member_collection(item_id,user_id)
        self.write_json({'state':200,'msg':'取消收藏成功'})

    def set_collection_cache(self,item_id,user_id):
        '''
        收藏商品缓存
        :param item_id:
        :param user_id:
        :return:
        '''
        if self.mcache:
            pass
        else:
            self.mcache = MemcacheManager().get_conn()
        key = str(COLLECTION_CACHE_KEY.format(user_id))
        collection = self.mcache.get(key)
        if collection==None:
            cache_item = []
            cache_item.append(str(item_id))
            self.mcache.set(key,ujson.dumps(cache_item))
        else:
            cache_item = ujson.loads(collection)
            if str(item_id) in cache_item:
                pass
            else:
                cache_item.append(str(item_id))
                self.mcache.set(key,ujson.dumps(cache_item))

    def collection_delete(self,item_id, user_id):
        '''
        删除该用户对应收藏的商品缓存
        :param item_id:
        :param user_id:
        :return:
        '''
        if self.mcache:
            pass
        else:
            self.mcache = MemcacheManager().get_conn()
        key = str(COLLECTION_CACHE_KEY.format(user_id))
        colls = self.mcache.get(key)
        if colls:
            cache_item = ujson.loads(colls)
            if str(item_id) in cache_item:
                cache_item.remove(item_id)
                self.mcache.set(key,ujson.dumps(cache_item))
            else:
                pass
        else:
            pass

    def get_item_by_item_id(self,item_id):
        '''
        获取商品信息
        :param item_id:
        :return:
        '''
        item_service.set_rdb(self.rdb)
        item = item_service.get_by_id(item_id)
        comment_service.set_rdb(self.rdb)
        comment_count = comment_service.get_comment_count_by_item_id(item_id)
        self.title = item.seo_title
        self.keywords = item.seo_keywords
        self.description = item.seo_description
        self.parent_category_id = item.top_category_id
        return {'item':item,'comment_count':comment_count}

class OrderCancleHandler(UserCenterHandler):

    def get(self,order_id,*args, **kwargs):
        self.write('ok')


from models.express_do import InvoiceOrders
from utils.kuaidi import kuaidi_query,kuaidi_query_2
import ujson
class OrderExpressCheck(UserCenterHandler):

    def get(self,order_no):
        user_id = self.get_current_user().get('id')
        #invoice_order = self.db.query(InvoiceOrders.express_company_id,InvoiceOrders.express_no,InvoiceOrders.status,InvoiceOrders.express_content).\
        invoice_order = self.db.query(InvoiceOrders).\
            filter(InvoiceOrders.deleted==0,InvoiceOrders.order_no==order_no,InvoiceOrders.user_id==user_id).scalar()
        content=''
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
            #     content=express_data.get('message','')
            #     data={'state':201,'data':content}
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
                data['state'] = 201
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


