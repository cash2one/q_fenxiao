#encoding:utf-8
__author__ = 'binpo'
from common.base_handler import BaseHandler
from services.item.comments_services import CommentsServies
from services.item.item_services import ItemService
from services.orders.orders_services import OrderServices
from ..common_handler import CommonHandler
from models.item_do import ItemComment
from utils.cache_manager import MemcacheManager
from services.member.collection_service import MemberCollectionsServices
from conf.cache_key import COLLECTION_CACHE_KEY
from common.permission_control import authenticated
from services.item.brand_service import BrandService
from services.attributes.attributes_service import AttributesService
from services.sites.nav_services import NavServices
import ujson
import sys
import datetime
import tornado.web

item_service = ItemService()
comment_service = CommentsServies()
order_service = OrderServices()
collection_service = MemberCollectionsServices()
brand_service = BrandService()
attributes_service = AttributesService()
sitenav_Services = NavServices()

class NavHandler(BaseHandler,CommonHandler):

    def get(self, *args, **kwargs):
        '''
        根据类目id获取二级类目菜单
        :param show_id:
        :return:
        '''
        category_html = self.mcache.get('category_html')
        category_service = ItemService(rdb=self.db)
        if not category_html:
            sitenav_Services.set_rdb(self.rdb)
            attributes_service.set_rdb(self.rdb)
            navs = sitenav_Services.query_all()
            category_lists = [{
                'top_category_id':nav.category_id,
                'name':nav.name,
                'link':nav.link,
                'show_id':nav.show_id,
                'categorys':[ {
                              'parent_id':category.parent_id,
                              'show_id':category.show_id,
                              'category_id':category.id,
                              'name':category.name,
                              'attributes':[{
                                  'attribute_id':att.id,
                                  'name':att.attribute_name,
                                  'value':[{
                                               'att_value_id':val.id,
                                               'att_value':val.attribute_value
                                            } for val in attributes_service._list_attribute_value(att.id)]
                                    } for att in attributes_service.get_attribute_by_category_id(category.id)]
                              }
                  for category  in category_service.get_categorys_by_id(nav.category_id)]
            } for nav in navs]
            #设置缓存
            category_html = category_lists
            self.mcache.set('category_html',category_html,7*24*36)
        self.write_json({'state':200,
                         'msg':'ok',
                         'categorys': category_html})

