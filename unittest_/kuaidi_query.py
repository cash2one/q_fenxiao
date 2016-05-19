#encoding:utf-8
__author__ = 'binpo'
import urllib,urllib2
# url = "http://www.kuaidi100.com/applyurl?key={0}&com={1}&nu={2}"
# requersurl = url.format('a723c34b5c963ff8','yuantong','801635828522')
# r = urllib2.urlopen(requersurl)
# content = r.read()
# print content
import ujson

# url2="http://www.kuaidi100.com/query?id=1&type=yuantong&postid=801635828522"
#
# r = urllib2.urlopen(url2)
# content = r.read()
# da = ujson.loads(content)
# print da
# #
# #
url2="http://www.kuaidi100.com/query?type=yuantong&postid=804968610412&id=1&valicode=&temp=0.08133630105294287"
r = urllib2.urlopen(url2)
content = r.read()
da = ujson.loads(content)
print da

# url2='http://api.kuaidi100.com/api?id=a723c34b5c963ff8&com=yuantong&nu=804968611498&show=0&muti=1&order=desc'
# r = urllib2.urlopen(url2)
# content = r.read()
# da = ujson.loads(content)
# print da
#
#
# import urllib2
# req = urllib2.Request('http://www.kuaidi100.com/')
# req.add_header('Referer', 'http://www.kuaidi100.com/')
# req.add_header('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:42.0) Gecko/20100101 Firefox/42.0')
# req.add_header('X-Requested-With','XMLHttpRequest')
# url2="http://www.kuaidi100.com/query?type=yuantong&postid=804968611498&id=1"

# url2='http://m.kuaidi100.com/query?type=yuantong&postid=804968612400&id=1&valicode=&temp=0.8341054425101049'
# r = urllib2.urlopen(url2)
# content = r.read()
# da = ujson.loads(content)
# print da

url2 = 'http://www.aikuaidi.cn/rest/?key=418fa3b65b0646d1a6912759ebfee653&order=804968610984&id=yuantong&ord=desc&show=json'
r = urllib2.urlopen(url2)
content = r.read()
da = ujson.loads(content)
print da


url2 = 'http://www.aikuaidi.cn/rest/?key=418fa3b65b0646d1a6912759ebfee653&order=804968611498&id=yuantong&ord=desc&show=json'
r = urllib2.urlopen(url2)
content = r.read()
da = ujson.loads(content)
print da



url2 = 'http://www.aikuaidi.cn/rest/?key=418fa3b65b0646d1a6912759ebfee653&order=8049686114981&id=yuantong&ord=desc&show=json'
r = urllib2.urlopen(url2)
content = r.read()
da = ujson.loads(content)
print da
print da.get('status')==1