#encoding:utf-8
__author__ = 'binpo'

from common.base import BaseHandler
import StringIO
from utils.create_img import create_validate_code
from utils.date_util import yyyydddddatetime
import ujson

class ImageHandler(BaseHandler):

    def get(self,code_type, *args, **kwargs):
        #code_type = self.get_argument('code_type',None)
        code_img= create_validate_code()
        #code_img[0].save("xiaorui.cc.gif", "GIF")
        #print 'str:',code_img[1]
    #   import Image, ImageFont, ImageDraw
        output = StringIO.StringIO()
    #     text = "EwWIieATzzz"
    #     im = Image.new("RGB",(130,35), (255, 255, 255))
    #     dr = ImageDraw.Draw(im)
    #     font = ImageFont.truetype("simsunb.ttf", 24)
    #     #simsunb.ttf 这个从windows fonts copy一个过来
    #     dr.text((10, 5), text, font=font, fill="#000000")
    # #    im.show()
    #     im.save(output,"GIF")
        code_img[0].save(output, "GIF")
        img_data = output.getvalue()
        #print 'code_img:',code_img[1]
        # ip = self.request.headers.get("X-Real-IP",'')
        # if not ip:
        #     ip = self.request.remote_ip
        user_ip = self.get_client_ip
        code_key = str(user_ip+'_'+(code_type and code_type or '_img_code_key'))
        # img_code_value = {'datetime':yyyydddddatetime(),'img_code':}
        # print ujson.dumps(img_code_value)
        #cookie_str = ujson.dumps(img_code_value)
        print code_key,code_img[1]
        self.mcache.set(code_key,code_img[1],120)
        self.set_cookie(code_key,code_img[1])   #图片 code 失效时间
        output.close()
        #在浏览器现实图片
        self.set_header('Content-Type','image/gif')
        self.write(img_data)

from common.base_handler import AdminBaseHandler
import StringIO
class BinaryImgHandler(BaseHandler):

    def post(self):
        url = self.get_argument('url')
        import qrcode
        q=qrcode.main.QRCode()
        q.add_data(url)
        q.make(fit=True)
        img = q.make_image()
        output = StringIO.StringIO()
        img.save(output)
        img_data = output.getvalue()
        output.close()
        self.set_header('Content-Type','image/png')
        self.write(img_data)

    def get(self):
        url = self.get_argument('url')
        import qrcode
        q=qrcode.main.QRCode()
        q.add_data(url)
        q.make(fit=True)
        img = q.make_image()
        output = StringIO.StringIO()
        img.save(output)
        img_data = output.getvalue()
        output.close()
        self.set_header('Content-Type','image/png')
        self.write(img_data)