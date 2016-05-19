#encoding:utf-8
__author__ = 'binpo'

from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base
from utils.datetime_util import datetime_format
from sqlalchemy import Table, Column, Integer, ForeignKey, String, DateTime, Boolean
from sqlalchemy.sql.functions import now
from sqlalchemy import event

class ModelMixin(object):

    id = Column(Integer, primary_key=True, doc='ID 自动增长列')
    gmt_created = Column(DateTime,default=now(),doc='创建时间')
    gmt_modified = Column(DateTime,default=now(),doc='最后更新时间')
    deleted = Column(Boolean,default=0,doc='记录状态 0 删除 1 正常')

    @classmethod
    def get_by_id(cls, session, id, columns=None, lock_mode=None):
        if hasattr(cls, 'id'):
            scalar = False
            if columns:
                if isinstance(columns, (tuple, list)):
                    query = session.query(*columns)
                else:
                    scalar = True
                    query = session.query(columns)
            else:
                query = session.query(cls)
            if lock_mode:
                query = query.with_lockmode(lock_mode)
            query = query.filter(cls.id == id)
            if scalar:
                return query.scalar()
            return query.first()
        return None

    @classmethod
    def get_all(cls, session, columns=None, offset=None, limit=None, order_by=None, lock_mode=None):
        if columns:
            if isinstance(columns, (tuple, list)):
                query = session.query(*columns)
            else:
                query = session.query(columns)
                if isinstance(columns, str):
                    query = query.select_from(cls)
        else:
            if hasattr(cls, 'deleted'):
                query = session.query(cls).filter(cls.deleted==0)
            else:
                query = session.query(cls)
        if order_by is not None:
            if isinstance(order_by, (tuple, list)):
                query = query.order_by(*order_by)
            else:
                query = query.order_by(order_by)
        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)
        if lock_mode:
            query = query.with_lockmode(lock_mode)
        return query.all()


    @classmethod
    def count_all(cls, session, lock_mode=None):
        query = session.query(func.count('*')).select_from(cls)
        if lock_mode:
            query = query.with_lockmode(lock_mode)
        return query.scalar()


    @classmethod
    def exist(cls,session,**kargs):

        query = session.query(func.count('*')).select_from(cls)
        for key in kargs.keys():
            key=kargs.get(key)
            if hasattr(cls, key):
                query = query.filter_by()
        # if hasattr(cls, 'id'):
        #    .filter(cls.id == id)
            # if lock_mode:
            #     query = query.with_lockmode(lock_mode)
        return query.scalar() > 0
        #return False

    @classmethod
    def set_attr(cls, session, id, attr, value):
        if hasattr(cls, 'id'):
            session.query(cls).filter(cls.id == id).update({
                attr: value,
                'gmt_modified':datetime_format()
            })
            session.commit()


    @classmethod
    def set_attrs(cls, session, id, **attrs):
        if hasattr(cls, 'id'):
            attrs['gmt_modified'] = datetime_format()
            session.query(cls).filter(cls.id == id).update(attrs)
            session.commit()

    def columns(self):
        return [c.name for c in self.__table__.columns]

    def to_dict(self):
        return dict([(c, getattr(self, c)) for c in self.columns()])
import sqlalchemy.types as types
class ChoiceType(types.TypeDecorator):

    impl = types.SmallInteger

    def __init__(self, choices, **kw):
        self.choices = dict(choices)
        super(ChoiceType, self).__init__(**kw)

    def process_bind_param(self, value, dialect):
        return [k for k, v in self.choices.iteritems() if v == value][0]

    def process_result_value(self, value, dialect):
        return self.choices[value]

Base = declarative_base(cls=ModelMixin)

metadata = Base.metadata

@event.listens_for(Base,'before_update')
def before_update_listener(mapper, conn, target):
    print 'update is callable '
    target.gmt_modified = now()

# @event.listens_for(ModelMixin, 'before_update')
# def receive_before_update(mapper, connection, target):
#     print 'before update eventes'
#     target.gmt_modified = now()
