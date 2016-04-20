#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on:2016/4/18 11:03
# Project:
# Author:yangmingsong

from pyspider.libs.base_handler import *
from ms_spider_fw.DBSerivce import DBService
import time
import re
import json

# config_text

db_name = 'address'
table_name = 'tcmap_china'
table_title = 'detail,crawl_time'
url_start = 'http://www.tcmap.com.cn/'
# connect string , usually no need to modify
connect_dict = {'host': '10.118.187.12', 'user': 'admin',
                'passwd': 'admin', 'charset': 'utf8'}

db_server = DBService(dbName=db_name, tableName=table_name, **connect_dict)

# if create table for store result in mysql , no need to be changed
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

    @config(age=1 * 24 * 60 * 60)
    def step_first(self, response):
        d = response.doc
        for t in d('div>p>a').items():
            province = t.text()
            if province == u'香港':
                break
            self.crawl(t.attr.href, callback=self.step_second, save={'province': province}, retries=100)

    @config(age=1 * 24 * 60 * 60)
    def step_second(self, response):
        d = response.doc
        save_t = response.save
        for t in d('#page_left>table tr').items():
            city = t('td>strong>a').text()
            if not city:
                continue

            city_code = t("td:nth-child(4)").text()
            zip_code = t("td:nth-child(5)").text().strip()
            for r in t('td>a').items():
                area = r.text()
                save_r = dict(
                        save_t.items() + [('city', city), ('area', area), ('city_code', city_code),
                                          ('zip_code', zip_code)])
                self.crawl(r.attr.href, callback=self.step_third, save=save_r, retries=100)

    @config(age=15 * 24 * 60 * 60)
    def step_third(self, response):
        d = response.doc
        save_t = response.save
        frame_table = d('#page_left table tr').items()
        if frame_table:
            for t in frame_table:
                street = t('td strong a').text()
                if not street:
                    continue
                zip_code_sub = t('td:nth-child(2)').text().strip()
                save_r = dict(save_t.items() + [('street', street), ('zip_code_sub', zip_code_sub)])
                self.crawl(t('td strong a').attr.href, callback=self.step_third, save=save_r, retries=100)

        district = d('.f12').text().replace(u'注：数据来自网络，仅供参考。欢迎 纠错 ！', '')
        if not district:
            return None
        result_t = list()
        if district:
            district_s_t = district.split(' ')
            district_s = map(lambda x: district_s_t[x[0]:x[1]],
                             map(lambda x: (x, x + 3), range(0, len(district_s_t), 3)))
            zip_temp = ['administrative_code', 'administrative_code_sub', 'district_name']
            for item in district_s:
                result_t.append(zip(zip_temp, item))
        result_ok = list()
        if result_t:
            for item in result_t:
                detail = json.dumps(dict(save_t.items() + item))
                crawl_time = time.strftime('%Y-%m-%d %X', time.localtime())
                result_ok.append([detail, crawl_time])

        return result_ok

    # over ride method for result store to mysql
    def on_result(self, result):
        if result:
            db_server.data2DB(data=result)
        else:
            print u'result-->return None'
