#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on:2015/12/24 11:06
# Project:zhouxiutest
# Author:yangmingsong

from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=3 * 60 + 10)
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

    # @config(age=10 * 24 * 60 * 60, priority=3)
    # noinspection PyMethodMayBeStatic
    def detail_page(self, response):
        d = response
        return {
            "name": d('.tit>a').text(),
            "brand": d('.tit>span').text(),
            "product_url": d.find('.pic>a').attr('href'),
            "size": d('.ssl_item>span').text(),
            "showprice": d('.showprice').text(),
            "delprice": d('.delprice').text()
        }

    # override
    def on_result(self, result):
        """Receiving returns from other callback, override me."""
        if not result:
            return
        assert self.task, "on_result can't outside a callback."
        if self.is_debugger():
            # pprint(result)
            temp=({"product_url":result['product_url']}, result)
            print(temp)
        if self.__env__.get('result_queue'):
            temp=(self.task, result)
            print self.task
            self.__env__['result_queue'].put(temp)

    # @config(age=10 * 24 * 60 * 60, priority=3)
    def in_page(self, response):
        d = response.doc
        i=1
        for temp in d('.item').items():
            self.on_result(self.detail_page(temp))
            if i==1:
                # print self.__env__get('result_queue')
                pass
            i+=1
        for temp in d('.Pagenum>a').items():
            if 'javascript' in temp.attr.href:
                continue
            else:
                self.crawl(temp.attr.href, callback=self.in_page)
