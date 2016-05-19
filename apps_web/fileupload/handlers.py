#encoding:utf-8
__author__ = 'gaoaifei'

from common.base_handler import BaseHandler
from utils.upload_utile import upload_to_oss
from tornado.options import options
from services.item.gallery_services import GalleryServices
gallery_service = GalleryServices()
import ujson
import sys
from common.asyn_wrap import unblock

class FileManagerHandler(BaseHandler):



    def get(self,img_type=2, *args, **kwargs):
        self.post(img_type=img_type)

    @unblock
    def post(self, img_type=2, *args, **kwargs):
        '''
        上传图片
        :param img_type: 图片前缀
        :param args:
        :param kwargs:
        :return:
        '''
        try:
            gallery_service.set_db(self.db)
            keys = self.request.files.keys()[0] #获取文件域的名称
            is_ok, files = upload_to_oss(self,options.IMG_BUCKET, param_name=keys,file_type='img', file_prex='ifyshareimg', max_size=5,water_mark=False)
            if is_ok:
                full_url = '/'.join([options.IMG_DOMAIN,files.get('full_name')])
                gallery_id = gallery_service._add(pic_type = img_type,
                                     img_url = files.get('full_name'),
                                     full_url = full_url,
                                     size = files.get('size'))
                data={  "state":200,
                        "url":full_url,
                        'msg':u'上传成功',
                        'id':str(gallery_id)
                 }
            else:
                data={ "state":400,
                        "url":'',
                        'msg':files
                 }
            return ujson.dumps(data)
        except Exception, e:
            print sys.exc_info()
            self.captureException(sys.exc_info())
            return ujson.dumps({'error':'1','url':'','msg':e.message})

