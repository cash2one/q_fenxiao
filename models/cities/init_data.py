#encoding:utf-8
__author__ = 'wangjinkuan'

from models.location_do import *



def parse(session,etree,file_path):
    tree = etree.parse(file_path+"Provinces.xml")#将xml解析为树结构
    root = tree.getroot()#获得该树的树根
    for article in root:#这样便可以遍历根元素的所有子元素(这里是article元素)

        id = article.get('ID')
        province_name = article.get('ProvinceName')
        province = Province()
        province.province_id = id
        province.name = province_name
        session.add(province)
        session.commit()

    tree = etree.parse(file_path+"Cities.xml")#将xml解析为树结构
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

        session.add(city)
        session.commit()

    tree = etree.parse(file_path+"Districts.xml")#将xml解析为树结构
    districts = tree.getroot()#获得该树的树根
    for district in districts:
        #ID="1" DistrictName="东城区" CID="1"
        id = district.get('ID')
        DistrictName = district.get('DistrictName')
        CID = district.get('CID')
        area = Area()
        area.area_id = id
        area.name = DistrictName
        area.father = CID
        session.add(area)
        session.commit()
