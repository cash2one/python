#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on:2016/1/14 14:42
# Project:proxy_ok
# Author:yangmingsong

from myTool import proxy_test
from ms_spider_fw.DBSerivce import DBService
from Queue import Queue as qu
import threading
import time

# config text
db_name = 'b2c_base'
# give some tables name to extract proxy list to test , different table name be combined use ','
table_name_s = 'proxy_you_dai_li,proxy_black_hat_world'
connect_dict = {'host': '10.118.187.12', 'user': 'admin', 'passwd': 'admin', 'charset': 'utf8'}
proxy_list = []
for table_name in table_name_s.split(','):
    db_server = DBService(dbName=db_name, tableName=table_name, **connect_dict)
    proxy_list += map(lambda x: x[0], db_server.getData(var='proxy_port', distinct=True))

# script
qu_proxy_test = qu(0)
qu_proxy_ok = qu(0)

for t in proxy_list:
    qu_proxy_test.put(t)


def test():
    while qu_proxy_test.qsize():
        # noinspection PyBroadException
        try:
            proxy = qu_proxy_test.get(timeout=1)
        except Exception:
            break
        if proxy_test.test(proxy, timeout=3):
            print proxy
            qu_proxy_ok.put([proxy, time.strftime('%Y-%m-%d %X', time.localtime())])


def run_test(n):
    print 'Runnig proxy test process , please waiting'
    tsk_pool = []
    while n > 0:
        tsk_pool.append(threading.Thread(target=test))
        n -= 1
    for tsk in tsk_pool:
        tsk.start()
    for tsk in tsk_pool:
        tsk.join()
    print 'Proxy test process is end .'


def run(thread_count=1000):
    run_test(thread_count)
    db_server_c = DBService(dbName=db_name, tableName='proxy_ok', **connect_dict)
    db_server_c.createTable(tableTitle=['proxy_port', 'test_time'], x='Y')
    res = []
    while qu_proxy_ok.qsize():
        res.append(qu_proxy_ok.get())
    db_server_c.data2DB(data=res)


if __name__ == '__main__':
    run(5000)
