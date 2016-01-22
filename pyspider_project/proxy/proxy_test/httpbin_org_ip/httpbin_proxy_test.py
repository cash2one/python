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

qu_proxy_test = qu(0)
qu_proxy_ok = qu(0)

db_name = 'b2c_base'
table_name = 'proxy_black_hat_world'
table_title = 'proxy_port,crawl_time'
url_for_proxy_test = 'http://httpbin.org/ip'
connect_dict = {'host': '10.118.187.12', 'user': 'admin', 'passwd': 'admin', 'charset': 'utf8'}

db_server = DBService(dbName=db_name, tableName=table_name, **connect_dict)
proxy_list = map(lambda x: x[0], db_server.getData(var='proxy_port', distinct=True))
for p in proxy_list:
    qu_proxy_test.put(p)

patt_ip = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')


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
            # for test
            print('%s is okay.' % proxy)
            print res.text
            print '=' * 50
            print qu_proxy_test.qsize(),qu_proxy_ok.qsize()


def muti_thread_test(n):
    thread_pool = []
    while n > 0:
        thread_pool.append(threading.Thread(target=test))
        n -= 1
    for tsk in thread_pool:
        tsk.start()
    for tsk in thread_pool:
        tsk.join()


if __name__ == '__main__':
    muti_thread_test(5000)
    print '+' * 50
    while qu_proxy_ok.qsize():
        print qu_proxy_ok.get()