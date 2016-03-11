#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on:2016/3/4 14:46
# Project:temp_0


import requests as req
from pyquery.pyquery import PyQuery as pq

url_base = 'http://www.stylemode.com/fashion/fashionideas/'
url_pool = set()
url_had_crawled = set()
url_pool.add(url_base)


# page_turning
def page_turn(res):
    d = pq(res)
    for item in d('.pager.text-center.clearfix>a').items():
        url = item.attr('href')
        if not url == '#':
            url_pool.add(url)


# page crawling
def page_crawl():
    while len(url_had_crawled) < len(url_pool):
        url = url_pool.difference(url_had_crawled).pop()
        res = req.get(url).text
        page_turn(res)
        # TODO
        print page_parse(res)
        url_had_crawled.add(url)


def page_parse(res):
    d = pq(res)
    fw = d('.clearfix.list-unstyled.list-content>li').items()
    return [
        {
            'title': t('img').attr('alt'),
            'src_image_href': t('img').attr('src'),
            'page_href': t('img-wrap').prev().attr('href'),
            'view_count': t('.icon:nth-child(1)').next().text(),
            'like_count': t('.icon:nth-child(2)').next().text(),
            'time': t('.option time').text()
        }
        for t in fw
        ]


if __name__ == '__main__':
    page_crawl()
