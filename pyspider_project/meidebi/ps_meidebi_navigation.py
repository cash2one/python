#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on:2016/1/11 14:05
# Project:ps_meidebi_navigation
# Author:yangmingsong

"""
collect all b2c websites on http://www.meidebi.com/company/,then choosing the useful B2C website
base:
--ip above **
--pv above **
--some other standards
"""

from pyspider.libs.base_handler import *
from ms_spider_fw.DBSerivce import DBService
import time

db_server = DBService(dbName='b2c_base', tableName='b2c_website_list_meidebi', host='10.118.187.12',
                      user='admin', passwd='admin', charset='utf8')

# create table for store result in mysql
db_server.createTable(tableTitle=[
    'name',
    'summary',
    'url',
    'evaluation_num',
    'total_score',
    'quality_score',
    'express_service_score',
    'customer_service_score',
    'crawl_time'
])


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=30 * 24 * 60)
    def on_start(self):
        self.crawl('http://www.meidebi.com/company/', callback=self.step_first)

    @config(age=30 * 24 * 60 * 60)
    def step_first(self, response):
        d = response.doc
        ignore = [u'团购', u'电视购物', u'教育培训', u'票务旅游', u'金融理财', u'网络服务']
        for each in d('.con>a').items():
            if each.text() not in ignore:
                self.crawl(each.attr.href, callback=self.step_second)

    @config(priority=2)
    def step_second(self, response):
        d = response.doc
        fw = d('.m_list.clearfix>li>a').items()
        for t in fw:
            self.crawl(t.attr.href, callback=self.my_result)

    def my_result(self, response):
        d = response.doc
        return [
            d('.right h1').text().replace(u'分享', '').strip(),  # website name
            d('.desc.less_desc.gray3').text()[:200],  # website summary
            d('.buy.mdb_btn.mb_bo').attr('href').split('url=')[1],  # url
            d('.count.fl>b').text(),  # evaluation number
            d('.point.hl_orange.fl').text(),  # total score
            d('.item:nth-child(1)>b').text(),  # product quality score
            d('.item:nth-child(2)>b').text(),  # express service score
            d('.item:nth-child(3)>b').text(),  # cutomer service score
            time.strftime('%Y-%m-%d %X', time.localtime())
        ]

    # over ride method for result store to mysql
    def on_result(self, result):
        if result:
            db_server.data2DB(data=result)
        else:
            print u'result-->return None'

if __name__=='__main__':
    H=Handler()