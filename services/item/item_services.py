#encoding:utf-8
__author__ = 'wangjinkuan'

from services.base_services import BaseService
from models.item_do import ItemCategory,ItemDetail,ItemPic,Merchant,Unit,ItemComment,DrpTraderItems
from sqlalchemy import or_

class ItemService(BaseService):

    def create_item_category(self,**kwargs):
        '''
        todo:创建商品分类
        :param kwargs:
        :return:
        '''
        ic = ItemCategory()
        ic.name = kwargs.get('name')
        ic.parent_id = kwargs.get('parent_id')
        ic.desc = kwargs.get('desc','desc')
        ic.is_abroad = kwargs.get('is_abroad')
        self.db.add(ic)
        self.db.flush()
        ic.show_id = self.set_show_id_by_id(ic.id)
        self.db.add(ic)
        self.db.commit()

        if kwargs.get('parent_id') == '0':
            full_parent_id = '/'+str(ic.id)+'/'
        else:
            parent_category = self.db.query(ItemCategory).filter(ItemCategory.deleted == 0,ItemCategory.id == kwargs.get('parent_id')).scalar()
            if parent_category.full_parent_id.endswith('/'):
                full_parent_id = parent_category.full_parent_id + str(ic.id)+'/'
            else:
                full_parent_id = parent_category.full_parent_id + '/'+ str(ic.id)+'/'
        self.update_item_category(ic.id,full_parent_id=full_parent_id)
        lst = full_parent_id.split('/')
        while '' in lst:
            lst.remove('')
        self.update_item_category(ic.id,level=len(lst))

        return ic

    def query_item_category(self,**kwargs):
        '''
        todo:查询商品分类
        :param kwargs:
        :return:
        '''
        query = self.rdb.query(ItemCategory).filter(ItemCategory.deleted == 0)
        if kwargs.get('category_name'):
            query = query.filter(ItemCategory.name.like("%"+kwargs.get('category_name')+"%"))
        if kwargs.has_key('category_id'):
            query = query.filter(ItemCategory.id == kwargs.get('category_id'))
        if kwargs.has_key('id'):
            query = query.filter(ItemCategory.parent_id == kwargs.get('id'))
        return query

    def get_show_id_by_category_id(self,category_id):
        '''
        根据类目id获取对应的showid
        :param category_id:
        :return:
        '''
        qurey = self.rdb.query(ItemCategory.show_id).filter(ItemCategory.id == category_id).scalar()
        return qurey

    def get_items_by_show_ids(self,show_ids):
        return self.rdb.query(ItemDetail).filter(ItemDetail.deleted == 0,
                                                  ItemDetail.show_id.in_(show_ids))

    def get_items_by_category_id(self,category_id,brand_id,catindex,item_ids,sortfield,is_desc):
        '''
        根据类目获取商品详细信息
        :param category_id: 商品类目id
        :param brand_id:品牌id
        :param item_ids:商品ID
        :param sortfield:商品排序值，0人气（根据pv字段） 1销售 2价格（price字段） 默认为0
        :return: list
        '''
        query = self.rdb.query(ItemDetail).filter(ItemDetail.deleted == 0,ItemDetail.category_id == category_id,ItemDetail.is_online==True)
        if brand_id!='0':
            query = query.filter(ItemDetail.brand_id == int(brand_id))
        if catindex!='0':
            query = query.filter(ItemDetail.id.in_(item_ids))
        if sortfield==0 or sortfield==1:
            query = query.order_by('pv  '+is_desc+'')
        else:
            query = query.order_by('price   '+is_desc+'')
        return query

    def items_like_search(self,input):
        '''
        商品模糊匹配
        :param input:
        :return:
        '''
        return self.rdb.query(ItemDetail).filter(ItemDetail.deleted == 0,ItemDetail.title.like("%"+input+"%"))

    def update_item_category(self,ic_id,**kwargs):
        '''
        todo:更新商品分类
        :param id:
        :param kwargs:
        :return:
        '''
        query = self.db.query(ItemCategory).filter(ItemCategory.deleted == 0,ItemCategory.id == ic_id)
        query.update(kwargs)
        self.db.commit()

    def update_item_category_show_id(self,id,show_id):
        '''
        设置类目的showid
        :param id: 类目的真实id
        :param show_id:类目showId
        :return:
        '''
        query = self.db.query(ItemCategory).filter(ItemCategory.deleted == 0,ItemCategory.id == id)
        query.update({'show_id':show_id})
        self.db.commit()
        return True

    def get_categorys_by_id(self,id):
        qurey = self.rdb.query(ItemCategory).filter(ItemCategory.parent_id == id,ItemCategory.deleted==0)
        return qurey

    def update_item_detail_show_id_by_id(self,id, show_id):
        '''
        设置商品详情的showid
        :param id: 类目的真实id
        :param show_id:类目showId
        :return:
        '''
        query = self.db.query(ItemDetail).filter(ItemDetail.deleted == 0,ItemDetail.id == id)
        query.update({'show_id':show_id})
        self.db.commit()
        return True

    def _children(self,paren_id):
        '''
        返回孩子节点
        :param paren_id:
        :return:
        '''
        return self.rdb.query(ItemCategory).filter(ItemCategory.deleted==0,ItemCategory.parent_id==paren_id)

    def query_by_level(self,level):
        '''
        根据层级查询
        :param level:
        :return:
        '''
        return self.rdb.query(ItemCategory).filter(ItemCategory.deleted == 0,ItemCategory.level==level)


    def _add(self,*args,**kwargs):

        data={}
        attr_keys = ['item_no','name','category_id','title','summary','props_name','orgin_price','price','drp_min_price',\
                    'content','start_time','end_time','item_tags','vendor_id','product_keywords','brand','brand_id',
                     'quantity','sale_quantity','warning_quantity','min_limit_quantity','max_limit_quantity',
                    'seo_title','seo_keywords','seo_description','unit','amount','standard','drp_max_price','is_online']
        for key in attr_keys:
            data[key] = kwargs.get(key)
        img_obj = kwargs.get('imgs_url',None)
        if img_obj:
            if isinstance(img_obj,list):
                data['main_pic'] = ';'.join(img_obj)
            else:
                data['main_pic'] = img_obj

        if 'is_drp_item' in kwargs:
            data['is_drp_item'] = kwargs.get('is_drp_item')
        if 'drp_user_id' in kwargs:
            data['drp_user_id'] = kwargs.get('drp_user_id')

        full_parent_id = self.db.query(ItemCategory.full_parent_id).filter(ItemCategory.id==kwargs.get('category_id')).scalar()
        if full_parent_id:
            data['top_category_id'] = full_parent_id.split('/')[1]
        item = self.db.execute(
            ItemDetail.__table__.insert(),[data])
        self.db.flush()
        self.db.commit()
        return item.inserted_primary_key[0]

    def _list(self,**kwargs):
        '''
        查询列表
        :param kwargs:
        :return:
        '''
        query = self.rdb.query(ItemDetail).filter(ItemDetail.deleted==0)

        if kwargs.get('id'):
            query = query.filter(ItemDetail.id == kwargs.get('id'))

        if kwargs.has_key('is_online'):
            query = query.filter(ItemDetail.is_online == kwargs.get('is_online'))

        cids=[]
        if kwargs.has_key('category_id'):
            if self.rdb.query(ItemCategory).filter(ItemCategory.deleted==0,ItemCategory.parent_id==kwargs.get('category_id')).count()>0:
                category_ids = self.rdb.query(ItemCategory.id).filter(ItemCategory.deleted==0,ItemCategory.parent_id==kwargs.get('category_id'))
                for c in category_ids:
                    cids.append(c[0])
        cids.append(kwargs.get('category_id'))
        query=query.filter(ItemDetail.category_id.in_(cids))
            #query = query.filter(ItemDetail.category_id==kwargs.get('category_id'))
        if kwargs.get('brand'):
            query = query.filter(ItemDetail.brand==kwargs.get('brand'))
        if kwargs.has_key('order_by'):
            query = query.order_by(kwargs.get('order_by'))
        else:
            query = query.order_by('gmt_created desc')
        return query

    def _delete(self,item_id):
        '''
        删除商品
        :param item_id:
        :return:
        '''
        self.db.query(ItemDetail).filter(ItemDetail.id==item_id,ItemDetail.is_online==False).update({'deleted':1},synchronize_session=False)
        # self.db.query(ItemPic).filter(ItemPic.item_id==item_id).update({'deleted':1},synchronize_session=False)


    def get_by_id(self,item_id,online=None):
        '''
        根据ID查询商品
        :param item_id:
        :return:
        '''
        query = self.rdb.query(ItemDetail).filter(ItemDetail.deleted==0,ItemDetail.is_online==True,ItemDetail.id==item_id)#.scalar()
        if online:
            query = query.filter(ItemDetail.is_online==online)
            
        return query.scalar()

    def query_by_ids(self,item_ids):
        '''
        购物车根据ID查询
        :param item_ids:
        :param kwargs:
        :return:
        '''
        query = self.rdb.query(ItemDetail).filter(ItemDetail.deleted==0,ItemDetail.is_online==True,ItemDetail.id.in_(item_ids))
        return query


    def _update_item_detail(self,item_id,**kwargs):
        '''
        todo:更新产品
        :param item_id:
        :param kwargs:
        :return:
        '''

        query = self.db.query(ItemDetail).filter(ItemDetail.deleted == 0,ItemDetail.id == item_id)
        query.update(kwargs)
        self.db.commit()

    # def _add_item_images(self,item_id,imgs):
    #
    #     index=0
    #     for url,id in imgs:
    #         pic = {}
    #         pic['item_id'] = item_id
    #         pic['pic_url'] = item_id
    #         pic['item_id'] = item_id
    #
    # item_id = Column(Integer,doc='商品ID')              #商品id
    # pic_url = Column(String(256),doc='图片URL')
    # sort = Column(SmallInteger,doc='排序')

    def _add_merchant(self,**kwargs):
        '''
        todo:添加供货商
        :param kwargs:
        :return:
        '''
        merchant = Merchant()
        merchant.name = kwargs.get('name','')
        merchant.address = kwargs.get('address','')
        merchant.contact = kwargs.get('contact','')
        merchant.phone = kwargs.get('phone','')
        merchant.remark = kwargs.get('remark','')

        self.db.add(merchant)
        self.db.commit()

        return merchant

    def _update_merchant(self,merchant_id,**kwargs):
        '''
        todo:更新供应商信息
        :param merchant_id:
        :param kwargs:
        :return:
        '''
        query = self.db.query(Merchant).filter(Merchant.Fdeleted == 0,Merchant.id == merchant_id)
        query.update(kwargs)

        self.db.commit()

    def _list_merchant(self):
        '''
        todo:查询供应商
        :param kwargs:
        :return:
        '''
        return self.rdb.query(Merchant).filter(Merchant.deleted == 0)


    def detail_side_query_by_category_id(self,category_id):
        '''
        detail页面侧边栏推荐查询
        :param category_id:
        :return:
        '''
        query = self.rdb.query(ItemDetail).filter(ItemDetail.deleted==0,ItemDetail.is_online==True,ItemDetail.category_id==category_id)
        buy_query = query.order_by(ItemDetail.comments.desc())
        view_query = query.order_by(ItemDetail.pv.desc())
        return buy_query.limit(6).offset(0),view_query.limit(6).offset(0)


    def update_item_pv(self,item_id,pv):
        '''
        更新浏览次数
        :param item_id:
        :param pv:
        :return:
        '''
        item = self.db.query(ItemDetail).filter(ItemDetail.id==item_id).scalar()
        item.pv = item.pv+pv
        self.db.add(item)
        self.db.commit()

    def qyery_category_by_level(self,level=None):
        '''
        根据类目登录查询
        :param level:
        :return:
        '''
        categories = self.rdb.query(ItemCategory.id,ItemCategory.name).filter(ItemCategory.deleted==0)
        if level:
            categories = categories.filter(ItemCategory.level==level)
        return categories


    def get_last_items_by_category_id(self,category_id,order_by=None,having=None):
        '''
        根据类目ID查询最新的商品
        :param category_id:
        :return:
        '''
        query = self.rdb.query(ItemDetail).filter(ItemDetail.deleted==0,ItemDetail.top_category_id==category_id,ItemDetail.is_online==True)
        if having:
            query = query.having((ItemDetail.sale_quantity-ItemDetail.warning_quantity)>1)
        if order_by:
            query = query.order_by(order_by)
        else:
            query = query.order_by('gmt_modified desc')
        return query

    def update_item_stock(self,items,operation='plus'):
        '''
        更新可卖库存
        :param items:
        :return:
        '''
        if operation=='plus':
            sql_format = 'update item_detail set sale_quantity=(sale_quantity+{0}) where id={1};'
        else:
            sql_format = 'update item_detail set sale_quantity=(sale_quantity-{0}) where id={1};'
        sqls=[]
        for item in items:
            item_id = item.id
            sale_amount = item.num
            excute_sql = sql_format.format(sale_amount,item_id)
            sqls.append(excute_sql)
        self.db.execute(''.join(sqls))
        self.db.commit()

    def _list_unit(self,**kwargs):
        '''
        todo:获取商品单位
        :param kwargs:
        :return:
        '''
        query = self.rdb.query(Unit).filter(Unit.deleted == 0)
        return query

    def query_items_detail(self,**kwargs):
        '''
        todo:查询商品
        :param kwargs:
        :return:
        '''
        query = self.rdb.query(ItemDetail).filter(ItemDetail.deleted == 0,ItemDetail.is_drp_item == kwargs.get('is_drp_item'))
        if kwargs.get('is_online'):
            query = query.filter(ItemDetail.is_online == int(kwargs.get('is_online')))
        if kwargs.get('category_id'):
            item_category_id = self.rdb.query(ItemCategory.id).filter(ItemCategory.deleted == 0,ItemCategory.id == kwargs.get('category_id')).scalar()
            if self.rdb.query(ItemCategory).filter(ItemCategory.deleted == 0,ItemCategory.parent_id == item_category_id).count()>0:
                query = query.filter(ItemDetail.category_id.in_(self.rdb.query(ItemCategory.id).filter(ItemCategory.parent_id == item_category_id)))
            else:
                query = query.filter(ItemDetail.category_id == item_category_id)
        if kwargs.get('is_abroad'):
            query = query.filter(ItemDetail.is_abroad==kwargs.get('is_abroad'))

        if kwargs.get('content'):
            content = kwargs.get('content')
            query = query.filter(or_(ItemDetail.item_no==content,ItemDetail.title.like("%"+content+"%")))
        return query

    def get_category_name_by_id(self,category_id):
        '''
        查询类目名称
        :param category_id:
        :return:
        '''
        return self.rdb.query(ItemCategory).filter(ItemCategory.id==category_id).scalar()

    def get_itemDetail_by_id(self,item_id):
        '''
        todo:
        :param item_detai_id:
        :return:
        '''
        return self.rdb.query(ItemDetail).filter(ItemDetail.deleted == 0,ItemDetail.id == item_id).scalar()

    def get_comments_count_by_item_id(self,item_id):
        '''
        获取商品的评论个数
        :param item_id:
        :return:
        '''
        return self.rdb.query(ItemComment).filter(ItemComment.deleted==0,ItemComment.item_id==item_id).count()

    #     return self.rdb.query(WareHouse.is_abroad).filter(WareHouse.deleted == 0,WareHouse.id == house_id).scalar()


    def query_drp_sales_items(self,drp_user_id,status=None,item_id=None,drp_item_id=None):
        '''
        分销商查询商品
        :param drp_user_id: 分销商ID
        :param status: 分销状态
        :return:
        '''
        query = self.rdb.query(DrpTraderItems,ItemDetail).filter(DrpTraderItems.deleted == 0,DrpTraderItems.item_id==ItemDetail.id,DrpTraderItems.drp_trader_id==drp_user_id,ItemDetail.deleted == 0,ItemDetail.is_online == True,ItemDetail.is_drp_item == 0)
        if status!=None:
            query = query.filter(DrpTraderItems.status==status)
        if item_id:
            query = query.filter(ItemDetail.id==item_id)
        if drp_item_id:
            query = query.filter(DrpTraderItems.id==drp_item_id)
        return query

    def add_drpTraderItems(self,item_id,drp_trader_id,item_price,status):
        '''
        分销商关联表
        :param item_id:
        :param drp_trader_id:
        :param item_price:
        :param status:
        :return:
        '''
        drp = self.db.query(DrpTraderItems).filter(DrpTraderItems.drp_trader_id==drp_trader_id,DrpTraderItems.item_id == item_id).scalar()
        if not drp:
            drp = DrpTraderItems()
        else:
            drp.deleted = 0
        drp.item_id = item_id
        drp.drp_trader_id = drp_trader_id
        drp.item_price = item_price
        drp.status = status
        self.db.add(drp)
        self.db.commit()
        return True

    def get_distributors_by_item_id(self,item_id):
        '''
        获取该商品下的所有分销商
        :param item_id: 商品id
        :return:
        '''
        return self.rdb.query(DrpTraderItems.drp_trader_id).filter(DrpTraderItems.item_id==item_id,DrpTraderItems.deleted == 0).all()

    def get_drpTraderItems_by_id(self,drp_trader_id,item_id):
        '''
        :param id: 主键id
        :return:
        '''
        return self.rdb.query(DrpTraderItems).filter(DrpTraderItems.drp_trader_id==drp_trader_id,DrpTraderItems.item_id==item_id).scalar()

    def get_exist_drp_ids(self,item_id):
        '''
        todo:
        :param item_id:
        :return:
        '''
        return self.rdb.query(DrpTraderItems.drp_trader_id).filter(DrpTraderItems.deleted == 0,DrpTraderItems.item_id == item_id)

    def delete_drp_id(self,drp_id,item_id):
        '''
        todo:
        :param drp_id:
        :param item_id:
        :return:
        '''
        self.db.query(DrpTraderItems).filter(DrpTraderItems.deleted == 0,DrpTraderItems.item_id == item_id,DrpTraderItems.drp_trader_id == drp_id).update({'deleted':1},synchronize_session=False)
        self.db.commit()

    def get_drpTraderItems_by_user_id(self,drp_user_id,category_id=None):
        '''
        todo:获取分销商下的分销商品
        :param drp_user_id:
        :return:
        '''
        query = self.rdb.query(DrpTraderItems.item_id,DrpTraderItems.item_price,
                                                    ItemDetail.show_id,ItemDetail.title,ItemDetail.main_pic,
                                                    ItemDetail.sale_quantity,ItemDetail.warning_quantity,ItemDetail.category_id).\
                                                    outerjoin(ItemDetail,DrpTraderItems.item_id == ItemDetail.id).\
                                                    filter(DrpTraderItems.deleted == 0,DrpTraderItems.status == 1,DrpTraderItems.drp_trader_id == drp_user_id,ItemDetail.deleted == 0,ItemDetail.is_online == True)

        if category_id:
            if self.rdb.query(ItemCategory).filter(ItemCategory.deleted == 0,ItemCategory.parent_id == category_id).count()>0:

                category_ids = self.rdb.query(ItemCategory.id).filter(ItemCategory.parent_id == category_id)

                query = query.filter(ItemDetail.category_id.in_(category_ids))
            else:
                query = query.filter(ItemDetail.category_id == category_id)
        return query

    def query_drp_min_price_by_id(self,item_id):
        '''
        todo:获取商品的最低分销价格
        :param item_id:
        :return:
        '''
        return self.rdb.query(ItemDetail.drp_min_price).filter(ItemDetail.deleted == 0,ItemDetail.id == item_id).scalar()

    def get_items_by_drp_id(self,drp_user_id):
        '''
        todo:查询分销商自主商品
        :param drp_user_id:
        :return:
        '''
        return self.rdb.query(ItemDetail).filter(ItemDetail.deleted == 0,ItemDetail.drp_user_id == drp_user_id)

    def _update_drpItem_by_id(self,drp_user_id,drp_item_id,**kwargs):
        '''
        todo:
        :param drp_user_id:
        :param drp_item_id:
        :return:
        '''
        query = self.db.query(DrpTraderItems).\
            filter(DrpTraderItems.deleted == 0,DrpTraderItems.drp_trader_id == drp_user_id,DrpTraderItems.item_id == drp_item_id)
        query.update(kwargs)
        self.db.commit()

    def query_by_vendorIds(self,item_ids,vendor_id):
        '''
        todo:根据供应商获取商品
        :param item_ids:
        :param vendor_id:
        :return:
        '''
        return self.rdb.query(ItemDetail).filter(ItemDetail.deleted == 0,ItemDetail.vendor_id == vendor_id,ItemDetail.id.in_(item_ids))

