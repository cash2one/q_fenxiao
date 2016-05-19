#encoding:utf-8
__author__ = 'binpo'

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from utils.cache_manager import RedisManaher,MemcacheManager
import tornado
from tornado.options import options


class MySQLPingListener(object):

    def checkout(self, dbapi_con, con_record, con_proxy):
        from sqlalchemy.exc import DisconnectionError
        from _mysql_exceptions import OperationalError
        try:
            dbapi_con.ping()
        except OperationalError:
            raise DisconnectionError("Database server went away")

class Application(tornado.web.Application):

    def __init__(self, handlers,**settings):
        tornado.web.Application.__init__(self, handlers, **settings)
