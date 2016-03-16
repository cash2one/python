#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on:2016/3/15 16:21
# Project:contact_info_aliexpress
# Author:yangmingsong

import time
import requests as req
from ms_spider_fw.DBSerivce import DBService

list_0 = []
list_1 = []
proxy_dict = {}
c = 0


def run():
    # connect_dict = {'host': 'localhost', 'user': 'root', 'passwd': '', 'charset': 'utf8'}
    connect_dict = {'host': '10.118.187.12', 'user': 'admin', 'passwd': 'admin', 'charset': 'utf8'}
    db_name = 'b2c_base'
    table_name = 'proxy_ok'
    db_server = DBService(dbName=db_name, tableName=table_name, **connect_dict)
    url_api = 'http://dev.kuaidaili.com/api/getproxy'
    par = {'orderid': 975806740125635, 'num': 20, 'an_ha': 1, 'sp1': 1, 'sort': 1}  # , 'an_ha': 1, 'sp1': 1, 'sort': 1
    ip_total = req.get(url_api, params=par).text
    p_l_t = set(filter(lambda x: 1 if x else 0, ip_total.split('\n')) + ip366_api())
    c = len(p_l_t)
    print u'本次提取共 %s 个代理' % c
    proxy_ok = p_l_t
    # proxy_ok = filter(lambda x: 1 if x not in proxy_dict or proxy_dict[x] >= 6 else 0, p_l_t)
    # print u'有效代理共 %s 个' % len(proxy_ok)

    if len(proxy_ok)==0:
        print '+' * 50 + u' 重启采集程序'
        c += 1
        if c % 3 == 0:
            time.sleep(5)
        run()

    # for t in p_l_t:
    #     if proxy_dict.has_key(t):
    #         if proxy_dict[t] >= 6:
    #             proxy_dict[t] = 1
    #         else:
    #             proxy_dict[t] = proxy_dict[t] + 1
    #     else:
    #         proxy_dict[t] = 1

    time_stamp = time.strftime('%Y-%m-%d %X', time.localtime())
    if proxy_ok:
        proxy_list = [[item, time_stamp] for item in proxy_ok]
        db_server.createTable(tableTitle=['proxy_port', 'crawl_time'], x='Y')
        db_server.data2DB(data=proxy_list)


def ip366_api():
    url_api = 'http://api.ip3366.net/api/?key=20160316110234541&getnum=20&anonymoustype=3&filter=1'
    ip_total = req.get(url_api).text
    return list(set(filter(lambda x: 1 if x else 0, ip_total.split('\r\n'))))


if __name__ == '__main__':
    i = 1
    while True:
        print u'第 %s 次提取' % i
        print time.ctime()
        run()
        print '-' * 100
        time.sleep(5)
        i += 1
