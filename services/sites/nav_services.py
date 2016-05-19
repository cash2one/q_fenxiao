#encoding:utf-8
__author__ = 'binpo'

from services.base_services import BaseService
from models.site_do import SiteNav

class NavServices(BaseService):

    def query_all(self,**kargs):
        query = self.rdb.query(SiteNav).filter(SiteNav.deleted==0).order_by('sort')
        if kargs.has_key('is_app_start'):
            query = query.filter(SiteNav.is_app_start == kargs.get('is_app_start'))
        return query

    def _update(self,name,category_id,show_id,link,enable,sort,open_type,is_app_start,nav_id=None):
        '''
        更新一级菜单导航
        :param name:名称
        :param category_id:以及类目名称
        :param link:连接
        :param enable:是否可用
        :param sort:排序
        :param open_type:打开方式
        :param nav_id:连接ID
        :return:
        '''
        if nav_id:
            site_nav = self.db.query(SiteNav).filter(SiteNav.deleted==0,SiteNav.id==nav_id).scalar()
            if not site_nav:
                site_nav = SiteNav()
        else:site_nav = SiteNav()

        site_nav.name = name
        site_nav.category_id = category_id
        site_nav.show_id = show_id
        site_nav.link = link
        site_nav.enable = enable
        site_nav.sort = sort
        site_nav.open_type = open_type
        site_nav.is_app_start = is_app_start
        self.db.add(site_nav)
        self.db.commit()



