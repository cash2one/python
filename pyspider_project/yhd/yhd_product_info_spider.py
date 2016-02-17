#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on:2016/2/3 18:16
# Project:yhd_product_info_spider
# Author:yangmingsong

from pyspider.libs.base_handler import *
from ms_spider_fw.DBSerivce import DBService
import time
import re
import json

# config_text

db_name = 'platform_data'
table_name = 'yhd_product_info'
table_title = 'url,category,product_name,product_par,sold,seller,seller_href,dsr,hidden_value,crawl_time'
url_start = 'http://www.yhd.com/marketing/allproduct.html?' \
            'tp=2092.0.153.0.1.LAaSxkk-00-33^eM'
# connect string , usually no need to modify
connect_dict = {'host': '10.118.187.12', 'user': 'admin',
                'passwd': 'admin', 'charset': 'utf8'}

db_server = DBService(dbName=db_name, tableName=table_name, **connect_dict)
# if create table for store result in mysql , no need to be changed
if not db_server.isTableExist():
    db_server.createTable(tableTitle=table_title.split(','))

pat_value = re.compile('input type=\"hidden\" autocomplete=\"off\" id=\"(.+?)\"\s{1,2}value=\"(.+?)\".*?>')
pat_par = re.compile('<dd title=\".*?>(.*?)</dd>')


class Handler(BaseHandler):
    crawl_config = {
        'proxy': '10.10.10.10:80',
        'headers': {
            'User-Agent': 'User-Agent:Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) '
                          'Gecko/20100101 Firefox/4.0.1'
        }
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl(url_start, callback=self.step_first, retries=100)

    @config(age=2 * 24 * 60 * 60)
    def step_first(self, response):
        d = response.doc
        for t in d('.fore>dd>em>span>a').items():
            self.crawl(t.attr.href, callback=self.step_second, retries=100)

    @config(age=10 * 24 * 60 * 60)
    def step_second(self, response):
        d = response.doc
        for t in d('.proName>a:nth-child(1)').items():
            self.crawl(t.attr.href, callback=self.my_result, retries=100)
        for t in d('.turn_page a').items():
            self.crawl(t.attr.href, callback=self.step_second, retries=100)

    @config(priority=2)
    def my_result(self, response):
        txt = response.text
        d = response.doc
        hidden_value = re.findall(pat_value, txt)
        hidden_value = json.dumps(hidden_value)
        category = d('.mod_detail_crumb.clearfix a').text()
        product_name = d('#productMainName').text()
        sold_num = d('#mod_salesvolume>strong').text()
        seller = d('.shop_name>a:nth-child(1)').text()
        seller_href = d('.shop_name>a:nth-child(1)').attr('href')
        seller_dsr = d('.inshopInf_sd li').text()
        product_par = re.findall(pat_par, txt)
        product_par = json.dumps(product_par) if product_par else ''
        crawl_time = time.strftime('%Y-%m-%d %X', time.localtime())
        return [
            response.url,
            category.split(seller)[0] if seller else category,
            product_name,
            product_par,
            sold_num,
            seller,
            seller_href,
            seller_dsr.replace(u' ◆ ', ''),
            hidden_value,
            crawl_time
        ]

    # over ride method for result store to mysql
    def on_result(self, result):
        if result:
            db_server.data2DB(data=result)
        else:
            print u'result-->return None'
