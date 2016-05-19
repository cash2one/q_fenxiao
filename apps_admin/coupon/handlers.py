#encoding:utf-8
__author__ = 'qiuyan'

from common.base_handler import AdminBaseHandler
from services.conpon.conpon_services import CouponService
coupon_serivice = CouponService()

class CouponHandler(AdminBaseHandler):

    def get(self, *args, **kwargs):

        coupon_serivice.set_rdb(self.rdb)
        coupon_channels = coupon_serivice.coupon_channel_list()
        coupon_types = coupon_serivice.coupon_type_list()
        if self.get_argument('operation',None) and self.get_argument('operation',None)=='edit':
            coupon_serivice.set_rdb(self.rdb)
            _id = self.get_argument('id',None)
            if _id:
                coupon = coupon_serivice.query_coupon_by_id(_id)
            else:
                coupon = None
            self.echo('admin/coupon/coupon_edit.html',{'coupon':coupon,'coupon_types':coupon_types,'coupon_channels':coupon_channels})
        else:
            self.get_paras_dict()
            query = coupon_serivice.coupon_list(**self.qdict)
            data = self.get_page_data(query)
            self.echo('admin/coupon/coupon_list.html',{'data':data,'coupon_types':coupon_types,'coupon_channels':coupon_channels})


    def post(self, *args, **kwargs):
        self.get_paras_dict()
        coupon_serivice.set_db(self.db)
        uid = coupon_serivice.edit_coupon(**self.qdict)
        self.redirect(self.reverse_url('coupon_handler')+'?uid='+uid)

    def put(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        pass



class CouponChannelHandler(AdminBaseHandler):

    def get(self, *args, **kwargs):
        if self.get_argument('operation',None) and self.get_argument('operation',None)=='edit':
            coupon_serivice.set_rdb(self.rdb)
            channel_id = self.get_argument('id',None)
            if channel_id:
                coupon_channel = coupon_serivice.query_channel_by_id(channel_id)
            else:
                coupon_channel = None
            self.echo('admin/coupon/channel_edit.html',{'coupon_channel':coupon_channel})
        else:
            coupon_serivice.set_rdb(self.rdb)
            conpon_channels = coupon_serivice.coupon_channel_list()
            self.echo('admin/coupon/channel.html',{'conpon_channels':conpon_channels})

    def post(self, *args, **kwargs):
        self.get_paras_dict()
        coupon_serivice.set_db(self.db)
        coupon_serivice.edit_channel(self.qdict.get('name'),self.qdict.get('code'),self.qdict.get('description'),self.qdict.get('id'))
        self.redirect(self.reverse_url('coupon_channel'))

    def put(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        pass


class CouponTypeHandler(AdminBaseHandler):

    def get(self, *args, **kwargs):
        if self.get_argument('operation',None) and self.get_argument('operation',None)=='edit':
            coupon_serivice.set_rdb(self.rdb)
            type_id = self.get_argument('id',None)
            if type_id:
                coupon_type = coupon_serivice.query_coupon_type_by_id(type_id)
            else:
                coupon_type = None
            self.echo('admin/coupon/channel_type_edit.html',{'coupon_type':coupon_type})
        else:
            coupon_serivice.set_rdb(self.rdb)
            conpon_types = coupon_serivice.coupon_type_list()
            self.echo('admin/coupon/channel_type.html',{'conpon_types':conpon_types})

    def post(self, *args, **kwargs):
        self.get_paras_dict()
        coupon_serivice.set_db(self.db)
        coupon_serivice.edit_coupon_type(self.qdict.get('name'),self.qdict.get('code'),self.qdict.get('description'),self.qdict.get('id'))
        self.redirect(self.reverse_url('coupon_type'))
