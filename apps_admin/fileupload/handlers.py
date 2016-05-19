#encoding:utf-8

__author__ = 'binpo'

from common.base_handler import AdminBaseHandler
from utils.upload_utile import upload_to_oss
from tornado.options import options
from services.item.gallery_services import GalleryServices
gallery_service = GalleryServices()
import ujson
import sys
from common.asyn_wrap import unblock

class FileManagerHandler(AdminBaseHandler):

    def get(self,img_type=0, *args, **kwargs):
        self.post(img_type=img_type)

    @unblock
    def post(self,img_type=0,*args, **kwargs):
        try:
            print '-----------fileupload-----------'
            gallery_service.set_db(self.db)
            is_ok, files = upload_to_oss(self,options.IMG_BUCKET, param_name='imgFile',file_type='img', file_prex=str(img_type), max_size=30,water_mark=False)
            if is_ok:
                full_url = '/'.join([options.IMG_DOMAIN,files.get('full_name')])
                gallery_id = gallery_service._add(pic_type = img_type,
                                     img_url = files.get('full_name'),
                                     full_url = full_url,
                                     size=files.get('size'))
                data={"error":0,
                        "url":full_url,
                        'msg':u'上传成功',
                        'id':str(gallery_id)
                 }
                print 'data:',data
            else:
                data={"error":1,
                        "url":'',
                        'msg':files
                 }
            return ujson.dumps(data)
        except Exception, e:
            print sys.exc_info()
            self.captureException(sys.exc_info())
            return ujson.dumps({'error':'1','url':'','msg':e.message})
