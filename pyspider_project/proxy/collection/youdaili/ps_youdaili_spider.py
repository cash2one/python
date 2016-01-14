#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on:2016/1/14 13:55
# Project:ps_youdaili_spider
# Author:yangmingsong


from pyspider.libs.base_handler import *
from ms_spider_fw.DBSerivce import DBService
import re
import time

# config_text
db_name = 'b2c_base'
table_name = 'proxy_you_dai_li'
table_title = 'proxy_port,crawl_time'
url_start = 'http://www.youdaili.net/Daili/'
connect_dict = {'host': '10.118.187.12', 'user': 'admin', 'passwd': 'admin', 'charset': 'utf8'}

# script
db_server = DBService(dbName=db_name, tableName=table_name, **connect_dict)
if not db_server.isTableExist():
    db_server.createTable(tableTitle=table_title.split(','))

patt_ip = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d]):\d+')


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl(url_start, callback=self.step_first)

    @config(age=2 * 24 * 60 * 60)
    def step_first(self, response):
        d = response.doc
        for t in d('.newslist_listyle>a').items():
            self.crawl(t.attr.href, callback=self.step_second)

    def step_second(self, response):
        d = response.doc
        for t in d('.newslist_line>li>a').items():
            self.crawl(t.attr.href, callback=self.step_third)

    @config(age=10 * 24 * 60 * 60)
    def step_third(self, response):
        self.my_result(response)
        d = response.doc
        for t in d('.pagelist>li>a').items():
            self.crawl(t.attr.href, callback=self.step_third)

    @config(priority=2)
    def my_result(self, response):
        txt = response.text
        proxy_list = re.findall(patt_ip, txt)
        self.on_result(map(lambda x: [x, time.strftime('%Y-%m-%d %X', time.localtime())], proxy_list))

    # over ride method for result store to mysql
    def on_result(self, result):
        if result:
            db_server.data2DB(data=result)
        else:
            print u'result-->return None'
