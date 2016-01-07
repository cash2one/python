#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on:2016/1/7 18:20
# Project:ps_beibei_spider
# Author:yangmingsong

from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.beibei.com/category/dress.html', callback=self.step_first)

    def step_first(self, response):
        # get the brand_list page url(attr) from brand_page
        d = response.doc
        for t in d('.sub-nav li>a').items():
            t_inner = t.attr('href')
            if 'category' in t_inner:
                self.crawl(t_inner, callback=self.step_second)

    def step_second(self, response):
        d = response.doc
        # TODO:analysy the begin page,use step_third function [done]

        # get the brand page url(attr) from brand_page
        for t in d('.brand-full>a').items():
            self.crawl(t.attr('href'), callback=self.step_third)

        # brand_page page turning
        for i in d('.brand-page>a').items():
            self.crawl(i.attr('href'), callback=self.step_second)

    def step_third(self, response):
        # get the product url(attr->href) from brand shop page
        d = response.doc
        for t in d('.view-ItemListItem>a').items():
            self.crawl(t.attr('href'), callback=self.my_result)

    def step_fourth(self, response):
        pass

    def my_result(self, response):
        # parser the product page and collect the product_info
        d = response.doc
        score = d('.eva-con>p>span').text().split(' ')
        return {
            'title': d('.title>h3').text(),
            'price_del': d('.pink .price').text(),
            'discount': d('.discount.view-SkuPriceDiscountInfo').text(),
            'price_origin': d('.market .strike').text(),
            'shopping_price': d('.view-ShippingFeeInfo').text(),
            'shopping_from': d('.p1').text(),
            'brand': d('.dec-con>p>span').text(),
            'score_total': score[0],
            'score_sending': score[1],
            'score_express': score[-1],
            # TODO
            'express_supplier': score
        }
