#encoding:utf-8
__author__ = 'gaoaifei'

from common.base_handler import AdminBaseHandler
from services.express.express_services import ExpressServices
express_service = ExpressServices()

class ExpressHandler(AdminBaseHandler):

    def get(self,operation=None, *args, **kwargs):
        self.get_paras_dict()
        content = self.qdict.get('content','') #判断身份证号码，手机,订单号
        express_service.set_rdb(self.rdb)
        query = express_service.get_invoice_orders(**self.qdict)
        expresses = self.get_page_data(query)
        self.echo('admin/express/express_list.html',{'data':expresses,
                                                     'content':content,
                                                     'count':query.count()})

    def post(self, operation=None, *args, **kwargs):
        pass

    def get_express_name_by_id(self,id):
        '''
        获取物流公司名称
        :param id:
        :return:
        '''
        express_service.set_rdb(self.rdb)
        return express_service.get_express_company_by_id(id)

    def get_user_name_by_user_id(self,user_id):
        '''

        :param user_id:
        :return:
        '''
        express_service.set_rdb(self.rdb)
        return express_service.get_user_name_by_user_id(user_id)