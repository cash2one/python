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
from pyquery.pyquery import PyQuery

# config_text

db_name = 'address'
table_name_1 = 'ershoufang_ganji_baseinfo'
table_name_2 = 'ershoufang_ganji_detail'
table_name_3 = 'ershoufang_ganji_amenities'
table_title_1 = 'detail,crawl_time'
table_title_2 = 'url,detail,crawl_time'
table_title_3 = 'url,detail,crawl_time'
url_start = 'http://sz.ganji.com/xiaoqu/'
# connect string , usually no need to modify
connect_dict = {'host': '10.118.187.12', 'user': 'admin',
                'passwd': 'admin', 'charset': 'utf8'}

db_server_1 = DBService(dbName=db_name, tableName=table_name_1, **connect_dict)
db_server_2 = DBService(dbName=db_name, tableName=table_name_2, **connect_dict)
db_server_3 = DBService(dbName=db_name, tableName=table_name_3, **connect_dict)

# if create table for store result in mysql , no need to be changed
if not db_server_1.isTableExist():
    db_server_1.createTable(tableTitle=table_title_1.split(','))

if not db_server_2.isTableExist():
    db_server_2.createTable(tableTitle=table_title_2.split(','))

if not db_server_3.isTableExist():
    db_server_3.createTable(tableTitle=table_title_3.split(','))

p_lat_lon = re.compile('coord=(\S+?);')


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
        self.crawl(url_start, callback=self.step_first, retries=100, proxy=False)

    @config(age=1 * 24 * 60 * 60)
    def step_first(self, response):
        d = response.doc
        for t in d('.posrelative a').items():
            area = t.text()
            if area == u'不限':
                continue
            save_t = {
                'area': area,
                'city': u'深圳'
            }
            self.crawl(t.attr.href, callback=self._step_second, save=save_t, retries=100)

    @config(age=15 * 24 * 60 * 60)
    def _step_second(self, response):
        d = response.doc
        s = response.save
        for t in d('.subarea a').items():
            area = t.text()
            if area == u'不限':
                continue
            save_t = {
                'area_sub': area,
            }
            s_t = dict(s.items() + save_t.items())
            self.crawl(t.attr.href, callback=self.step_second, save=s_t, retries=100)

    @config(age=15 * 24 * 60 * 60)
    # @config(priority=5)
    def step_second(self, response):
        d = response.doc
        save_t = response.save
        for r in d('.pageLink li a').items():
            href = r.attr.href
            if href:
                self.crawl(href, callback=self.step_second, save=save_t, retries=100)

        result_t = list()
        for t in d(".list-img.list-xq").items():
            name = t(".list-info-title").text()
            href = t(".list-info-title").attr.href

            address = t('.xiaoqu-street').text()
            sell_count = t('.ico-sell+a').text()
            rent_count = t('.ico-rent+a').text()
            sell_price = t(".fc-org.xq-price-num").text()
            up_down = t('.list-part:nth-child(2) span').attr('class')
            rate_up_down = t('.list-part:nth-child(2) i:nth-child(2)').text() + "%"
            # map_href = t('.info .tli4 a:nth-child(1)').attr.href
            src = t('.list-mod1 img').attr.src
            detail = {
                'area': save_t,
                'name': name,
                'address': address,
                'href': href,
                'sell_count': sell_count,
                'rent_count': rent_count,
                'sell_price': sell_price,
                'up_down': up_down,
                'rate_up_down': rate_up_down,
                'picture_href': src
            }
            result_t.append(json.dumps(detail))
            if href:
                self.crawl(href, callback=self.detail_page, save=detail, retries=100)
        return [1, map(lambda x: [x, time.strftime('%Y-%m-%d %X', time.localtime())], result_t)]

    @config(age=15 * 24 * 60 * 60)
    def detail_page(self, response):
        t = response.text.replace('&nbsp;', '')
        d = PyQuery(t)
        base = response.save
        base_url = response.url
        fenbu = dict(map(
                lambda x: (x.find('.field-righttit').text(), x.find('ul').text()),
                list(d.find(".right-border div").items())
        ))
        basic_info = dict(map(
                lambda x: (x.text().replace(u'：', "").strip(),
                           x.parent().text().replace(x.text(), "").strip()),
                list(d.find('.fc-gray').items())
        ))
        other_info = dict(map(
                lambda x: (x.text().replace(u'：', ''), x.next().text()), list(d.find('.xiaoqu-otherinfo dt').items())
        ))
        info_temp = {
            'base': base,
            'sell_rent_info': fenbu,
            'basic_info': basic_info,
            'other_info': other_info
        }
        url = base_url + 'amenities/'
        self.crawl(url, callback=self.amenities_page, save=info_temp, retries=100)

        return [
            2,
            response.url,
            json.dumps(info_temp),
            time.strftime('%Y-%m-%d %X', time.localtime())
        ]

    @config(age=15 * 24 * 60 * 60)
    def amenities_page(self, response):
        t = response.text
        d = response.doc
        s = response.save
        lat_lon_t = p_lat_lon.findall(t)
        lat_lon = dict()
        if lat_lon_t:
            t = lat_lon_t[0].split(',')
            lat_lon = dict([('lat', t[0]), ('lon', t[1])])
        amenities = dict(map(
                lambda x: (x.text().replace(u'：', '').replace(' ', ''), x.next().text()),
                list(d.find('.info-tit').items())))
        return [
            3,
            response.url,
            json.dumps(dict(s.items() + [('amenities',amenities)] + [('lat_lon', lat_lon)])),
            time.strftime('%Y-%m-%d %X', time.localtime())
        ]

    # over ride method for result store to mysql
    def on_result(self, result):
        if result:
            if result[0] == 1:
                db_server_1.data2DB(data=result[1:][0])
            elif result[0] == 2:
                db_server_2.data2DB(data=result[1:])
            elif result[0] == 3:
                db_server_3.data2DB(data=result[1:])
            else:
                print u'result-->return None'
