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

def init_cities():
    from lxml import etree#导入lxml库
    tree = etree.parse("Provinces.xml")#将xml解析为树结构
    root = tree.getroot()#获得该树的树根
    for article in root:#这样便可以遍历根元素的所有子元素(这里是article元素)

        id = article.get('id')
        province_name = article.get('ProvinceName')
        province = Province()
        province.province_id = id
        province.name = province_name
        session.add(province)
        session.commit()


    tree = etree.parse("Cities.xml")#将xml解析为树结构
    cities = tree.getroot()#获得该树的树根
    for city in cities:
        #ID="1" CityName="北京市" PID="1" ZipCode="100000
        id = city.get('ID')
        cityname = city.get('CityName')
        pid = city.get('PID')
        zipcode = city.get('ZipCode')

        city = City()
        city.city_id = id
        city.name = cityname
        city.father = pid
        city.zip_code = zipcode
        session.add(city)
        session.commit()


    tree = etree.parse("Districts.xml")#将xml解析为树结构
    districts = tree.getroot()#获得该树的树根
    for district in districts:
        #ID="1" DistrictName="东城区" CID="1"
        id = district.get('id')
        DistrictName = district.get('DistrictName')
        CID = district.get('CID')
        area = Area()
        area.area_id = id
        area.name = DistrictName
        area.father = CID
        session.add(area)
        session.commit()


# class Area(Base):
#     """
#         区域信息
#     """
#     __tablename__ = 'area'
#
#     id = Column(Integer, primary_key=True)
#     area_id = Column(Integer)
#     area_name = Column(String(128))                 #区域名称
#     father = Column(Integer)
#     gmt_created = Column(DateTime)
#     gmt_modified = Column(DateTime)
#     deleted = Column(Boolean)
#
#     def to_dict(self):
#         dic = {}
#         dic["area_id"] = self.area_id
#         dic["city_id"] = self.father
#         dic["area_name"] = self.area_name
#         return dic
    # print "元素名称：",article.Province#用.tag得到该子元素的名称
    # for field in article:#遍历article元素的所有子元素(这里是指article的author，title，volume，year等)
    #     print field.tag,":",field.text#同样地，用.tag可以得到元素的名称，而.text可以得到元素的内容
    # mdate=article.get("mdate")#用.get("属性名")可以得到article元素相应属性的值
    # key=article.get("key")
    # print "mdate:",mdate
    # print "key",key
    # print ""#隔行分开不同的article元素

#
from yh_code_init import syn_yuhua_code
if __name__=='__main__':
    #init_cities()
    syn_yuhua_code()
#     get_tagname_other('Provinces.xml')