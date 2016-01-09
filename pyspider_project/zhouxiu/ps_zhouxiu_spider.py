#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on:2015/12/24 11:06
# Project:zhou_xiu_product
# Author:yangmingsong

from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.xiu.com/brand.html', callback=self.index_page)

    # @config(age=10 * 24 * 60 * 60, priority=3)
    def index_page(self, response):
        d = response.doc
        for temp in d('.brand_top_menu a').items():
            self.crawl(temp.attr.href, callback=self.product_page)

    # @config(age=10 * 24 * 60 * 60, priority=3)
    def product_page(self, response):
        d = response.doc
        for temp in d('h2+dl>dd>a').items():
            self.crawl(temp.attr('href'), callback=self.in_page)

    # noinspection PyMethodMayBeStatic
    def detail_page(self, response):
        d = response
        return {
            'res': [{
                        "name": di('.tit>a').text(),
                        "brand": di('.tit>span').text(),
                        "product_url": di.find('.pic>a').attr('href'),
                        "size": di('.ssl_item>span').text(),
                        "showprice": di('.showprice').text(),
                        "delprice": di('.delprice').text()
                    }
                    for di in d('.item').items()]
        }

    # @config(age=10 * 24 * 60 * 60, priority=3)
    def in_page(self, response):
        d = response.doc
        # for temp in d('.item').items():
        #     self.on_result(self.detail_page(temp))
        # self.on_result(self.detail_page(d))

        res = self.detail_page(d)
        for item in res['res']:
            self.on_result(item)

        for temp in d('.Pagenum>a').items():
            if 'javascript' in temp.attr.href:
                continue
            else:
                self.crawl(temp.attr.href, callback=self.in_page)

    # TODO:for result store to mysql
    def detail_page_mysql(self, response):
        pass

    # TODO:over_ride method,for result store to mysql
    # def on_result(self, result):
    #     pass
