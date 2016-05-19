#encoding:utf-8
__author__ = 'gaoaifei'

from common.base_handler import BaseHandler
import pyes

conn = pyes.ES('127.0.0.1:9200')#连接
INDEX_NAME = 'test_index'
DOC_TYPE = 'test_type'
class ElasticsearchHandler(BaseHandler):

    def get(self, *args, **kwargs):
        '''
        搜索
        :param args:
        :param kwargs:
        :return:
        '''
        searchkey = self.get_argument('key')
        qtitle = pyes.TextQuery('title',searchkey)
        qcontent = pyes.TextQuery('desc', searchkey)
        h = pyes.HighLighter(['<b>'], ['</b>'], fragment_size=20)
        #多字段搜索(must=>and,should=>or)，高亮，结果截取（分页），排序
        q = pyes.Query.search(pyes.BoolQuery(should=[qtitle,qcontent]), highlight=h, start=0, size=3, sort={'id': {'order': 'asc'}})
        q.add_highlight("title")
        q.add_highlight("desc")
        results = conn.search(query = q, indices=[INDEX_NAME], doc_types=["test-type1"])
        print results.count
        print type(results)
        print dir(results)
        list = []
        for r in results:
            print r
        #     if(r._meta.highlight.has_key("title")):
        #         r['title']=r._meta.highlight[u"title"][0]
        #     if(r._meta.highlight.has_key("desc")):
        #         r['desc']=r._meta.highlight[u"desc"][0]
        #     list.append(r)
        # print list
        # self.echo('index.html',{'list':list,'count':results.total})

    def post(self, *args, **kwargs):
        '''
        创建搜索索引
        :param args:
        :param kwargs:
        :return:
        '''
        data = self.get_argument('data')
        conn.indices.create_index_if_missing(INDEX_NAME)#创建一个test_index的索引 test_index类似一个数据库
        #定义索引存储结构
        mapping = {
             u'id': {'boost': 1.0,
                          'index': 'not_analyzed',#no not_an an..
                          'store': 'yes',
                          'type': u'string',
                          "term_vector" : "with_positions_offsets"},
             u'category_id': {'boost': 1.0,
                         'index': 'not_analyzed',
                         'store': 'no',
                         'type': u'integer'},
             u'title': {'boost': 1.0,
                         'index': 'analyzed',
                         'store': 'yes',
                         'type': u'string',
                         'analyzer':'mmseg_maxword',
                         "term_vector": "with_positions_offsets"},
             u'desc': {'boost': 1.0,
                        'index': 'analyzed',
                        'store': 'yes',
                        'type': u'integer',
                        'analyzer':'mmseg_maxword',
                        "term_vector": "with_positions_offsets"},
             u'brand_id':{
                        'boost':1.0,
                        'index':'not_analyzed',
                        'store':'no',
                        'type':u'integer'}
        }
        conn.put_mapping("test-type1", {'properties':mapping}, [INDEX_NAME])#定义test-type
        conn.put_mapping("test-type2", {"_parent" : {"type" : "test-type1"}}, [INDEX_NAME])#从test-type继承
        #插入索引数据
        conn.index(data,INDEX_NAME,"test-type1")
        conn.default_indices=[INDEX_NAME]#设置默认的索引
        conn.refresh()#刷新以获得最新插入的文档
        return True