#!/usr/bin/env python2.7
# encoding:utf-8
from __future__ import absolute_import
import datetime
import traceback
from celery_tasks.base import DatabaseTasks
from celery_tasks.celery import app
from models.orders_do import *
from models.express_do import *
from models.item_do import ItemComment
from data_cache.user_cache import UserCache
from utils.logs import LOG

pay_log = LOG('crontab_logs')

@app.task(base=DatabaseTasks)
def cancel_timeout_orders():
    '''
    超时订单处理
    :return:
    '''
    #update item_detail set sale_quantity=(sale_quantity+45) where id=1
    session = cancel_timeout_orders.db
    user_cache = UserCache()
    try:
        date = datetime.datetime.now()-datetime.timedelta(hours=6)
        orders = session.query(Orders).filter(Orders.deleted==0,Orders.status==1,Orders.pay_status==0,Orders.gmt_created<date)
        order_ids=[o.id for o in orders]
        sql_format = 'update item_detail set sale_quantity=(sale_quantity+{0}) where id={1};'
        if orders.count()>0:
            orders.update({'status':4,'cancle_remark':'订单超时关闭'},synchronize_session=False)
        execute_sqls=[]
        for item in session.query(ItemOrders).filter(ItemOrders.order_id.in_(order_ids)):
            execute_sqls.append(sql_format.format(item.buy_nums,item.item_id))
        for order_id in order_ids:
            user_cache.delete_user_daily_pay(order_id)
        #未支付并且订单超时 取消订单
        if order_ids:
            session.query(PayOrders).filter(PayOrders.deleted==0,PayOrders.pay_status==0,PayOrders.order_id.in_(order_ids)).update({'pay_status':2},synchronize_session=False)
        if execute_sqls:
            session.execute(''.join(execute_sqls))
        session.commit()
    except Exception,e:
        pay_log.info(traceback.format_exc())
        try:
            session.rollback()
            session.close()
        except:
            pass
    finally:
        try:
            session.close()
        except:
            pass

# @app.task(base=DatabaseTasks)
# def receive_timeout_orders():
#     '''
#     自动签收订单,发货时间超过10天自动确认
#     :return:
#     '''
#     try:
#         timeout = datetime.datetime.now()-datetime.timedelta(days=10)
#         invoice_orders = complete_timeout_orders.db.query(InvoiceOrders).filter(InvoiceOrders.deleted==0,InvoiceOrders.status==1,InvoiceOrders.gmt_modified<timeout)
#         for o in invoice_orders:
#             o.status=2
#             o.receive_time = now()
#             o.complete_time=now()
#             o.remark='超时自动签收'
#             #
#             # o.receive_time=now()
#             # o.delivery_status=2
#             # o.complete_time=now()
#             # o.status=2
#             complete_timeout_orders.db.add(o)
#         complete_timeout_orders.db.commit()
#     except:
#         try:
#             complete_timeout_orders.db.rollback()
#             complete_timeout_orders.db.close()
#         except:pass
#     finally:
#         try:complete_timeout_orders.db.close()
#         except:pass
#

@app.task(base=DatabaseTasks)
def complete_timeout_orders():
    '''
    自动签收完成订单,发货单签收超过超过5天自动确认为签收
    :return:
    '''
    try:
        timeout = datetime.datetime.now()-datetime.timedelta(days=10)
        invoice_orders = complete_timeout_orders.db.query(InvoiceOrders).filter(InvoiceOrders.deleted==0,InvoiceOrders.status==1,InvoiceOrders.gmt_modified<timeout)
        for o in invoice_orders:
            o.status=2
            o.receive_time = now()
            o.complete_time=now()
            o.remark='超时自动签收'
            complete_timeout_orders.db.query(Orders).filter(Orders.id==o.order_id).update(
                {
                'receive_time':now(),
                'delivery_status':2,
                'complete_time':now(),
                'status':2
                })
            #
            # o.receive_time=now()
            # o.delivery_status=2
            # o.complete_time=now()
            # o.status=2
            complete_timeout_orders.db.add(o)
        complete_timeout_orders.db.commit()
    except:
        try:
            complete_timeout_orders.db.rollback()
            complete_timeout_orders.db.close()
        except:pass
    finally:
        try:complete_timeout_orders.db.close()
        except:pass


@app.task(base=DatabaseTasks)
def comment_timeout_orders():
    '''
        发货时间超过15天自动好评
    :return:
    '''
    try:
        timeout = datetime.datetime.now()-datetime.timedelta(days=10)
        _orders = comment_timeout_orders.db.query(Orders.id,Orders.user_id,ItemOrders.item_id).join(ItemOrders,ItemOrders.order_id==Orders.id).filter(Orders.deleted==0,Orders.status==2,InvoiceOrders.complete_time<timeout)
        for o in _orders:
            item_comment = ItemComment()
            item_comment.item_id = o.item_id
            item_comment.order_id = o.id
            item_comment.user_id = o.user_id
            item_comment.user_name = UserCache().get_user_info(o.user_id).get('nick')
            item_comment.assess_level = 2
            item_comment.comment = '系统默认好评'
            item_comment.is_show = False
            item_comment.show_imgs = ''
            o.is_assess = True
            comment_timeout_orders.db.add(item_comment)
            comment_timeout_orders.db.add(o)
        comment_timeout_orders.db.commit()
    except:
        try:
            comment_timeout_orders.db.rollback()
            comment_timeout_orders.db.close()
        except:pass
    finally:
        try:comment_timeout_orders.db.close()
        except:pass
