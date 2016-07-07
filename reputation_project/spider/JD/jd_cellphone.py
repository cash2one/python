#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on:2016/3/1 10:04
# Project:jd_comment_cellphone
# Author:yangmingsong

from pyspider.libs.base_handler import *
from ms_spider_fw.DBSerivce import DBService
import time
import json

# config_text
# when start a spider,you should modify the next config text first

db_name = 'platform_data'
table_name = 'jd_comment_cellphone_0'
table_title = 'product_name,comment_list_url,comment_json,crawl_time'
# cellphone page,can be change other industry
url_start = 'http://list.jd.com/list.html?cat=9987,653,655&page=1&go=0&JL=6_0_0'

# now,the next is spider script
db_server = DBService(dbName=db_name, tableName=table_name)

if not db_server.isTableExist():
    db_server.createTable(tableTitle=table_title.split(','))


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

    @config(age=0.5 * 24 * 60 * 60)
    def step_first(self, response):
        d = response.doc
        # 产品列表页面翻页
        for t in d('.pn-next').items():
            self.crawl(t.attr.href, callback=self.step_first, retries=100)
        for t in d('.gl-i-wrap.j-sku-item').items():
            sku_id = t('.p-focus a').attr('data-sku')
            sku_name = t('.p-name em').text()
            comment_list_url = 'http://club.jd.com/productpage/p-' + sku_id + \
                               '-s-0-t-3-p-0.html'
            self.crawl(comment_list_url, callback=self.my_result, retries=100,
                       save={
                           'sku': sku_id,
                           'name': sku_name
                       })

    @config(age=10 * 24 * 60 * 60)
    def step_second(self, response):
        """
        在生产系统，本部分内容不需爬取，只取第一页内容即可；
        """
        url = response.url
        s = response.save
        sku_id = s['sku']
        sku_name = s['name']
        d = json.loads(response.text)
        comment_page_count_t = d['productCommentSummary']['showCount']
        comment_page_count_t = comment_page_count_t / 10 \
            if comment_page_count_t % 10 == 0 \
            else 1 + comment_page_count_t / 10
        # max page limit
        comment_page_count = 30 \
            if comment_page_count_t >= 30 \
            else comment_page_count_t
        urls = [
            'http://club.jd.com/productpage/p-' + sku_id + '-s-0-t-3-p-' +
            str(x) + '.html'
            for x in range(comment_page_count - 1, 0, -1)
            ]
        if urls:
            for url in urls:
                self.crawl(url, callback=self.my_result, save=s, retries=100)
        return [
            sku_name,
            url,
            response.text,
            time.strftime('%Y-%m-%d %X', time.localtime())
        ]

    @config(priority=2)
    def my_result(self, response):
        return [
            response.save['name'],
            response.url,
            response.text,
            time.strftime('%Y-%m-%d %X', time.localtime())
        ]

    # over ride method for result store to mysql
    # def on_result(self, result):
    #     if result:
    #         db_server.data2DB(data=result)
    #     else:
    #         print u'result-->return None'
