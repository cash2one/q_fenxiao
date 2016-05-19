#!/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2013-11-22
@author: zhangjianxin
Email: rhca2013@163.com
'''
import time
import timeit
import urllib2
import threading
from Queue import Queue
from time import sleep

# 性能测试页面
#PERF_TEST_URL = "http://192.168.1.9/index.php"
#关于memc-nginx-module模块和php-fpm访问memcache性能比较详见,http://www.linuxsa.cn/memc-nginx-php-fpm-module.html
nginx_set = "http://127.0.0.1:8080/"
# nginx_get = "http://127.0.0.1:8080/asyn"
# php_set = "http://127.0.0.1:8080/asyn"
# php_get = "http://127.0.0.1:8080/asyn"

PERF_TEST_URL = nginx_set

# 参数配置
# 1.并发线程总数 2.每个线程的循环次数 3.每次请求时间间隔
THREAD_NUM = 100
ONE_WORKER_NUM = 100
LOOP_SLEEP = 0

# 出错数
ERROR_NUM = 0

# 具体的处理函数,负责处理单个任务
def doWork(index):
    '''
    Execute a single task
    '''
    t = threading.currentThread()
    #print "[" + t.name + " " + str(index) + "]" + PERF_TEST_URL

    try:
        html = urllib2.urlopen(PERF_TEST_URL).read()
    except urllib2.URLError, e:
        #print "[" + t.name + " " + str(index) + "]"
        #print e
        global ERROR_NUM
        ERROR_NUM += 1

# 这个是工作进程,负责不断从队列中取数据并处理
def working():
    '''
    To fetch data from the queue and processed
    '''
    t = threading.currentThread()
    #print "[" + t.name + "] Sub Thread Begin..."
    
    i = 0
    while i < ONE_WORKER_NUM:
        i += 1
        doWork(i)
        sleep(LOOP_SLEEP)
    
    #print "[" + t.name + "] Sub Thread End!!!"
    
def main():
    StartTime = time.time()
    Threads = []
    # 创建线程
    for i in range(THREAD_NUM):
        t = threading.Thread(target = working, name = "T" + str(i))
        t.setName(True)
        Threads.append(t)
    # 启动线程
    #exit(0)
    for t in Threads:
        t.start()
        
    for t in Threads:
        t.join()
    
    #print "Main Thread End."
    EndTime = time.time()
    SpendTime = EndTime - StartTime
    TotalThreadNum = THREAD_NUM * ONE_WORKER_NUM
    
    #print "="*40
    #print "URL: ", PERF_TEST_URL
    #print "任务总数: ", THREAD_NUM, "*", ONE_WORKER_NUM, "=", TotalThreadNum
    #print "总耗时(秒): ", SpendTime
    #print "每次请求耗时(秒): ", SpendTime / TotalThreadNum
    #print "每秒承载请求数: ", 1 / (SpendTime / TotalThreadNum)
    #print "错误数量: ", ERROR_NUM


def get_id_by_show_id(showId):
    '''
    根据showid获取真实id值
    :param showId: type string 自动增长列id值
    :return:
    '''
    showId = str(showId)
    i = showId[len(showId)-1]
    j = showId[0:len(showId)-1]
    k = (int(j) - int(i) - 1000)/int(i)
    return k
import random
def set_show_id_by_id(id):
    '''
    设置showid
    :param id: 真实id
    :return:
    '''
    a = random.randint(1,9)
    b = a*int(id) + 1000 + a
    j = str(b) + str(a)
    return j
if __name__ == "__main__":
    print set_show_id_by_id(55)
    print get_id_by_show_id(13306)
    exit(0)
    stat_time = timeit.default_timer()
    main()
    print timeit.default_timer()-stat_time