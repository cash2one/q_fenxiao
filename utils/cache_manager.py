#encoding:utf-8
__author__ = 'binpo'

import redis
import sys
from setting import REDIS_HOST,REDIS_PORT,MEMCACHE_HOST,OCS_ACCESS_URL,OCS_ACCESS_ID,OCS_ACCESS_PASS

import logging
import traceback
LOG = logging.getLogger(__name__)
from utils.singleton import Singleton

# class Singleton(object):
#     def __new__(cls, *args, **kw):
#         if not hasattr(cls, '_instance'):
#             orig = super(Singleton, cls)
#             cls._instance = orig.__new__(cls, *args, **kw)
#         return cls._instance

class RedisManaher(Singleton):

    def __init__(self):
        print "Redis connection start.........."
        self.host = REDIS_HOST#'localhost'
        self.port = REDIS_PORT#6379
        self.db = 0
        pool = redis.ConnectionPool(host=self.host, port=self.port)
        self.r = redis.Redis(connection_pool=pool)

    def cache_con(self):
        return self.r

    @classmethod
    def get_single_cache(cls):
        if cls.r:
            return cls.r
        else:
            return cls().cache_con()

from setting import  EV
class MemcacheManager(Singleton):
    _client = None

    def __init__(self):
        try:
            if EV=='TEST':
                raise
            import bmemcached
            #,,OCS_ACCESS_PASS
            self._client = bmemcached.Client((OCS_ACCESS_URL),OCS_ACCESS_ID,OCS_ACCESS_PASS)
            self._client.set('cache_conn','OK')
            if not self._client.get('cache_conn') or self._client.get('cache_conn')!='OK':
                raise
            print 'aliyun ocs is connection...'
        except Exception:
            try:
                import memcache
                self._client = memcache.Client([MEMCACHE_HOST])
                print 'local memcache is connection...'
            except Exception:
                e = sys.exc_info()[0](traceback.format_exc())
                LOG.exception(e)

    def get_conn(self):
        return self._client

    @classmethod
    def get_single_conn(cls):
        if cls._client:
            return cls._client
        else:
            return cls().get_conn()

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @classmethod
    def get_cache(cls):
        return cls._client


# def pagecache(key = "", expiration = 3600*2, key_suffix_calc_func = None):
#     def _decorate(func):
#         def _wrapper(self, *args, **kwargs):
#             red = self.mcache
#             key_with_suffix = key
#             if key_suffix_calc_func:
#                 key_suffix = key_suffix_calc_func(self,*args, **kwargs)
#                 if key_suffix:
#                     key_with_suffix = '%s:%s' % (key, stringToUnicode(key_suffix))
#             print key_with_suffix
#             html = red.get(key_with_suffix)
#             print html
#             if not html:
#                 html = func(self, *args, **kwargs)
#                 red.set(key_with_suffix, html)
#                 red.expire(key_with_suffix, expiration)
#             print 'html',html
#             self.write(str(html))
#         return _wrapper
#     return _decorate

