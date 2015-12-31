#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on:2015/12/31 16:39
# Project:comment_page
# Author:yangmingsong

import urllib, random
import time
from ms_spider_fw.downLoad import DownLoad_noFollow as DBN
from ms_spider_fw.parser.PageParser import PageParser

def gen_url(user_id='UvCHyvFvGMCkSvNTT', page_count=4):
    """
    par_id:user_id should be given
    page_count:int,should be <=4 but >=0
    """
    url_base = 'https://rate.taobao.com/member_rate.htm?'
    t = []
    for c in range(1, page_count + 1, 1):
        par_s = [
            ('_ksTS', str(int(time.time() * 1000)) + '_' + str(random.randint(100, 999))),  # time_stamp
            ('callback', 'shop_rate_list'),
            ('content', 1),
            ('result', ''),
            ('from', 'rate'),
            ('user_id', user_id),
            ('identity', 2),
            ('rater', 0),
            ('direction', 0),
            ('page', c)
        ]
        t.append(urllib.urlencode(par_s))
    for temp in map(lambda x: url_base + x, t):
        print(temp)
    return map(lambda x: url_base + x, t)

class Dler(DBN.DownLoadBase):
    def __init__(self):
        DBN.DownLoadBase.__init__(self)

    def startUrlList(self):
        return gen_url()

class PPer(PageParser):
    def __init__(self, pageSource):
        PageParser.__init__(self, pageSource=pageSource)

    def pageParser(self):
        d=self.d.content()
        print(d)

def spiderMain():
    dler = Dler()
    dler.downLoad(1)
    while True:
        que = DBN.queueForDownLoad
        if not que.empty():
            url, src = que.get()
            print(src)

if __name__=='__main__':
    spiderMain()