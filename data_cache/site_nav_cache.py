# #encoding:utf-8
# __author__ = 'binpo'
#
# from cache_base import CacheBase
# import ujson
# from services.sites.nav_services import NavServices
# from utils.cache_manager import MemcacheManager
# import tornado.web
# conn = MemcacheManager().get_conn()
# class SiteNav(CacheBase,tornado.web.RequestHandler):
#
#     def get_site_nav(self):
#         sit_nav_html = self.mcache.get('site_nav_html')
#         if not sit_nav_html:
#             nav_service = NavServices(rdb=self.db)
#             navs = nav_service.query_all()
#             content= self.render('include/cache_nav.html',{'navs':navs})
#             conn.set('site_nav_html',content,7*24*36)
#         return sit_nav_html
#
#     def update_site_nav_cache(self):
#         conn.delete('site_nav_html')
#         self.get_sit_nav()
#
