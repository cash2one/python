#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on:2016/1/7 18:20
# Project:ps_beibei_spider
# Author:yangmingsong

from pyspider.libs.base_handler import *
import sys
from ms_spider_fw.DBSerivce import DBService
import time

reload(sys)
# noinspection PyUnresolvedReferences
sys.setdefaultencoding('utf8')

db_server = DBService(dbName='industry_data__mon_baby', tableName='beibei', host='10.118.187.12',
                      user='admin', passwd='admin', charset='utf8')


# db_server.createTable(tableTitle=[
#     'title',
#     'product_url',
#     'catalogue',
#     'price_del',
#     'discount',
#     'price_origin',
#     'shopping_price',
#     'shopping_from',
#     'brand',
#     'score_total',
#     'score_sending',
#     'score_express',
#     'express_supplier',
#     'material',
#     'article_number',
#     'make_in',
#     'expiration_date',
#     'size',
#     'other_info',
#     'crawl_time'
# ])

class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.beibei.com/category/dress.html', callback=self.step_first)

    @config(age=1 * 24 * 60 * 60)
    def step_first(self, response):
        # get the brand_list page url(attr) from brand_page
        d = response.doc
        for t in d('.sub-nav li>a').items():
            t_inner = t.attr('href')
            if 'category' in t_inner:
                self.crawl(t_inner, callback=self.step_second)

    @config(age=2 * 24 * 60 * 60)
    def step_second(self, response):
        d = response.doc
        # get the brand page url(attr) from brand_page
        for t in d('.brand-full>a').items():
            self.crawl(t.attr('href'), callback=self.step_third)

        # brand_page page turning
        for i in d('.brand-page>a').items():
            self.crawl(i.attr('href'), callback=self.step_second)

    @config(age=10 * 24 * 60 * 60)
    def step_third(self, response):
        # get the product url(attr->href) from brand shop page
        d = response.doc
        for t in d('.view-ItemListItem>a').items():
            self.crawl(t.attr('href'), callback=self.detail_page)

    def global_sale(self, response):
        d = response.doc

        def other_info():
            return '|'.join(map(lambda t: t.text() + t.next().text(), d('.props.clearfix>li>b').items()))

        return [
            d('.title>h3').text(),
            response.url,
            d('.crumb a:nth-child(2)').text(),
            d('.pink .price').text(),
            d('.over-zhe').text(),
            d('.market').text(),
            d('.baoyou').text(),
            d('.over-sendout').text(),
            '-',
            '-',
            '-',
            '-',
            '-',
            '-',
            '-',
            '-',
            '-',
            '-',
            other_info(),
            time.strftime('%Y-%m-%d %X', time.localtime())
        ]

    def detail_page(self, response):
        # parser the product page and collect the product_info
        d = response.doc
        if u'【全球购】' in d('title').text():
            return self.global_sale(response)
        # beibei self_support does not given score
        try:
            score = d('.eva-con>p>span').text().split(' ')
        except Exception:
            score = ['-', '-', '-']
        # the next part is used for extract information from product_info_table
        info_dict = {}
        other_info = ''
        for t in d('.props.clearfix>li').items():
            if t:
                # take care, the sep '：' is chinese characters
                t_text = t.text().split('：')
                if t_text[0] in (u'默认快递', u'材质', u'货号', u'产地', u'保持期', u'尺寸'):
                    info_dict[t_text[0]] = t_text[1]
                else:
                    other_info += ':'.join(t_text) + '|'

        return [
            d('.title>h3').text(),
            response.url,
            d('.crumb a:nth-child(2)').text(),
            d('.pink .price').text(),
            d('.discount.view-SkuPriceDiscountInfo').text(),
            d('.market .strike').text(),
            d('.baoyou').text(),
            d('.p1').text(),
            d('.dec-con>p>span').text(),
            score[0],
            score[1],
            score[-1],
            info_dict.get(u'默认快递'),
            info_dict.get(u'材质'),
            info_dict.get(u'货号'),
            info_dict.get(u'产地'),
            info_dict.get(u'保持期'),
            info_dict.get(u'尺寸'),
            other_info[:-2],  # delete the last redundant symbols '|'
            time.strftime('%Y-%m-%d %X', time.localtime())
        ]

    def on_result(self, result):
        if result:
            db_server.data2DB(data=result)
        else:
            print u'result-->return None'
