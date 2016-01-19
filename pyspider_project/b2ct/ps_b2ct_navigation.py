#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on:2016/1/11 12:54
# Project:ps_b2ct_navigation
# Author:yangmingsong

"""
collect all b2c websites on http://www.b2ct.com,then choosing the useful B2C website
base:
--ip above **
--pv above **
--some other standards
"""

from pyspider.libs.base_handler import *
from ms_spider_fw.DBSerivce import DBService
import time

db_server = DBService(dbName='b2c_base', tableName='b2c_website_list_b2ct', host='10.118.187.12',
                      user='admin', passwd='admin', charset='utf8')


# create table for store result in mysql
# db_server.createTable(tableTitle=[
#     'catalogue_name',
#     'website_slogan',
#     'b2ct_link',
#     'url',
#     'website_name','crawl_time'
# ])

class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=30 * 24 * 60)
    def on_start(self):
        self.crawl('http://www.b2ct.com/', callback=self.step_first)

    @config(age=30 * 24 * 60 * 60)
    def step_first(self, response):
        d = response.doc
        ignore = [u'首页', u'团购', u'旅游', u'优惠券']
        for each in d('.zh>li>a').items():
            if each.text() not in ignore:
                self.crawl(each.attr.href, callback=self.my_result)

    @config(priority=2)
    def my_result(self, response):
        d = response.doc
        fw = d('.info2>a').items()
        return [
            [d('.place.zh>a:nth-child(2)').text(),  # catalogue name
             t.attr('title'),  # title for the href
             t.attr.href,  # href for redirect to target website
             'http://www.' + t.attr.href.split('/')[-1][:-5] + '.com',  # new target website url
             t('img').attr('alt'),
             time.strftime('%Y-%m-%d %X', time.localtime())]
            for t in fw
            ]

    # over ride method for result store to mysql
    def on_result(self, result):
        if result:
            db_server.data2DB(data=result)
        else:
            print u'result-->return None'
