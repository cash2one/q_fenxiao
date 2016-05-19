#encoding:utf-8
__author__ = 'binpo'

from utils.singleton import Singleton
from utils.logs import LOG
from sqlalchemy import create_engine

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
# from application import MySQLPingListener
import MySQLdb
from setting import DB_HOST,DB_PORT,DB_USER,DB_PASSWD,DB_NAME,ENGINE
import traceback
log = LOG('db_excute_log')

class DbFactory(Singleton):
    def __init__(self,engine = ENGINE):
        session_factory = scoped_session(sessionmaker(bind=engine, autoflush=True, autocommit=False))
        self.session = session_factory()


    def get_session(self):
        return self.session

class DB(object):

    def __init__(self,engine=ENGINE):
        _engine = create_engine(engine)
        self.session = scoped_session(sessionmaker(bind=_engine,autoflush=True,autocommit=False))
        #self.session = Session()

    def get_session(self):
        return self.session

    def execute(self,sql):
        # self.session.begin()
        try:
            self.session.execute(sql)
            self.session.commit()
            # print 'hello world'
        except:
            log.error(traceback.format_exc())
            self.session.rollback()
        finally:
            self.db_close()
    def db_close(self):
        self.session.close()

class DbConnection(Singleton):

    def __init__(self):
        self.conn = None
        self.cur = None

    def get_conn(self):
        self.conn= MySQLdb.connect(
                host=DB_HOST,
                port = DB_PORT,
                user = DB_USER,
                passwd = DB_PASSWD,
                db = DB_NAME
                )

    def get_cur(self):
        self.cur = self.conn.cursor()

    def execution(self,sqls,args=None):
        if not self.conn:
            self.get_conn()
        if not self.cur:
            self.get_cur()
        self.conn.begin()
        try:
            for sql in sqls:
                self.cur.execute(sql)

            self.conn.commit()
        except Exception,e:
            log.error(traceback.format_exc())
            self.conn.rollback()
        finally:
            self.close_db()

    def close_db(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
    #创建数据表
    #cur.execute("create table student(id int ,name varchar(20),class varchar(30),age varchar(10))")

    #插入一条数据
    #cur.execute("insert into student values('2','Tom','3 year 2 class','9')")


    #修改查询条件的数据
    #cur.execute("update student set class='3 year 1 class' where name = 'Tom'")

    #删除查询条件的数据
    #cur.execute("delete from student where age='9'")

# sqls='''update item_detail set quantity=(quantity+10) where id=1;
# update item_detail set quantity=(quantity+20) where id=1;
# update item_detail set quantity=(quantity+1) where id=1;
# update item_detail set quantity=(quantity+1) where id=1'''
# # # db.execution(sqls)
# # # # from setting import ENGINE
# import  time
# db = DB()
# for x in xrange(10):
#     db.execute(sqls)
#     time.sleep(3)