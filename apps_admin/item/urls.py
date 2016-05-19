#encoding:utf-8
__author__ = 'wangjinkuan'

from tornado.web import url
from item_handler import *

#类目管理
_handlers = [
    url(r'/admin/item/category',CategoryHandler,name='item_category'),
    url(r'/admin/category/tree/([\w\W]*)',TreeHandler,name='tree'),
    url(r'/admin/category/search',ItemCategorySearchHandler,name='category_search'),
    url(r'/admin/category/([\w\W]*)',ItemCategoryHandler,name='category'),

]

#商品管理
from product_handler import *
_handlers.extend([
         url(r'/admin/items/query/ajax/',ItemsAjaxHandler,name='items_query_ajax'),
         url(r'/admin/items/search/',ItemsSearchHandler,name='items_search'),
         url(r'/admin/items/([\w\W]*)',ItemsHandler,name='items'),
         url(r'/admin/mobile/items/([\w\W]*)',ItemsHandler,name='admin_mobile_items')
    ]
)

#品牌管理
from brand_handler import *
_handlers.extend([
    url(r'/admin/brand/([\w\W]*)', BrandHandler,name='brand'),
    url(r'/admin/category_brand',CategoryBrandHandler,name='category_brand')

])

#商品属性管理
from attribute_handler import *
_handlers.extend([
    url(r'/admin/product/attribute/([\d]*)/([\d]*)/([\w\W]*)',ProductAttributeHandler,name='product_attribute'),
    url(r'/admin/product/attributes/list/([\w\W]*)',ListAttributeHandler,name='product_attribute_list')
])

#保税仓管理
from marchant_handler import *
_handlers.extend([
    url(r'/admin/vendor/([\w\W]*)',VendorHandler,name='vendor')
])