class ItemscategoryHandler(BaseHandler,CommonHandler):

    def get(self,show_id, *args, **kwargs):
        '''
        二级目录列表：品牌  属性展示
        :param show_id:
        :return:
        '''
        # try:
        # attribute_id = self.get_argument('attribute_id',0)
        # attribute_value_id = self.get_argument('catindex',0)#商品属性id
        catindex = self.get_argument('catindex','0')
        search_content={}
        if catindex:
            sign = catindex[-1]
            if sign==',':
                catindex = catindex[:-1]
            for t in catindex.split(','):
                if t and t!='0':
                    key,value = t.split('_')
                    search_content[str(key)] = t
        brand_id = self.get_argument('brand_id','0')#品牌id
        sortfield = self.get_argument('sortfield','0')#排序值 0人气 1销售 2价格，默认为0
        is_desc = self.get_argument('is_desc','desc')#生序 降序 True 降序 Flase生序
        category_id = self.get_id_by_show_id(show_id)
        item_service.set_rdb(self.rdb)
        ItemCategory = item_service.get_category_name_by_id(category_id)
        category_name = ItemCategory.name
        parent_id = ItemCategory.parent_id
        categorys = item_service.get_categorys_by_id(parent_id)
        brand_service.set_rdb(self.rdb)
        brands = brand_service.get_brands_by_category_id(category_id)
        attributes_service.set_rdb(self.rdb)
        attributes = [
            {
                'attribute_id':att.id,
                'name':att.attribute_name,
                'value':[{
                        'attribute_value_id':val.id,
                        'attribute_value':val.attribute_value
                         } for val in attributes_service.get_attribute_value_by_id(att.id)]
            } for att in attributes_service.get_attribute_by_category_id(category_id)
        ]
        item_ids = [] #搜索属性商品id值
        arrs = None
        if catindex!='0':
            arrs = catindex.split(',')
            for arr in arrs :
                arr_ids = arr.split('_')
                attribute_id = arr_ids[0]
                attribute_value_id = arr_ids[1]
                item_idarr = attributes_service.get_item_attribute_filters(attribute_value_id,attribute_id,item_ids)
                if item_idarr.count()>0:
                    for item_id in item_idarr:
                        item_ids.append(item_id[0])
        # 商品信息
        item_service.set_rdb(self.rdb)
        items = item_service.get_items_by_category_id(category_id,brand_id,catindex,item_ids,sortfield,is_desc)
        list = self.get_page_data(items)
        item_count = items.count()
        # except Exception,e:
        #     self.captureException(sys.exc_info())
        self.echo('items/category.html',{'category_name':category_name,
                                         #'attribute_value_id':int(attribute_value_id),
                                         #'attribute_id':int(attribute_id),
                                         'arrs':arrs,#接收的属性值ids
                                         'catindex':catindex,
                                         'brand_id':int(brand_id),
                                         'categorys':categorys,
                                         'is_desc':is_desc,
                                         'sortfield':sortfield,
                                         'item_count':item_count,
                                         'brands':brands,
                                         'show_id':show_id,
                                         'attributes':attributes,
                                         'lists':list,
                                         'search_content':search_content
                                         })
    def get_comments_count(self,item_id):
        '''
        获取商品评论条数
        :param item_id:
        :return:
        '''
        item_service.set_rdb(self.rdb)
        return item_service.get_comments_count_by_item_id(item_id)

class ItemsQueryHandler(BaseHandler,CommonHandler):

    def get(self,show_id,*args, **kwargs):
        try:
            category_id = self.get_id_by_show_id(show_id)
            item_service.set_rdb(self.rdb)
            query = item_service._list(is_online=True,category_id=category_id,order_by = 'sale_quantity desc,gmt_modified desc')
            self.parent_category_id=category_id
        except Exception,e:
            self.captureException(sys.exc_info())
        self.echo('items/list.html',{'query':query})


