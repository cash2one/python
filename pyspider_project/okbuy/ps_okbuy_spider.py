#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on:2016/1/11 18:45
# Project:ps_okbuy_spider
# Author:yangmingsong

from pyspider.libs.base_handler import *
from ms_spider_fw.DBSerivce import DBService

db_server = DBService(dbName='industry_data__clothes_shoes', tableName='okbuy', host='10.118.187.12',
                      user='admin', passwd='admin', charset='utf8')

# create table for store result in mysql
db_server.createTable(tableTitle=[])

class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.okbuy.com/brand/brandcat', callback=self.step_first)

    @config(age=10 * 24 * 60 * 60)
    def step_first(self, response):
        for each in response.doc('.t-abcconr-new>a').items():
            url=each.attr.href.split('?')[0]
            self.crawl(url, callback=self.my_result)

    @config(priority=2)
    def my_result(self, response):
        return []

    # over ride method for result store to mysql
    def on_result(self, result):
        if result:
            db_server.data2DB(data=result)
        else:
            print u'result-->return None'