#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on:2016/3/15 16:21
# Project:contact_info_aliexpress
# Author:yangmingsong

import time
import requests as req
from ms_spider_fw.DBSerivce import DBService


def run():
    connect_dict = {'host': 'localhost', 'user': 'root', 'passwd': '', 'charset': 'utf8'}
    db_name = 'base'
    table_name = 'proxy_ok'
    db_server = DBService(dbName=db_name, tableName=table_name, **connect_dict)
    db_server.createTable(tableTitle=['proxy_port', 'crawl_time'], x='Y')
    url_api = 'http://dev.kuaidaili.com/api/getproxy'
    par = {'orderid': 975806740125635, 'num': 9999}  # , 'an_ha': 1, 'sp1': 1, 'sort': 1
    ip_total = req.get(url_api, params=par).text
    c = len(ip_total.split('\n'))
    print u'本次提取共 %s 个代理' % c
    p_l_t = list(set(filter(lambda x: 1 if x else 0, ip_total.split('\n'))))
    time_stamp = time.strftime('%Y-%m-%d %X', time.localtime())
    proxy_list = [[item, time_stamp] for item in p_l_t]
    db_server.data2DB(data=proxy_list)


if __name__ == '__main__':
    i = 1
    while True:
        run()
        print u'第 %s 次提取' % i
        time.sleep(300)
        i += 1
