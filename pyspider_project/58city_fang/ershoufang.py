#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on:2016/4/18 17:46
# Project:
# Author:yangmingsong

from pyspider.libs.base_handler import *
from ms_spider_fw.DBSerivce import DBService
import time
import re
import json

# config_text

db_name = 'address'
table_name_1 = 'ershoufang_58city_baseinfo'
table_name_2 = 'ershoufang_58city_detail'
table_title_1 = 'detail,crawl_time'
table_title_2 = 'url,detail,crawl_time'
url_start = 'http://www.58.com/ershoufang/changecity/'
# connect string , usually no need to modify
connect_dict = {'host': '10.118.187.12', 'user': 'admin',
                'passwd': 'admin', 'charset': 'utf8'}

db_server_1 = DBService(dbName=db_name, tableName=table_name_1, **connect_dict)
db_server_2 = DBService(dbName=db_name, tableName=table_name_2, **connect_dict)

# if create table for store result in mysql , no need to be changed
if not db_server_1.isTableExist():
    db_server_1.createTable(tableTitle=table_title_1.split(','))

if not db_server_2.isTableExist():
    db_server_2.createTable(tableTitle=table_title_2.split(','))

pat_num = re.compile('\d+')
pat_replace_space = re.compile('\s+?')
pat_comment = re.compile('var arr=(.+?)\;')


class Handler(BaseHandler):
    crawl_config = {
        # 'proxy': '10.10.10.10:80',
        'headers': {
            'User-Agent': 'User-Agent:Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) '
                          'Gecko/20100101 Firefox/4.0.1'
        }
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl(url_start, callback=self.step_first, retries=100)

    @config(age=1 * 24 * 60 * 60)
    def step_first(self, response):
        d = response.doc
        for t in d('#clist>dt').items():
            province = t.text()
            if province == u'热门':
                continue
            for r in t.next()('a').items():
                city = r.text()
                save_t = {
                    'province': province,
                    'city': city
                }
                href = r.attr.href.replace('ershoufang', 'xiaoqu')
                self.crawl(href, callback=self.step_second, save=save_t, retries=100)

    @config(age=15 * 24 * 60 * 60)
    @config(priority=5)
    def step_second(self, response):
        d = response.doc
        save_t = response.save
        for r in d('#xiaoquPager>a').items():
            self.crawl(r.attr.href, callback=self.step_second, save=save_t, retries=100)
        result_t = list()
        for t in d("tbody tr").items():
            name = t(".info .tli1").text()
            address = t('.info .tli2').text()
            ershoufang_t = pat_num.findall(t('.info .tli3 span:nth-child(1)').text())
            ershoufang = ershoufang_t[0] if ershoufang_t else '-'
            ershoufang_href = t('.info .tli3 span:nth-child(1) a').attr.href
            chuzufang_t = pat_num.findall(t('.info .tli3 span:nth-child(2)').text())
            chuzufang = chuzufang_t[0] if chuzufang_t else '-'
            chuzufang_href = t('.info .tli3 span:nth-child(2) a').attr.href
            detail_href = t('.info .tli4 a:nth-child(1)').attr.href
            if detail_href:
                self.crawl(detail_href, callback=self.detail_page, save=save_t, retries=100)
            # map_href = t('.info .tli4 a:nth-child(1)').attr.href
            money = t('.money').text()
            up_down = t('.jg p:nth-child(2)>span:nth-child(2)').attr.class_
            rate = t('.jg p:nth-child(2)>span:nth-child(2)').text()
            detail = {
                'area': save_t,
                'name': name,
                'address': address,
                'ershoufang': ershoufang,
                'ershoufang_href': ershoufang_href,
                'chuzufang': chuzufang,
                'chuzufang_href': chuzufang_href,
                'detail_href': detail_href,
                # 'map_href': map_href,
                'money': money,
                'up_down': up_down,
                'rate': rate
            }
            result_t.append(json.dumps(detail))
        return [1,
                map(
                        lambda x: [x, time.strftime('%Y-%m-%d %X', time.localtime())], result_t
                )]

    @config(age=15 * 24 * 60 * 60)
    def detail_page(self, response):
        d = response.doc
        save_t = response.save
        name = d('.xiaoquh1').text()
        comment_detail_t = pat_comment.findall(response.text)
        comment_detail_t = {
            'comment_detail': json.loads(comment_detail_t[0].replace("'", '"')) if comment_detail_t else '-'}
        base_info_t = dict(map(lambda x: x.split(u'：', 1),
                               [re.sub(pat_replace_space, '', t.text())
                                for t in list(d('.bhrInfo dd').items())
                                ]))
        other_info_t = dict(map(lambda x: map(
                lambda y: y.replace(u'\u00a0', ''), x.split(u'：', 1)
        ), [re.sub(pat_replace_space, '', r.parent().text())
            for r in d('.litit').items()
            ]))
        return [
            2,
            response.url,
            json.dumps({
                'area': save_t,
                'xiaoqu_name': name,
                'comment_detail': comment_detail_t,
                'base_info': base_info_t,
                'other_info': other_info_t
            }),
            time.strftime('%Y-%m-%d %X', time.localtime())
        ]

    # over ride method for result store to mysql
    def on_result(self, result):
        if result:
            if result[0] == 1:
                db_server_1.data2DB(data=result[1:][0])
            elif result[0] == 2:
                db_server_2.data2DB(data=result[1:])
            else:
                print u'result-->return None'
