#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-12-22 16:01:24
# Project: youku

from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.youku.com/v/', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('.item.item-moreshow>ul>li>a').items():
            self.crawl(each.attr.href, callback=self.in_page)

    @config(age=10 * 24 * 60 * 60, priority=3)
    def in_page(self, response):
        # for each in response.doc('.p-meta.pa').items():
        #     self.crawl(each.attr.href,callback=self.step_second)
        for each in response.doc('.yk-filter-panel div:nth-child(2) a').items():
            self.crawl(each.attr.href, callback=self.in2_page)

    @config(age=10 * 24 * 60 * 60, priority=3)
    def in2_page(self, response):
        print(response.doc('.p-meta-title>a'))
        if response.doc('.p-meta-title>a'):
            for each in response.doc('.p-meta-title>a').items():
                self.crawl(each.attr.href, callback=self.detail_page)
        elif response.doc('.v-meta-title>a'):
            for each in response.doc('.v-meta-title>a').items():
                self.crawl(each.attr.href, callback=self.detail_page)
        else:
            pass
        for each in response.doc('.yk-pages>li>a').items():
            self.crawl(each.attr.href, callback=self.in2_page)

    @config(priority=3)
    # if using this function,result was handled by pyspider(json)
    def detail_page(self, response):
        name=response.doc('.name').text() if response.doc('.name').text() else response.doc('.base_info>.title').text()
        comment=response.doc('.comment').text() if response.doc('.comment').text() else response.doc('#videoTotalComment').text()
        play=response.doc('.play').text() if response.doc('.play').text() else response.doc('#videoTotalPV>em').text()
        return {
            "name": name,
            "rate": response.doc('.row1.rate .num').text(),
            "alias": response.doc('.alias').text(),
            "pub": response.doc('.row2 .pub:nth-child(1)').text(),
            "youku_pub": response.doc('.row2 .pub:nth-child(2)').text(),
            "area": response.doc('.area').text(),
            "type": response.doc('.row2 .type').text(),
            "director": response.doc.attr('title'),
            "actor": response.doc('.actor a').text(),
            "play": play,
            "comment": comment,
            "increm": response.doc('.increm').text(),
            "basenotice": response.doc('.basenotice').text()
        }

    # TODO:for result store to mysql
    def detail_page_mysql(self,response):
        pass

    # TODO:over_ride method,for result store to mysql
    # def on_result(self, result):
    #     pass

if __name__ == '__main__':
    H = Handler()
    H.on_start()
