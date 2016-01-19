#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on:2015/12/24 11:06
# Project:zhou_xiu_product
# Author:yangmingsong

from pyspider.libs.base_handler import *
from ms_spider_fw.DBSerivce import DBService

# config_text
db_name = 'industry_data__clothes_shoes'
table_name = 'zhouxiu'
table_title = 'product_name,brand,product_url,sizes,price,origin_price'
url_start = 'http://www.xiu.com/brand.html'  # start url for crawl,string
connect_dict = {'host': '10.118.187.12', 'user': 'admin', 'passwd': 'admin', 'charset': 'utf8'}

# now,the next is spider script
db_server = DBService(dbName=db_name, tableName=table_name, **connect_dict)
if not db_server.isTableExist():
    db_server.createTable(tableTitle=table_title.split(','))


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl(url_start, callback=self.index_page)

    @config(age=2 * 24 * 60 * 60)
    def index_page(self, response):
        d = response.doc
        for temp in d('.brand_top_menu a').items():
            self.crawl(temp.attr.href, callback=self.product_page)

    @config(age=2 * 24 * 60 * 60)
    def product_page(self, response):
        d = response.doc
        for temp in d('h2+dl>dd>a').items():
            self.crawl(temp.attr('href'), callback=self.in_page)

    @config(age=10 * 24 * 60 * 60)
    def in_page(self, response):
        d = response.doc
        for temp in d('.Pagenum>a').items():
            if 'javascript' in temp.attr.href:
                continue
            else:
                self.crawl(temp.attr.href, callback=self.detail_page)
                self.crawl(temp.attr.href, callback=self.in_page)

    # noinspection PyMethodMayBeStatic
    def detail_page(self, response):
        d = response.doc
        return [[
                    di('.tit>a').text(),  # name
                    di('.tit>span').text(),  # "brand"
                    di.find('.pic>a').attr('href'),  # "product_url"
                    di('.ssl_item>span').text(),  # "size"
                    di('.showprice').text(),  # "showprice"
                    di('.delprice').text()  # "delprice"
                ] for di in d('.item').items()]

    # over ride method for result store to mysql
    def on_result(self, result):
        print(result)
        if result:
            db_server.data2DB(data=result)
        else:
            print u'result-->return None'
