#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on:2016/1/12 19:56
# Project:ps_blackhatworld_spider
# Author:yangmingsong

from pyspider.libs.base_handler import *
from ms_spider_fw.DBSerivce import DBService
import re

# config_text
db_name = 'b2c_base'
table_name = 'proxy_black_hat_world'
table_title = 'proxy_port,crawl_time'
url_start = 'http://www.blackhatworld.com/blackhat-seo/f103-proxy-lists/'
connect_dict = {'host': '10.118.187.12', 'user': 'admin', 'passwd': 'admin', 'charset': 'utf8'}

# script
db_server = DBService(dbName=db_name, tableName=table_name, **connect_dict)
if not db_server.isTableExist():
    db_server.createTable(tableTitle=table_title.split(','))

# compile re pattern
re_pat = re.compile(r'\d+.\d+.\d+.\d+:\d+')


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl(url_start, callback=self.step_first)

    @config(age=3 * 24 * 60 * 60)
    def step_first(self, response):
        d = response.doc
        for t in d('dd>span>a').items():
            self.crawl(t.attr.href, callback=self.my_result)

    @config(priority=2)
    def my_result(self, response):
        return list(set(re.findall(re_pat, response.text)))

    # over ride method for result store to mysql
    def on_result(self, result):
        if result:
            db_server.data2DB(data=result)
        else:
            print u'result-->return None'
