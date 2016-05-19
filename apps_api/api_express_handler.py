#encoding:utf-8
__author__ = 'binpo'

from apps_api.api_base_handler import ApiBaseHandler
from services.express.express_services import ExpressServices
from services.orders.orders_services import OrderServices
from services.item.item_services import ItemService
from models.orders_do import ItemOrders
from utils.md5_util import hmac_md5
import ujson,sys
from common.asyn_wrap import unblock
from services.logs.logs_services import LogsServices
from utils.logs import LOG
import traceback

express_service = ExpressServices()
order_service = OrderServices()
TOKEN='e9060bd3a5987d638ac66399444117d1'
ACCESS_USER = 'yhwl'
log = LOG('express_logs')

#海关回调
class ExpressHandler(ApiBaseHandler):

    def get(self):
        self.post()

    @unblock
    def post(self):
        '''
        :param order_no:订单num
        :param express_no:物流号
        :param express_company_code:物流公司code
        :param token:验证码
        :return:
        '''
        order_service.set_rdb(self.rdb)
        express_service.set_rdb(self.rdb)
        order_no = self.get_argument('order_no','')
        express_no = self.get_argument('express_no','')
        express_company_code = self.get_argument('express_company_code','')
        request_token = self.get_argument('token','')
        if not order_no:
            return ujson.dumps({'stat':'error','info':'订单号参数不能为空'})
        elif not express_no:
            return ujson.dumps({'stat':'error','info':'物流单号参数不能为空'})
        elif not express_company_code:
            return ujson.dumps({'stat':'error','info':'快递公司代码不能为空'})
        elif not request_token:
            return ujson.dumps({'stat':'error','info':'token不能为空'})
        token = hmac_md5(TOKEN,order_no+express_no)
        if token==request_token:
            pass
        else:
            return ujson.dumps({'stat':'error','info':'token错误,非法请求'})
        try:
            rsp = {'stat':'success',
                   'order_no':order_no,
                   'express_no':express_no,
                   'express_company_code':express_company_code,
                   'info':''
                  }
            order = order_service.get_order_no(order_no)
            express_company = express_service.get_express_company_code(express_company_code=express_company_code).scalar()

            if not order:
                rsp['stat'] = 'error'
                rsp['info'] = '订单号不存在'
            elif not express_company:
                rsp['stat'] = 'error'
                rsp['info'] = '物流公司不存在,物流公司代码出错'

            if rsp['stat'] == 'success':
                express_service.set_db(self.db)
                express_service.get_order_express_no(order,express_no,express_company.id)
                rsp = express_service._add(order,express_no,express_company.id,'ok',rsp)

            # item_service = ItemService()
            # item_service.set_db(self.db)
            # item_service.update_item_stock()

            #--------------------------更新库存------------------------------
            if rsp['stat'] == 'success': #发货成功，更新库存
                try:
                    sql_format = 'update item_detail set quantity=(quantity-{0}) where id={1};'
                    execute_sqls=[]
                    for item in self.db.query(ItemOrders).filter(ItemOrders.order_id==order.id):
                        execute_sqls.append(sql_format.format(item.buy_nums,item.item_id))
                    if execute_sqls:
                        # conn = DbConnection.get_conn()
                        # conn.begin()
                        # cur = conn.cursor()
                        # cur.
                        print ''.join(execute_sqls)
                        #self.db.execute(''.join(execute_sqls))
                    self.db.commit()
                except Exception,e:
                    self.captureMessage('更新库存失败:'+e.message)
                    self.captureException(sys.exc_info())
            logs_data ={}
            logs_data['logs_type']=1
            logs_data['reqeust_url']=self.request.uri
            logs_data['params'] = self.get_paras_dict()
            logs_data['action'] = 'post'
            if rsp['stat'] == 'error':
                logs_data['status'] = 0
            else:
                logs_data['status'] = 1
            logs_data['key_params'] = order_no
            logs_data['error'] = ujson.dumps(rsp)
            try:
                logs_service = LogsServices(db=self.db)
                logs_service.new_api_logs(**logs_data)
            except Exception,e:
                self.captureException(sys.exc_info())
            if logs_data['status'] == 1:
                return ujson.dumps({'stat':'success','info':'处理成功'})
            else:
                return ujson.dumps(rsp)
        except Exception,e:
            self.captureMessage(sys.exc_info())
            return ujson.dumps({'stat':'success','info':'回调成功'})

