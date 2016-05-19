#encoding:utf-8
__author__ = 'binpo'

from base_do import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, SmallInteger,Text,Date,Float
from sqlalchemy import event
from sqlalchemy.sql.functions import now

class Merchant(Base):

    '''供货商 '''
    __tablename__='merchant'

    name = Column(String(128),doc='供货商名称')
    account = Column(String(128),doc='供应商登陆账号')
    address = Column(String(1024),doc='供货商地址')
    contact = Column(String(128),doc='联系人')
    phone = Column(String(30),doc='电话')
    remark = Column(String(1024),doc='简要说明')


class ItemCategory(Base):

    '''商品分类'''
    __tablename__ = 'item_category'

    show_id = Column(Integer,doc='类目展示id',nullable=False,default=0)
    name = Column(String(128),nullable=False)       #类目名称
    desc = Column(String(1024),nullable=False)
    parent_id = Column(String(128),nullable=False,default=0)  #父类目
    full_parent_id = Column(String(256),default='')
    level = Column(SmallInteger,default=1)
    is_abroad = Column(Boolean,default=1,doc='是否跨境类目') #1:是  0:否

class Brand(Base):
    '''品牌表'''
    __tablename__= 'brand'
    category_id = Column(Integer)              # 类目
    name = Column(String(256),doc='品牌名称')
    description = Column(Text,doc='品牌的一些描述信息')
    sort = Column(Integer,doc="排序值")
    is_online = Column(Integer,doc="是否显示 0显示 1不显示")

class Unit(Base):

    __tablename__ = 'unit'

    code = Column(String(32),doc='代码')
    name = Column(String(32),doc='名称')

class ItemDetail(Base):
    """
    商品基本信息
    """
    __tablename__ = 'item_detail'

    show_id = Column(Integer,doc='类目展示id',nullable=False,default=0)
    item_no = Column(String(256),doc='商品序号')  # 和仓库保存一致,录入的时候人工录入
    top_category_id = Column(Integer,doc='顶级类目',nullable=False,default=0)  #顶级类目设计
    category_id = Column(Integer)              # 类目

    #--商品描述信息
    name = Column(String(60),doc='商品名称',default='')
    title = Column(String(128),doc='商品标题',default='')              # 商品标题,不能超过60字节
    summary = Column(String(1024),doc='概述,title下方显示的')
    type = Column(String(64),doc='商品型号',default='')     #商品类型 ST3000VX006
    brand = Column(String(128),doc='品牌',default='')
    brand_id = Column(Integer,doc='品牌id')              #品牌id
    features = Column(String(1024))         # 宝贝特征值  key-value
    orgin_price = Column(Float,doc='原价')           # 商品原价价格
    
    price = Column(Float,doc='零售价格')                 # 商品价格，如果有sku 以sku为主
    inner_price = Column(Float,doc='国内参考价格')        #市场参考价格
    
    drp_min_price = Column(Float,doc='分销最低价格',default=0) #分销最低价格
    drp_max_price = Column(Float,doc='分销最高价格',default=0) #分销最高价格

    main_pic = Column(String(256))          # 商品主图
    content = Column(Text,doc='商品内容')   #大部分是图片链接，因此不做分离
    #----上下架信息，（和商品数量也有关系）
    is_online = Column(Boolean,doc='是否上架')

    is_drp_item = Column(Boolean,doc='是否分销商的商品 1:是 0:否',default=0)
    drp_user_id = Column(Integer,doc='分销商ID')

    start_time = Column(DateTime)           # 上架时间 （格式：yyyy-MM-dd HH:mm:ss）
    end_time = Column(DateTime)             # 下架时间 （格式：yyyy-MM-dd HH:mm:ss）

    #----产地标签------
    item_tags = Column(String(128))         # 商品标签
    vendor_id = Column(SmallInteger,doc='供应商ID',nullable=True)

    product_keywords = Column(String(255),doc='产品关键字',default='')

    sort = Column(Integer,doc='排序')
    #----库存信息
    quantity = Column(Integer,doc='库存',default=0)
    sale_quantity = Column(Integer,doc='可卖库存',default=0)        # 可卖库存
    warning_quantity = Column(Integer,doc='预警库存',default=0)

    is_xinpin = Column(Boolean)                 #标示商品是否为新品。 值含义：true-是，false-否。
    is_second_kill = Column(Boolean)            #是否秒杀
    is_sell_promise = Column(Boolean)          #是否支持退货服务
    has_invoice = Column(Boolean,default=0)               # 是否有发票
    has_warranty = Column(Boolean,default=0)              # 是否保修
    outer_id = Column(String(60))               # 商家外部编码

    unit = Column(String(32),doc='单位名称',default='')
    amount = Column(Integer,doc='个数',default=1)#  eg:一箱方便面,6袋  子包装单位和个数
    standard = Column(String(512),doc='规格型号')

    #是否限购
    min_limit_quantity = Column(SmallInteger,doc='最少限购数量',default=1)
    max_limit_quantity = Column(SmallInteger,doc='最多限购数量',default=100)
    pv = Column(Integer,doc='访问量',default=0)
    #评价等像个信息
    comments = Column(Integer,doc='评价次数',default=0)
    collections = Column(Integer,doc='收藏次数',default=0)

    #seo信息
    seo_title = Column(String(255),doc='SEO标题')
    seo_keywords = Column(String(255),doc='SEO关键字')
    seo_description = Column(String(255),doc='SEO描述')

    #售后保障
    sale_protection = Column(Text,doc='售后保障',nullable=True,default='')

    
