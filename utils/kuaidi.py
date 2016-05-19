#encoding:utf-8
__author__ = 'binpo'
import urllib2
def kuaidi_query(company_code,num):
    _url = "http://www.kuaidi100.com/query?id=1&type={0}&postid={1}"
    _url = _url.format(company_code,num)
    r = urllib2.urlopen(_url)
    content = r.read()
    return content

def kuaidi_query_2(company_code,num):
    _url = 'http://www.aikuaidi.cn/rest/?key=418fa3b65b0646d1a6912759ebfee653&order={1}&id={0}&ord=desc&show=json'
    _url = _url.format(company_code,num)
    r = urllib2.urlopen(_url)
    content = r.read()
    return content