class ItemsDetailHandler(BaseHandler,CommonHandler):

    def get(self,show_id, *args, **kwargs):
        item_id = self.get_id_by_show_id(show_id)
        item_service.set_rdb(self.rdb)
        item = item_service.get_by_id(item_id)
        self.set_user_view_cookie(item)
        item_carts = self.get_cookie('item_carts')
        self.set_item_views(item_id)
        cart_count=0
        if item_carts:
            carts = ujson.loads(item_carts)
            cart_count = sum([int(c.get('item_num')) for c in carts])
        comment_service.set_rdb(self.rdb)
        comment_count = comment_service.get_comment_count_by_item_id(item_id)
        # 是否收藏
        user = self.get_current_user()
        is_collection = 0
        if user:
            if self.mcache:
                pass
            else:
                self.mcache = MemcacheManager().get_conn()
            user_id = user.get('id')
            collection = self.check_item_is_collection_on_cache(item_id,user_id)
            if collection:
                is_collection = 1
            else:
                is_collection = 0

        self.title = item.seo_title
        self.keywords = item.seo_keywords
        self.description = item.seo_description
        self.parent_category_id = item.top_category_id
        self.echo('items/detail.html',{'item':item,'cart_count':cart_count,'comment_count':comment_count,'is_collection':is_collection})

    def post(self, *args, **kwargs):
        pass

    def set_user_view_cookie(self,item):
        items = self.get_secure_cookie('user_history_view')
        item_service.set_rdb(self.rdb)
        comments = item_service.get_comments_count_by_item_id(item.id)
        if item:
            tmp_item = {
                'id':item.id,
                'title':item.title.encode('utf-8'),
                'comments':comments,
                'price':item.price,
                'inner_price':item.inner_price,
                'main_pic':item.main_pic and item.main_pic.split(';')[0]+'@158w.jpg' or ''
            }
        if not items and item:
            items = [tmp_item]
        else:
            items = ujson.loads(items)
            for i in items:
                if i.get('id') ==item.id:
                    items.remove(i)
            if len(items)>=4:
                items.remove(items[0])
            items.append(tmp_item)
        self.set_secure_cookie('user_history_view',ujson.dumps(items),domain=self.cookie_domain,expires_days=7)

    def check_item_is_collection_on_cache(self,item_id,user_id):
        '''
        判断是否已经收藏
        :param user_id:
        :param item_id:
        :return:boolen True标示已经收藏 false未收藏
        '''
        key = str(COLLECTION_CACHE_KEY.format(user_id))
        if self.mcache:
            pass
        else:
            self.mcache = MemcacheManager().get_conn()
        collection = self.mcache.get(key)
        if collection:
            if str(item_id) in ujson.loads(self.mcache.get(key)):
                return True
            else:
                return False
        return False

    def set_item_views(self,item_id):
        '''
        用户浏览数更新
        :param item_id:
        :return:
        '''
        if self.mcache:
            pass
        else:
            self.mcache = MemcacheManager().get_conn()
        key = 'item_detail_'+str(item_id)
        pv = self.mcache.get(key)
        if not pv:
            self.mcache.set(key,1)
        else:
            if pv<100:
                self.mcache.set(key,pv+1)
            else:
                item_service.set_db(self.db)
                item_service.update_item_pv(item_id,pv)
                self.mcache.set(key,1)

class HistoryViewHandler(BaseHandler):

    def get(self, *args, **kwargs):
        data = self.get_secure_cookie('user_history_view',None)
        if data:
            self.write(data)
        else:
            self.write_json({})

class SimilarItemsHandler(BaseHandler):

    def get(self,*args, **kwargs):
        item_service.set_rdb(self.rdb)
        category_id = self.get_argument('category_id')
        buy_items,view_items= item_service.detail_side_query_by_category_id(category_id)
        item_service.set_rdb(self.rdb)
        buydata = [{
                'id':item.id,
                'show_id':item.show_id,
                'title':item.title,
                'comments':item_service.get_comments_count_by_item_id(item.id),
                'price':item.price,
                'inner_price':item.inner_price,
                'main_pic':item.main_pic and item.main_pic.split(';')[0]+'@158w.jpg' or ''
            } for item in buy_items]

        viewdata = [{
                'id':item.id,
                'show_id':item.show_id,
                'title':item.title,
                'comments':item.comments,
                'price':item.price,
                'inner_price':item.inner_price,
                'main_pic':item.main_pic and item.main_pic.split(';')[0]+'@158w.jpg' or ''
            } for item in view_items]

        self.write_json({
            'viewitems':viewdata,
            'buyitems':  buydata
        })


class CommentHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        '''
        商品评论页: 展示商品内容
        :param args:
        :param kwargs:
        :return:
        '''
        self.get_paras_dict()
        order_no = self.qdict.get('order_no')
        user_id = self.current_user.get('id')
        order_service.set_rdb(self.rdb)
        page_data = []
        try:
            data = order_service.query_item_by_order_no(order_no)
            for d in data:
                item_id = d.id
                comment_service.set_rdb(self.rdb)
                comment = comment_service.check_comment_by_user_id(item_id,user_id,order_no)
                page_data.append((d,comment))

        except Exception,e:
            print e.message
        self.echo('items/comment.html', {'data':page_data})

    @authenticated
    def post(self, *args, **kwargs):
        '''
        添加评论
        之前判断评论是否存在
        :param args:
        :param kwargs:
        :return:
        '''
        self.get_paras_dict()
        user_id = self.current_user.get('id')
        user_name = self.current_user.get('nick')
        comment_id = self.qdict.get('comment_id','')
        order_no = self.qdict.get('order_no')
        if comment_id: #追评
            add_show_imgs = self.qdict.get('add_show_imgs')
            if add_show_imgs!="":
                self.qdict['is_show'] =  1
            self.qdict['is_add_comment'] = 1
            comment_service.set_db(self.db)
            self.qdict.pop('comment_id')
            is_success,comment = comment_service.update_by_id(comment_id, **self.qdict)
            order_service.set_db(self.db)
            order_service.mark_comment(user_id, order_no, 'two')
            if is_success:
                keys = ['id','show_imgs','add_show_imgs','item_id','order_no',
                        'comment','addition_comment','assess_level','user_name','user_id','is_add_comment']
                data = {key:getattr(comment,key) for key in keys}
            self.write_json({"state":200,"info":"success","data":data})
        else:  #第一次评论
            comment_service.set_db(self.db)
            self.qdict['user_id'] = user_id
            self.qdict['user_name'] = user_name
            show_imgs = self.qdict.get('show_imgs')
            if self.qdict.get('comment')=='':
                self.qdict['comment'] = '默认好评～'
            if show_imgs != "":
                self.qdict['is_show'] = 1
            is_success,comment_id = comment_service._add( **self.qdict)
            order_service.set_db(self.db)
            order_service.mark_comment(user_id, order_no, 'one')
            if is_success:
                self.write_json({"state":200,"info":"success","data":self.qdict,'comment_id':comment_id})


class CommentListHandler(BaseHandler):
    """
    商品评价列表
    :todo 可以将评论内容写入缓存
    :param item_id 商品id
    """
    def get(self,*args, **kwargs):
        self.get_paras_dict()
        item_id = self.qdict.get('item_id')
        assess_level = self.qdict.get('assess_level','')#好 中 差评
        is_show = self.qdict.get('is_show','')#是否晒单
        is_add_comment = self.qdict.get('is_add_comment','') #是否追加评论
        comment_service.set_rdb(self.rdb)
        query = comment_service._list(item_id,assess_level,is_show,is_add_comment)
        data = self.get_page_data(query)
        all_count = self.rdb.query(ItemComment).filter(ItemComment.deleted==0,ItemComment.item_id==item_id).count()
        good_count = self.rdb.query(ItemComment).filter(ItemComment.assess_level==2,ItemComment.deleted==0,ItemComment.item_id==item_id).count()
        mid_count = self.rdb.query(ItemComment).filter(ItemComment.assess_level==1,ItemComment.deleted==0,ItemComment.item_id==item_id).count()
        bad_count = self.rdb.query(ItemComment).filter(ItemComment.assess_level==0,ItemComment.deleted==0,ItemComment.item_id==item_id).count()
        add_comment_count = self.rdb.query(ItemComment).filter(ItemComment.is_add_comment==0,ItemComment.deleted==0,ItemComment.item_id==item_id).count()
        show_count = self.rdb.query(ItemComment).filter(ItemComment.is_show==0,ItemComment.deleted==0,ItemComment.item_id==item_id).count()
        if all_count:
            good_percent = round(float(good_count)/float(all_count), 1)
        else:
            good_percent = 1
        self.write_json({"state":200,
                         "msg":"操作成功",
                         "data":{"page_num":data.page_num,
                                 "page_size":data.page_size,
                                 "page":data.page,
                                 "page_start":data.page_start,
                                 "page_end":data.page_end,
                                 "result":[{key:getattr(d,key) for key in d.columns() if not isinstance(d,datetime.datetime) } for d in data.result]},
                         "all_count":all_count,
                         "good_count":good_count,
                         "mid_count":mid_count,
                         "bad_count":bad_count,
                         "add_comment_count": add_comment_count,
                         "show_count": show_count,
                         "good_percent":good_percent
                         })