class DrpTraderItems(Base):
    '''
    分销商商品关联表
    '''
    __tablename__ = 'drp_trader_items'
    item_id = Column(Integer,doc='商品ID')
    drp_trader_id = Column(Integer,doc='分销商ID')
    item_price = Column(Float,doc='分销商品状态价格')
    status = Column(SmallInteger,doc='',default=0) #0：待分配价格 1：已分配可卖 2:售完下架

class ItemPic(Base):

    '''商品首图'''
    __tablename__='item_pic'

    item_id = Column(Integer,doc='商品ID')              #商品id
    pic_url = Column(String(256),doc='图片URL')
    sort = Column(SmallInteger,doc='排序')

class ItemAttribute(Base):
    """
    类目属性定义。
    """
    __tablename__ = 'item_attribute'

    attribute_name = Column(String(128),nullable=False)  #类目名称
    attribute_desc = Column(String(256),nullable=False)  #类目说明
    category_id = Column(Integer)                       #分类
    is_alais = Column(Boolean, default=False)  #是否别名
    is_color = Column(Boolean, default=False)  #是否颜色
    is_enum = Column(Boolean, default=False)  #是否别名
    is_key_att = Column(Boolean, default=False)  #是否关键属性
    is_for_seller = Column(Boolean, default=False)

    is_filter = Column(Boolean, default=False) #是否查询属性
    is_sku = Column(Boolean, default=False)    #是否SKU属性

    is_unique = Column(Boolean, default=False)
    is_multi_select = Column(Boolean, default=False)  #是否多选
    html = Column(String(256),doc='html显示属性')
    status = Column(Integer, default=0)
    paixu = Column(Integer, default=0)  #排序

    def as_dict(self):
        pass
        # return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class ItemAttributeValue(Base):
    """
    类目属性数值定义。
    """
    __tablename__ = 'item_attribute_value'

    attribute_id = Column(Integer)  #属性id
    attribute_name = Column(String(128),nullable=False)  #属性名称
    attribute_value = Column(String(1024),nullable=False)
    status = Column(Integer, default=0)
    paixu = Column(Integer, default=0)


class ItemSKU(Base):
    """
    SKU 信息
    """
    __tablename__ = 'item_sku'

    item_id = Column(Integer)  # 商品id
    item_code = Column(String(128))#库存编码
    item_name = Column(String(256),doc='SKU名称')
    item_count = Column(Integer,doc='商品库存')            # 商品数量
    sale_quantity = Column(Integer,doc='可卖库存')         # 可卖库存
    warning_quantity = Column(Integer,doc='预警库存')
    orgin_price = Column(Float)                       # 商品原价价格
    item_price = Column(Float)                        # 商品价格，
    inner_price = Column(Float,doc='国内参考价格')      # 国内参考价格

    attribute_name_id_list = Column(String(1024),doc='属性名id列表,以;分隔')
    attribute_value_id_list = Column(String(1024),doc='属性值id列表,以;分隔')
    attribute_name_list = Column(String(1024))  # 属性名称列表 ;隔开
    attribute_value_list = Column(String(1024))  # 属性值列表 如： 玉兰油;红色;200ml
    attribute_html_name = Column(String(1024))  # 属性名称 如： 玉兰油，红色，200ml  带HTML 标题时用


class ItemAttributeFilter(Base):
    """
    商品属性关系表
    """
    __tablename__ = 'item_attribute_filter'
    item_id = Column(Integer)  # 商品id
    attribute_id = Column(Integer)  #属性名称id
    attribute_value_id = Column(Integer)  #属性值id
    is_sku = Column(Boolean,doc='是否sku 0搜索 1sku',default=0)
    sku_id = Column(Integer) # sku属性表id

class ItemComment(Base):

    '''商品评价'''
    __tablename__ = 'item_comment'

    item_id = Column(Integer)                       #商品id
    order_id = Column(Integer,doc='订单ID')
    order_no = Column(String(64),doc='订单序号')
    user_id = Column(Integer,doc='用户ID')
    user_name = Column(String(32),doc='用户名',default='****')
    assess_level = Column(SmallInteger,doc='评价')  #好:2 中:1 差:0
    comment = Column(String(2048),doc='评论',default='')
    addition_comment  = Column(String(2048),doc='追加评论',default='')
    is_add_comment = Column(Boolean,doc='是否有追加评论 0无 1有',default=0)
    is_show = Column(Boolean,doc='是否晒单 1是 0无',default=0)
    show_imgs = Column(String(2014),doc='晒单图片')       #用;分割每个URL
    add_show_imgs = Column(String(2014),doc='追加晒单图片') #用;分割每个URL


class HomeRecommend(Base):
    '''首页推荐'''

    __tablename__ = 'home_recommend'

    category_id = Column(Integer,doc='分类ID')
    item_id = Column(Integer,doc='商品ID')
    start_date = Column(Date,doc='开始时间')
    end_date = Column(Date,doc='结束时间')
    sort  = Column(Integer,doc='排序')

class UserItemViews(Base):
    '''浏览记录'''

    __tablename__ = 'user_item_views'
    item_id = Column(Integer,doc='商品ID')
    item_title = Column(String(256),doc='商品标题')
    item_pic = Column(String(256),doc='商品图片')
    price = Column(Float,doc='卖价')
    inner_price = Column(Float,doc='参考价格')
    comments = Column(Integer,doc='品论次数')


@event.listens_for(ItemDetail, 'before_update')
def receive_before_update(mapper, connection, target):
    target.gmt_modified = now()


@event.listens_for(ItemComment, 'before_update')
def receive_before_update(mapper, connection, target):
    target.gmt_modified = now()