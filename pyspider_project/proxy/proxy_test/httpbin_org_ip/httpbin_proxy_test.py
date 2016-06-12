#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on:2016/1/13 9:57
# Project:httpbin_proxy_test
# Author:yangmingsong

from ms_spider_fw.DBSerivce import DBService
from Queue import Queue as qu
import requests
import json
import re
import threading
import time

qu_proxy_test = qu(0)
qu_proxy_ok = qu(0)

# db_name = 'b2c_base'
db_name = 'base'
table_name_s = 'proxy_other_source,proxy_xi_ci_dai_li,proxy_you_dai_li,mimiip'
table_title = 'proxy_port,crawl_time'
url_for_proxy_test = ' '
# connect_dict = {'host': '10.118.187.12', 'user': 'admin', 'passwd': 'admin', 'charset': 'utf8'}
connect_dict = {'host': 'localhost', 'user': 'root', 'passwd': '', 'charset': 'utf8'}

# db_server = DBService(dbName=db_name, tableName=table_name, **connect_dict)
# proxy_list = map(lambda x: x[0], db_server.getData(var='proxy_port', distinct=True))
# for p in proxy_list:
#     qu_proxy_test.put(p)

patt_ip = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')
proxy_list = []

for table_name in table_name_s.split(','):
    print table_name
    db_server = DBService(dbName=db_name, tableName=table_name, **connect_dict)
    if db_server.isTableExist():
        proxy_list += map(lambda x: x[0], db_server.getData(var='proxy_port'))

proxy_list_t=list(set(proxy_list))
for p in proxy_list_t:
    qu_proxy_test.put(p)


def original_ip_address():
    t = requests.get('http://httpbin.org/ip').text
    return json.loads(t).get('origin')


original = original_ip_address()


def test():
    while qu_proxy_test.qsize():
        proxy = qu_proxy_test.get()
        s = requests.Session()
        proxy_s = {'http': 'http://%s' % proxy}
        try:
            res = s.get('http://httpbin.org/ip', proxies=proxy_s, timeout=1)
        except:
            continue
        ip_return = re.findall(patt_ip, res.text)
        if ip_return \
                and proxy.split(':')[0] == ip_return[0] \
                and len(ip_return) == 1 \
                and original not in ip_return \
                and len(res.text) < 100:
            qu_proxy_ok.put(proxy)
            print proxy
            # for test
            # logger.debug(proxy)


def muti_thread_test(n):
    thread_pool = []
    while n > 0:
        thread_pool.append(threading.Thread(target=test))
        n -= 1
    for tsk in thread_pool:
        tsk.start()

    time.sleep(300)
    # for tsk in thread_pool:
    #     tsk.join()


def run(thread_count=20000):
    muti_thread_test(thread_count)
    db_server_c = DBService(dbName=db_name, tableName='proxy_ok', **connect_dict)
    db_server_c.createTable(tableTitle=['proxy_port', 'test_time'], x='Y')
    res = []
    while qu_proxy_ok.qsize():
        res.append([
            qu_proxy_ok.get(),
            time.strftime('%Y-%m-%d %X', time.localtime())
        ])
    db_server_c.data2DB(data=res)


if __name__ == '__main__':
    run()
