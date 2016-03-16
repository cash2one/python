#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on:2016/3/16 13:55
# Project:data_extract
# Author:yangmingsong

from ms_spider_fw.DBSerivce import DBService
import json

db_name = 'alibaba'
table_name = 'contact_info_aliexpress'
table_title = 'shop_url,contact_detail,crawl_time'
connect_dict = {
    'host': '10.118.187.12',
    'user': 'admin',
    'passwd': 'admin',
    'charset': 'utf8'
}

db_server = DBService(dbName=db_name, tableName=table_name, **connect_dict)


def crawled_data():
    return map(
            lambda x: x[0], db_server.getData(var='contact_detail')
    )


def extrac(x):
    try:
        d = json.loads(x)
    except:
        return []
    return map(
            lambda x: '' if x == None else x,
            [
                d.get('shop_name'),
                d.get('contact_person'),
                d.get('Department:'),
                d.get('Province/State: '),
                d.get('City: '),
                d.get('Street Address: '),
                d.get('Zip:')
            ]
    )


if __name__ == '__main__':
    data_s = crawled_data()
    db_server = DBService(dbName=db_name, tableName='aliexpress_contactinfo_extract', **connect_dict)
    db_server.createTable(
        tableTitle=['shop_name', 'contact_person', 'department', 'province', 'city', 'address', 'zip'], x='Y')
    res = []
    for item in data_s:
        res.append(extrac(item))
    db_server.data2DB(data=res)
