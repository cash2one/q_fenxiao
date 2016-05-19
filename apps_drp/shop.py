#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'binpo'
from base_handler import DrpBaseHandler

import StringIO
class Shophandler(DrpBaseHandler):

    def get(self):
        shop_id = self.current_user.get('shop_id')
        # url = 'http://m.qqqg.com/item/detail/'+shop_id+'.html'
        content = 'http://fenxiao.qqqg.com/drp/shop/'+shop_id+'.html'
        self.echo('admin_drp/shop.html',{'content':content,'url':content})

class Qrcodehandler(DrpBaseHandler):

    def get(self):
        content = self.current_user.get('content')
        import qrcode
        q=qrcode.main.QRCode()
        q.add_data(content)
        q.make(fit=True)
        img = q.make_image()
        output = StringIO.StringIO()
        img.save(output)
        img_data = output.getvalue()
        output.close()
        self.set_header('Content-Type','image/png')
        self.write(img_data)

class ItemDetailHandler(DrpBaseHandler):

    def get(self):
        self.get_paras_dict()
        show_id = self.qdict.get('show_id')
        url = 'http://fenxiao.qqqg.com/item/detail/'+show_id+'.html'
        self.echo('admin_drp/item_detail.html',{'content':url,'url':url})

        # shop_id = self.current_user.get('shop_id')
        # #ue\
        # #url = self.get_argument('url')
        # url = 'http://fenxiao.qqqg.com/drp/shop/'+shop_id+'.html'
        # import qrcode
        # q=qrcode.main.QRCode()
        # q.add_data(url)
        # q.make(fit=True)
        # img = q.make_image()
        # output = StringIO.StringIO()
        # img.save(output)
        # img_data = output.getvalue()
        # output.close()
        # self.set_header('Content-Type','image/png')
        # self.write(img_data)
