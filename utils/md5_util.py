#encoding:utf-8
'''
Created on 2014-6-1

@author: qiuyan.zwp
'''

import hmac
import hashlib
import base64
import urllib

def create_md5(args):
    md5_constructor = hashlib.md5
    return md5_constructor(args).hexdigest()

def hmac_md5(key,args):
    myhmac = hmac.new(key,args, hashlib.md5)
    str_result = base64.b64encode(myhmac.digest())
    return str_result

def hmac_md5_php(secret_access_key,string_to_sign):
    '''
    Python对PHP服务器hmac_md5签名认证方法的匹配实现
    :param secret_access_key: key值
    :param string_to_sign: 字符串
    :return: string
    '''
    signature = hmac.new(secret_access_key, string_to_sign, digestmod=hashlib.md5).hexdigest()
    return signature
# ''
# #
# key='123qwe.'
# args='113144350773830'
# print hmac_md5(key,args)
# key='123qwe.'
# msg ='13144280328661'
#HilwMAJ87tGN5XBddNHUmQ==
#HilwMAJ87tGN5XBddNHUmQ==
# d = hmac.new(key,'',hashlib.sha1)
# d.update(msg)
# content = d.hexdigest()
# print content
# import base64
# print 'SP1uEQ+y2hUesG02XXn3tw=='
# print base64.b32encode(content)
# print base64.b64encode(content)

# g1 = hmac.digest()
# g2 = hmac.hexdigest()
# g3 = hmac.copy()
# print g1
# print g2
# print g3
# print create_md5('123qwe.120150914006')
# print hmac_md5('123qwe.','120150914006')
# import base64
# print base64.b64encode(hmac_md5('123qwe.','120150914006'))
# from hashlib import md5
# trans_5C = "".join(chr(x ^ 0x5c) for x in xrange(256))
# trans_36 = "".join(chr(x ^ 0x36) for x in xrange(256))
# blocksize = md5().block_size
#
# def hmac_md5(key, msg):
#     if len(key) > blocksize:
#         key = md5(key).digest()
#     key += chr(0) * (blocksize - len(key))
#     o_key_pad = key.translate(trans_5C)
#     i_key_pad = key.translate(trans_36)
#     h = md5(o_key_pad + md5(i_key_pad + msg).digest())
#     return h.hexdigest()
# if __name__ == "__main__":
#     h = hmac_md5("key", "The quick brown fox jumps over the lazy dog")
#     print h.hexdigest()  # 80070713463e7749b90c2dc24911e275