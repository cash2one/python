#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on:2016/3/16 13:55
# Project:data_extract
# Author:yangmingsong

from ms_spider_fw.DBSerivce import DBService
import json

db_name = 'alibaba'
table_name = 'contact_info_aliexpress_com'
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
            lambda x: x[0], db_server.getData(var='contact_detail')[17412:]
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
                d.get('contact_url'),
                d.get('open_time'),
                d.get('Company Name:'),
                d.get('contact_person'),
                d.get('Department:'),
                d.get('Position:'),
                d.get('Country/Region: '),
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
        tableTitle=[
            'shop_name',
            'contact_info_url',
            'open_time',
            'company_name',
            'contact_person',
            'department',
            'position',
            'country_region',
            'province',
            'city',
            'address',
            'zip'
        ], x='Y')
    res = []
    for item in data_s:
        res.append(extrac(item))
    db_server.data2DB(data=res)
