#encoding:utf-8
__author__ = 'binpo'

from common.base_handler import AdminBaseHandler
from services.sites.nav_services import NavServices
from services.item.item_services import ItemService
from models.item_do import ItemCategory
from models.site_do import SiteNav
from utils.cache_manager import MemcacheManager

nav_service = NavServices()
item_service = ItemService()
class NavHandler(AdminBaseHandler):

    def get(self,*args, **kwargs):
        operation = self.get_argument('operation','list')
        if operation and operation == 'add':
            categories = self.rdb.query(ItemCategory).filter(ItemCategory.deleted == 0,ItemCategory.parent_id=='0')
            self.echo('admin/site/add_nav.html',{'categories':categories,'site_nav':None})
        elif operation and operation == 'edit':
            categories = self.rdb.query(ItemCategory).filter(ItemCategory.deleted == 0,ItemCategory.parent_id=='0')
            site_nav = self.rdb.query(SiteNav).filter(SiteNav.deleted==0,SiteNav.id==self.get_argument('nav_id',0)).scalar()
            self.echo('admin/site/add_nav.html',{'categories':categories,'site_nav':site_nav})
        else:
            nav_service.set_rdb(self.rdb)
            navs = nav_service.query_all()
            self.echo('admin/site/nav_list.html',{'navs':navs})

    def post(self, *args, **kwargs):
        self.get_paras_dict()
        category_id = self.qdict.get('category_id')
        item_service.set_rdb(self.rdb)
        show_id = item_service.get_show_id_by_category_id(category_id)
        nav_service.set_db(self.db)
        nav_service._update(self.qdict.get('name',''),self.qdict.get('category_id'),show_id,
                            self.qdict.get('link'),self.qdict.get('enable',1),
                            self.qdict.get('sort'),
                            self.qdict.get('open_type'),
                            self.qdict.get('app_start'),
                            nav_id=self.qdict.get('nav_id'))
        MemcacheManager().get_conn().delete('site_nav_html')
        self.write('菜单更新成功')

    def delete(self):
        nav_id = self.get_argument('nav_id')
        self.db.query(SiteNav).filter(SiteNav.deleted==0,SiteNav.id==nav_id).delete(synchronize_session=False)
            #.update({'deleted':1},synchronize_session=False)
        self.db.commit()
        MemcacheManager().get_conn().delete('site_nav_html')
        self.write_json({'status':200,'info':'操作成功'})

class LinkHandler(AdminBaseHandler):

    def get(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        pass

from tornado.options import define
class ConfHandler(AdminBaseHandler):

    def get(self):

        config = {}
        execfile('web_conf.conf', config, config)
        config.pop('__builtins__')
        import setting
        setting_data = setting.__dict__
        setting_data.pop('__builtins__')
        #for name in config:

        self.echo('admin/site/conf_list.html',{'confs':config,'settings':setting_data})
