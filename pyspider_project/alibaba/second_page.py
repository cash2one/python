#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on:2016/1/6 19:08
# Project:pagecount_info
# Author:yangmingsong
import urllib
from pyspider.libs.base_handler import *


def gen_url(path=r'd:/spider/pagecount.csv'):
    def inner_gen_url(x):
        url = []
        for t in range(2, x[1] + 1):
            url_base = x[0]
            url_par = [
                ('beginPage', t),
                ('offset', 0)
            ]
            url.append(url_base + '#' + urllib.urlencode(url_par))
        return url

    with open(path) as f:
        t = f.readlines()
    t = map(lambda x: x.strip().split(','), t[1:])
    t = [item for item in t if item[1] and int(item[1]) >= 60]
    t = [(item[0], item[-1]) for item in map(lambda x: x + [int(x[1]) / 60 + 1], t)]
    t = map(lambda x: (x[0], 100) if x[1] > 100 else x, t)
    t = map(inner_gen_url, t)
    return reduce(lambda x, y: x + y, t)


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl(gen_url(), callback=self.my_result)

    def my_result(self, response):
        d = response
        return {
            'page_count': d('.sm-widget-offer>em').text()
        }


if __name__ == '__main__':
    for item in gen_url():
        print(item)
