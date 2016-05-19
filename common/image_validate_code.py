#encoding:utf-8
__author__ = 'binpo'

from common.base_handler import BaseHandler
import StringIO
from utils.create_img import create_validate_code

class ImageHandler(BaseHandler):

    def get(self,*args, **kwargs):
        code_img= create_validate_code()
        output = StringIO.StringIO()
        code_img[0].save(output, "GIF")
        img_data = output.getvalue()
        user_ip = self.get_client_ip
        code_key = str(user_ip+'_img_code')
        client = self.mcache
        client.set(code_key,code_img[1],180)
        self.set_cookie(code_key,code_img[1])   #图片 code 失效时间
        output.close()
        #在浏览器现实图片
        self.set_header('Content-Type','image/gif')
        self.write(img_data)