class BatchExpressHandler(ApiBaseHandler):
    '''
    批量发货接口
    '''
    def get(self, *args, **kwargs):
        self.post()

    @unblock
    def post(self, *args, **kwargs):

        params_data=data = self.get_argument('data','')
        try:
            LogsServices(db=self.db).new_api_logs(
                logs_type=2,
                key_params='',
                reqeust_url = self.request.host+self.request.uri,
                params = params_data,
                action = 'post',
                result = '',
                status = 1,
                error=''
            )
        except:
            pass
        if not data:
            return ujson.dumps({'stat':'error','info':'参数错误,数据不能为空'})
        try:
            data = ujson.loads(data)
        except:
            return ujson.dumps({'stat':'error','info':'数据格式错误,数据格式为严格的JSON数据格式'})
        try:
            token = data.get('token',None)
            express_data = data.get('data',None)
            order_nos=[]
            for express in express_data:
                order_no = express.get('order_no')
                if order_no:
                    order_nos.append(order_no)
            if len(order_nos)<1:
                return ujson.dumps({'stat':'error','info':'数据格式错误,订单号不能为空'})

            #用户名＋token hmac_md5加密  ＋ip白名单限制
            param_token = hmac_md5(TOKEN,ACCESS_USER)
            if token!=param_token:
                return ujson.dumps({'stat':'error','info':'token错误,非法请求'})
            express_service.set_db(self.db)
            error_data,invoice_orders = express_service.batch_add(express_data)
            logs_data={}
            logs_data['logs_type']=2
            logs_data['reqeust_url']=self.request.uri
            logs_data['params'] = params_data
            logs_data['action'] = 'post'
            logs_data['result'] = str(error_data)
            logs_data['status'] = 1
            logs_data['key_params'] = ''#;'.join([order_no for order_no in order_nos])
            if len(error_data)==len(order_nos):
                logs_data['status'] = 0
            elif 0<len(error_data)<len(order_nos):
                logs_data['status'] = 2
            logs_data['error'] = ujson.dumps(error_data)
            if logs_data['status']!=1:
                try:
                    pdata = ujson.loads(params_data)
                    pdata['data']=error_data
                    LogsServices(db=self.db).create_task(
                            task_type=2,
                            key_params=logs_data['key_params'],
                            reqeust_url=self.request.host+self.request.uri,
                            params=ujson.dumps(pdata),
                            action='post',
                            result='',
                            status=0,
                            error=ujson.dumps(error_data)
                    )
                except Exception,e:
                    print e.message

            if logs_data['status'] in (1,2):
                return ujson.dumps({'state':'success','info':'处理成功','code':200})
            else:
                return ujson.dumps({'state':'error','info':error_data,'code':401})
        except Exception,e:
            log.warning(traceback.format_exc())
            LogsServices(db=self.db).create_task(
                    task_type=2,
                    key_params=order_no,
                    reqeust_url=self.request.host+self.request.uri,
                    params=params_data,
                    action='post',
                    result='',
                    status=0,
                    error=e.message
            )
            return ujson.dumps({'state':'error','info':'处理失败','code':400})

        # {‘token’:’p9boLc9NygNU/8mc+7JhJA==‘,’data’:[{‘order_no’:’3144307983029’,’express_no’:’’,’express_company_code’:’’}]}
        #{"token": "p9boLc9NygNU/8mc+7JhJA==","data": [{"order_no": "3144307983029","express_no": "","express_company_code": "shunfeng"},{"order_no": "3144307983030","express_no": "","express_company_code": "shunfeng"}]}


