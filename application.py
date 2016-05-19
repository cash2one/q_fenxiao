#encoding:utf-8
__author__ = 'binpo'

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from utils.cache_manager import MemcacheManager
import tornado.web
from tornado.options import options
from sqlalchemy.pool import QueuePool
from sqlalchemy.event import listens_for
import sys,os
from utils.conf_util import parse_config_file

reload(sys)
sys.setdefaultencoding('utf-8')
parse_config_file(os.path.join(os.path.dirname(__file__),'web_conf.conf'))
tornado.options.parse_command_line()

engine = create_engine(options.ENGINE,echo=False,
                                        poolclass=QueuePool,
                                       pool_size=200,
                                       max_overflow=300,
                                       pool_recycle=3600,
                                       pool_timeout=3600)

from sqlalchemy import exc
from sqlalchemy import select

@listens_for(engine, "engine_connect")
def ping_connection(connection, branch):
    if branch:
        # "branch" refers to a sub-connection of a connection,
        # we don't want to bother pinging on these.
        return
    try:
        # run a SELECT 1. use a core select() so that
        # the SELECT of a scalar value without a table is
        # appropriately formatted for the backend
        connection.scalar(select([1]))
    except exc.DBAPIError as err:
        # catch SQLAlchemy's DBAPIError, which is a wrapper
        # for the DBAPI's exception. It includes a .connection_invalidated
        # attribute which specifies if this connection is a "disconnect"
        # condition, which is based on inspection of the original exception
        # by the dialect in use.
        if err.connection_invalidated:
          # run the same SELECT again - the connection will re-validate
          # itself and establish a new connection. The disconnect detection
          # here also causes the whole connection pool to be invalidated
          # so that all stale connections are discarded.
          connection.scalar(select([1]))
        else:
            raise


class Application(tornado.web.Application):

    def __init__(self, handlers,**settings):
        #session_factory = scoped_session(sessionmaker(bind=engine, autoflush=True, autocommit=False))
        # self.db = session_factory()
        # print 'create sassion factiory'
        #self.rcache = RedisManaher().cache_con()  #redis cache conn
        self.mcache = MemcacheManager().get_conn() #memcache conn
        tornado.web.Application.__init__(self, handlers, **settings)