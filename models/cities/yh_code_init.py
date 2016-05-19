#encoding:utf-8
__author__ = 'binpo'


from sqlalchemy import create_engine, MetaData,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from models.base_do import Base
from models.location_do import Country,Province,City,Area


mysql_engine = create_engine('mysql://root:111111@127.0.0.1:3306/haitao?charset=utf8',encoding = "utf-8",echo =True)
#Base.metadata.drop_all(mysql_engine)
#Base.metadata.create_all(mysql_engine)  #建表
Session = sessionmaker(bind=mysql_engine)
session = Session()

def syn_yuhua_code():
    f = open('areas.txt','r')
    content = f.readline()

    while content:
        print content
        print content.split()
        print '--------------'

        tmp = content.split()

        if not tmp:
            content = f.readline()
            continue
        code = tmp[0].strip()
        name = tmp[1].strip()
        print name
        try:
            province = session.query(Province).filter(Province.name==name).scalar()
            if province:
                province.yh_code=code
                session.add(province)
            else:
                city = session.query(City).filter(City.name==name).scalar()
                if city:
                    city.yh_code=code
                    session.add(city)
                else:
                    area = session.query(Area).filter(Area.name==name).scalar()
                    if area:
                        area.yh_code =code
                        session.add(area)
            session.commit()
        except:
            pass

        content = f.readline()

    print '初始化完成'