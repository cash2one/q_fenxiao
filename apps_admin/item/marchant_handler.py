#encoding:utf-8
__author__ = 'jinkuan'

from ..common_handler import CommonHandler
from services.merchant.merchant_services import MerchantService

merchant_services = MerchantService()


class VendorHandler(CommonHandler):

    def get(self, operation,*args, **kwargs):
        merchant_services.set_rdb(self.rdb)
        if operation == 'list':
            query = merchant_services._list()
            data = self.get_page_data(query)
            self.echo('admin/merchant/list.html',{'data':data,'count':query.count()})
        else:
            vendor_id = self.get_argument('vendor_id','')
            vendor = merchant_services.get_by_id(vendor_id)
            self.echo('admin/merchant/_add.html',{'vendor':vendor})

    def post(self, operation,*args, **kwargs):
        self.get_paras_dict()
        merchant_services.set_db(self.db)
        print self.qdict.get('user_pwd')
        print self.qdict.get('name')
        merchant_services._add(name=self.qdict.get('name'),
                               account = self.qdict.get('account'),
                               address=self.qdict.get('address'),
                               contact=self.qdict.get('contact'),
                               phone=self.qdict.get('phone'),
                               remark=self.qdict.get('remark',''),
                               vendor_id=self.qdict.get('vendor_id',''))
        self.write('添加成功!')





















