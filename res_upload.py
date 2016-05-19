#encoding:utf-8
__author__ = 'binpo'

'''
静态资源上传脚本

'''
from libs.oss.oss_api import *

try:
    from libs.oss.oss_xml_handler import *
except:
    # from oss_xml_handler import *
    pass
from setting import OSS_HOST
HOST = OSS_HOST

from setting import ACCESS_ID,SECRET_ACCESS_KEY
ACCESS_ID = ACCESS_ID#"RmIF3RxSaGhHuS30"
SECRET_SECRET_ACCESS_KEY = SECRET_ACCESS_KEY#"nrBeozrHL2oBfQMiVybnbUDjsRkk02"


#ACCESS_ID=ACCESS_ID #'RmIF3RxSaGhHuS30'
#SECRET_ACCESS_KEY = SECRET_ACCESS_KEY#'nrBeozrHL2oBfQMiVybnbUDjsRkk02'

#ACCESS_ID and SECRET_SECRET_ACCESS_KEY 默认是空，请填入您申请的正确的ID和KEY.

sep = "=============================="
headers = {}


oss=None
res=None

if len(ACCESS_ID) == 0 or len(SECRET_SECRET_ACCESS_KEY) == 0:
    print "Please make sure ACCESS_ID and SECRET_SECRET_ACCESS_KEY are correct in ", __file__ , ", init are empty!"
    exit(0)
def get_oss():

    global oss
    oss = OssAPI(HOST, ACCESS_ID, SECRET_SECRET_ACCESS_KEY)
    res = oss.get_service()

#指定文件名, 把这个文件上传到bucket中,在bucket中的文件名叫object。
def upload_file(bucket,filename,file_name):
    if not oss:
        get_oss()
    object = file_name#"object_test"
    #filename = __file__
    content_type = get_content_type_by_filename(filename)
    headers = {}

    fp = open(filename, 'rb')
    res = oss.put_object_from_fp(bucket, object, fp, content_type, headers)
    fp.close()
    if (res.status / 100) == 2:
        print "put_object_from_fp OK"
    else:
        print "put_object_from_fp ERROR"
    print sep


if __name__ == "__main__": 
    #初始化
    # if len(ACCESS_ID) == 0 or len(SECRET_SECRET_ACCESS_KEY) == 0:
    #     print "Please make sure ACCESS_ID and SECRET_SECRET_ACCESS_KEY are correct in ", __file__ , ", init are empty!"
    #     exit(0)
    # oss = OssAPI(HOST, ACCESS_ID, SECRET_SECRET_ACCESS_KEY)
    # sep = "=============================="
    # res = oss.get_service()
    #
    #
    # #create bucket
    # create_my_bucket('userid')
    #
    #
    # # #列出创建的bucket
    # show_all_my_bucket()
    #
    import timeit
    start = timeit.default_timer()
    import os
    #上传文件到根目录
    #upload_file('zenmez','IMG_0662.JPG','IMG_0662.JPG')
    #上传到user/hello目录下 如果没有则创建目录
    current_path = os.path.dirname(__file__)
    static_path = os.path.join(current_path, 'static')
    print static_path
    # from os.path import isfile, join
    # onlyfiles = [ f for f in os.listdir(static_path) if isfile(join(static_path,f)) ]
    # for fname in onlyfiles:
    #     print fname
    f=[]
    # print os.path.isdir(static_path)
    def join_file(f,path):
        for path_name in os.listdir(path):
            file_path = os.path.join(path, path_name)
            if os.path.isfile(file_path):
                # f.append(path_name)
                pass
            elif os.path.isdir(file_path):
                f.append(file_path)
                next_dir=file_path
                # pre_path = os.path.join(pre_path, path_name)
                join_file(f,next_dir)
    join_file(f,static_path)
    # print f
    upload_files=[]
    # for a,b,c in os.walk(static_path):
    #     print a,b,c
    for path in f:
        # print f
        for a,b,c in os.walk(path):
            for file_name in c:
                # print static_path
                file_path = os.path.join(path,file_name)
                ufile = file_path.replace(static_path+'/','')
                upload_files.append((file_path,ufile))
            break
    for key,value in upload_files:
        # if value.endswith('core.min.js'):
        #     print key,value
        if 'microshop' in value:
            upload_file('qqqg-static',key,value)
        # break
    print 'upload success'




    # f = []
    # for (dirpath, dirnames, filenames) in os.walk(static_path):
    #     f.extend(filenames)
    # for t in f :
    #     print t
    # for path in os.walk(static_path):
    #     print path
    # upload_file('zenmezhuang','/Users/binpo/Downloads/苏威个人简历+作品集2/个人简历2色彩缤纷-01.png','ttt2/个人简历2色彩缤纷-01.png')
    # print timeit.default_timer()-start
    # start = timeit.default_timer()
    #
    # upload_with_multi_upload_file('zenmezhuang','/作品集2/个人简历2色彩缤纷-01.png','/Users/binpo/Downloads/苏威个人简历+作品集2/个人简历2色彩缤纷-01.png')
    # print timeit.default_timer()-start
    #create_my_bucket_with_location('zenmeza','zenmez')