#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on:2016/1/15 17:45
# Project:ps_amazon_spider
# Author:yangmingsong

from pyspider.libs.base_handler import *
from ms_spider_fw.DBSerivce import DBService
import re
import time

# config_text
db_name = 'platform_data'
table_name = 'amazon'
table_title = 'product_url,catalogue,product_title,brand,brand_page_url,comment_counts,comment_page_url,' \
              'origin_price,price,base_service,deliver_service,comp_list_page_url,product_params,crawl_time'
url_start = 'http://www.amazon.cn/gp/site-directory/ref=nav_shopall_btn'
connect_dict = {'host': '10.118.187.12', 'user': 'admin', 'passwd': 'admin', 'charset': 'utf8'}

# now,the next is spider script
db_server = DBService(dbName=db_name, tableName=table_name, **connect_dict)

# if create table for store result in mysql , no need to be changed
if not db_server.isTableExist():
    db_server.createTable(tableTitle=table_title.split(','))


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl(url_start, callback=self.step_first)

    @config(age=2 * 24 * 60 * 60)
    def step_first(self, response):
        d = response.doc
        for t in d('.a-nostyle.a-horizontal.sd-last-child li .a-list-item a').items():
            self.crawl(t.attr.href, callback=self.step_second)

    @config(age=30 * 24 * 60 * 60)
    def step_second(self, response):
        d = response.doc
        for t in d('.s-item-container>div:nth-child(2) a').items():
            self.crawl(t.attr.href, callback=self.my_result)
        for x in d('#pagn a').items():
            self.crawl(x.attr.href, callback=self.step_second)

    @config(priority=2)
    def my_result(self, response):
        d = response.doc
        txt = response.text

        # for join the company_list_page url , only third_part seller would got it
        # match market_id
        pat = re.compile(r'pf_rd_m=.+&')
        try:
            market_id = re.findall(pat, txt)[0]
        except IndexError:
            market_id = None
        if market_id:
            market_id = market_id.split('=')[1][:-1]

        url_base_b = 'http://www.amazon.cn/gp/aag/main?ie=UTF8&asin=&isAmazonFulfilled=&isCBA=&marketplaceID='
        url_base_m = '&orderID=&protocol=current&seller='
        url_base_e = '&sshmPath='

        def url_join_inner(x, y):
            if x:
                return url_base_b + x + url_base_m + y + url_base_e
            else:
                return None

        return [
            response.url,
            d('.a-horizontal.a-size-small').text(),  # catalogue
            d('#productTitle').text(),  # product title
            d('#brand').text(),  # brand
            d('#brand').attr('href'),  # brand main page url
            # d('.swSprite.s_star_4_5 span').text(),  # product stars
            d('#acrCustomerReviewLink span').text().split(' ')[0],  # comment count
            d('#acrCustomerReviewLink').attr('href'),  # product comment page
            d('.a-span12.a-color-secondary.a-size-base').text(),  # base/original price
            d('#priceblock_ourprice').text(),  # price
            d('.a-size-base.a-color-base').text(),  # express and other service
            d('.a-size-base.a-color-secondary.a-text-normal').text(),  # deliver service
            # for join the company_list_page url , only third_part seller would got it
            # given components to join url
            url_join_inner(market_id, d('#sellingCustomerID').attr('value')),
            '|'.join([t.text() for t in d('.content>ul>li').items()]),  # product base info/params
            time.strftime('%Y-%m-%d %X', time.localtime())
        ]

    # over ride method for result store to mysql
    def on_result(self, result):
        if result:
            db_server.data2DB(data=result)
        else:
            print u'result-->return None'
