#encoding:utf-8
__author__ = 'binpo'
#
# import requests
# exit()
from models.syncdb import init_site_data
init_site_data()
from models.cities.cities import init_cities
init_cities()
