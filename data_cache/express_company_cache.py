#encoding:utf-8
__author__ = 'binpo'
from cache_base import CacheBase
import ujson
from models.express_do import ExpressCompany

class ExpressCompanyCache(CacheBase):

    def get_express_company_info(self,compamy_id):
        '''
        根据快递公司id缓存公司信息
        :param compamy_id:
        :return:
        '''
        key='express_company_'+str(compamy_id)
        company_info = self.mcache.get(key)
        if company_info:
            return ujson.loads(company_info)
        else:
            company = self.db.query(ExpressCompany).filter(ExpressCompany.deleted==0,ExpressCompany.id==compamy_id).scalar()
            if company:
                data = {'name':company.name,
                        'code':company.code,
                        'id':company.id}
                self.mcache.set(key,ujson.dumps(data),7*24*3600)
                self.db.close()
                return data
            else:
                return None

    def get_express_company_info_by_company_code(self,compamy_code):
        '''
        根据快递公司代码缓存公司信息
        :param compamy_code:
        :return:
        '''
        key='express_company_'+str(compamy_code)
        company_info = self.mcache.get(key)
        if company_info:
            return ujson.loads(company_info)
        else:
            company = self.db.query(ExpressCompany).filter(ExpressCompany.deleted==0,ExpressCompany.code==compamy_code).scalar()
            if company:
                data = {'name':company.name,
                        'code':company.code,
                        'id':company.id}
                self.mcache.set(key,ujson.dumps(data),7*24*3600)
                self.db.close()
                return data
            else:
                return None
