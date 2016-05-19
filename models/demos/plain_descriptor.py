__author__ = 'binpo'

from models.base_do import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import column_property
from ..demos import session


from sqlalchemy.orm import object_session
from sqlalchemy import select, func

class Address(Base):
    __tablename__ = 'user_address'

    user_id = Column(Integer)
    name = Column(String(64),doc='名称')
    code = Column(String(32),doc='身份证号')
    phone = Column(String(31),doc='电话')

class User(Base):

    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    firstname = Column(String(50))
    lastname = Column(String(50))

    @property
    def address(self):
        return object_session(self).scalar(
                select(Address.name).where(Address.user_id==self.id)
            )
