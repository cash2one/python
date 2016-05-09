#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on:2016/4/21 10:04
# Project:jd_comment_woman_cloth
# Author:yangmingsong

from pyspider.libs.base_handler import *
from ms_spider_fw.DBSerivce import DBService
import time
import json
import re
import threading

# connect_dict = {
#     'host': 'localhost',
#     'user': 'root',
#     'passwd': '',
#     'charset': 'utf8'
# }

_lock = threading._allocate_lock()
S = set()

# config_text
# when start a spider,you should modify the next config text first

db_name = 'jddata'
table_name = 'jd_comment_cow_powder'
table_title = 'product_name,comment_list_url,comment_json,crawl_time'
# cellphone page,can be change other industry
url_start = 'http://list.jd.com/1319-1523-7052.html'

# now,the next is spider script
db_server = DBService(dbName=db_name, tableName=table_name)

if not db_server.isTableExist():
    db_server.createTable(tableTitle=table_title.split(','))

pat_page_config = re.compile('pageConfig = (.+?);', re.DOTALL)
pat_word = re.compile('\w+:')
pat_score = re.compile('<span class="score-desc">(.+?)<.+?"number">(.+?)<.+?<'
                       'i class="(\w+?)">.+?"percent">(.+?)<', re.DOTALL)
pat_par = re.compile('<li title=.+?>(.+?)</li>')
pat_sku = re.compile('\d+')


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
        self.crawl(url_start, callback=self.step_first, retries=100, proxy=False)

    # def gen_url(self, response):
    #     d = response.doc
    #     for t in d(".menu-drop-list.clearfix>li a").items():
    #         self.crawl(t.attr.href, callback=self.step_first, retries=100)

    @config(age=10 * 24 * 60 * 60)
    def step_first(self, response):
        d = response.doc
        for t in d('.p-num>a').items():
            self.crawl(t.attr.href, callback=self.step_first, retries=100, timeout=2)
        for t in d('.gl-i-wrap.j-sku-item .p-name a').items():
            self.crawl(t.attr.href, callback=self.step_second, save={'name': t.text()}, retries=100, timeout=2)

    def step_second(self, response):
        txt = response.text
        sku_name = response.save.get('name')
        sku_id = pat_sku.findall(response.url)[0]
        if not sku_id in S:
            url = 'http://club.jd.com/productpage/p-' + sku_id + '-s-0-t-3-p-0.html'
            self.crawl(url, callback=self.step_third, retries=100, save={'sku': sku_id, 'name': sku_name}, timeout=2)
        data_temp = re.findall(pat_page_config, txt)[0]
        data = re.sub('\s+', '', data_temp)
        data = data.replace("'", '"')
        data_sub = re.findall(pat_word, data)
        for w in data_sub:
            if w == 'http:':
                continue
            else:
                temp = data.replace(w, '"' + w[:-1] + '"' + ':')
                data = temp
        data = json.loads(data)
        p = data.get('product')
        cs_list = p.get('colorSize')
        if cs_list:
            sku_l = list()
            for cs in cs_list:
                sku_l.append(cs.get('SkuId'))
            if sku_l:
                _lock.acquire()
                for sku in sku_l:
                    S.add(str(sku))
                _lock.release()

    @config(age=10 * 24 * 60 * 60)
    def step_third(self, response):
        url = response.url
        s = response.save
        sku_id = s['sku']
        sku_name = s['name']
        d = json.loads(response.text)
        comment_page_count_t = d['productCommentSummary']['commentCount']
        comment_page_count = 0 if comment_page_count_t <= 10 else (
            comment_page_count_t / 10 if comment_page_count_t % 10 == 0 else 1 + comment_page_count_t / 10)
        # print comment_page_count
        urls = [
            'http://club.jd.com/productpage/p-' + sku_id + '-s-0-t-3-p-' +
            str(x) + '.html'
            for x in range(comment_page_count - 1, 0, -1)
            ]
        if urls:
            for url_t in urls:
                self.crawl(url_t, callback=self.step_third, save=s, retries=100, timeout=2)
        return [
            sku_name,
            url,
            response.text,
            time.strftime('%Y-%m-%d %X', time.localtime())
        ]

    # over ride method for result store to mysql
    def on_result(self, result):
        if result:
            db_server.data2DB(data=result)
        else:
            print u'result-->return None'