# if __name__=='__main__':
#     import memcache
#     _client = memcache.Client([MEMCACHE_HOST])
#     print _client
#     mcache = MemcacheManager()
#     _client = mcache.get_conn()
#     key = 'send_tel_msg'+'15397008337'
#     print _client.get(key)
#     # _client.set()
#     _client.set(key,'5',600)
#     print _client.get(key)
#     print client.get('cache_conn')
#
#     # print dir(client)
#     # # print client.stats()
#     # print client.set('key', 'value11111111111')
#     # print client.get('key')
#     rcache = RedisManaher()
#     p = rcache.cache_con()
#     #p.get('decoration_help')
#     # print dir(rcache.r)
#     # print type(rcache.r.set)
#     # print type(p)
#     # print dir(p)
#     # p.set('key','value')
#     # #print rcache.r.get('key')
#     # print p.get('index_role_cache_name')
#     # reg key:ip_reg
#     # config/image_code/login  key:ip_log
#     #
#     # import ujson
#     # data=[(10L, 10L, u'http://zenmez.oss-cn-hangzhou.aliyuncs.com/album/member/508d4265-4e71-3170-b247-2369ea589ba6/\u9ed8\u8ba4\u76f8\u518c/clock-desc-d.png', u'http://zenmez.oss-cn-hangzhou.aliyuncs.com/album/member/508d4265-4e71-3170-b247-2369ea589ba6/\u9ed8\u8ba4\u76f8\u518c/clock-desc-d.png', 1L, None), (8L, 8L, None, u'http://image.python-libs.com/album/member/508d4265-4e71-3170-b247-2369ea589ba6/\u9ed8\u8ba4\u76f8\u518c/002\u526f\u672c2.png', 1L, None), (8L, 8L, None, u'http://image.python-libs.com/album/member/508d4265-4e71-3170-b247-2369ea589ba6/\u9ed8\u8ba4\u76f8\u518c/002.png', 1L, None), (8L, 8L, None, u'http://image.python-libs.com/album/member/508d4265-4e71-3170-b247-2369ea589ba6/\u9ed8\u8ba4\u76f8\u518c/001.png', 1L, None), (4L, 4L, None, u'http://image.python-libs.com/album/member/508d4265-4e71-3170-b247-2369ea589ba6/\u9ed8\u8ba4\u76f8\u518c/2.jpg', 1L, None), (4L, 4L, None, u'http://image.python-libs.com/album/member/508d4265-4e71-3170-b247-2369ea589ba6/\u9ed8\u8ba4\u76f8\u518c/3.jpg', 1L, None)]
#     #
#     # client.set('preend',ujson.dumps(data),126)
#     # dd = client.get('preend')
#     # print dd
#     # client.set('key','value)
#     # print client.get('key')
#     '''
#     ['RESPONSE_CALLBACKS', '__class__', '__contains__', '__delattr__', '__delitem__', '__dict__', '__doc__', '__format__', '__getattribute__',
#     '__getitem__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setitem__',
#     '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_use_lua_lock', '_zaggregate', 'append', 'bgrewriteaof', 'bgsave', 'bitcount',
#     'bitop', 'bitpos', 'blpop', 'brpop', 'brpoplpush', 'client_getname', 'client_kill', 'client_list', 'client_setname', 'config_get',
#     'config_resetstat', 'config_rewrite', 'config_set', 'connection_pool', 'dbsize', 'debug_object', 'decr', 'delete', 'dump', 'echo',
#     'eval', 'evalsha', 'execute_command', 'exists', 'expire', 'expireat', 'flushall', 'flushdb', 'from_url', 'get', 'getbit', 'getrange',
#     'getset', 'hdel', 'hexists', 'hget', 'hgetall', 'hincrby', 'hincrbyfloat', 'hkeys', 'hlen', 'hmget', 'hmset', 'hscan', 'hscan_iter',
#     'hset', 'hsetnx', 'hvals', 'incr', 'incrby', 'incrbyfloat', 'info', 'keys', 'lastsave', 'lindex', 'linsert', 'llen', 'lock', 'lpop',
#     'lpush', 'lpushx', 'lrange', 'lrem', 'lset', 'ltrim', 'mget', 'move', 'mset', 'msetnx', 'object', 'parse_response', 'persist',
#     'pexpire', 'pexpireat', 'pfadd', 'pfcount', 'pfmerge', 'ping', 'pipeline', 'psetex', 'pttl', 'publish', 'pubsub', 'randomkey',
#     'register_script', 'rename', 'renamenx', 'response_callbacks', 'restore', 'rpop', 'rpoplpush', 'rpush', 'rpushx', 'sadd', 'save',
#     'scan', 'scan_iter', 'scard', 'script_exists', 'script_flush', 'script_kill', 'script_load', 'sdiff', 'sdiffstore', 'sentinel',
#     'sentinel_get_master_addr_by_name', 'sentinel_master', 'sentinel_masters', 'sentinel_monitor', 'sentinel_remove', 'sentinel_sentinels',
#     'sentinel_set', 'sentinel_slaves', 'set', 'set_response_callback', 'setbit', 'setex', 'setnx', 'setrange', 'shutdown', 'sinter',
#     'sinterstore', 'sismember', 'slaveof', 'slowlog_get', 'slowlog_len', 'slowlog_reset', 'smembers', 'smove', 'sort', 'spop', 'srandmember',
#     'srem', 'sscan', 'sscan_iter', 'strlen', 'substr', 'sunion', 'sunionstore', 'time', 'transaction', 'ttl', 'type', 'unwatch', 'watch',
#     'zadd', 'zcard', 'zcount', 'zincrby', 'zinterstore', 'zlexcount', 'zrange', 'zrangebylex', 'zrangebyscore', 'zrank', 'zrem',
#     'zremrangebylex', 'zremrangebyrank', 'zremrangebyscore',
#     'zrevrange', 'zrevrangebyscore', 'zrevrank', 'zscan', 'zscan_iter', 'zscore', 'zunionstore']
#     '''
#     #print dir(p)
#     product = {'1':100}
#     daries = [1,2,3,4,5]
#     p.set('dairy',daries)
#     print type(p.get('dairy')),p.get('dairy')
#     print 'exist',p.exists('dairy')
#     print 'exist',p.exists('dairies')
#
#     # p.set('items',items)
#     # print type(p.get('items')),p.get('items')
#     # p.setex('items',3600,items)
#     # print type(p.get('items')),p.get('items')
#
