#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on:2016/1/5 14:56
# Project:tmall_target_shop_comment
# Author:yangmingsong

from pyspider.libs.base_handler import *
import time, random, urllib


def gen_url(user_id='UvCNyMG8bvFILMQTT', page_count=4):
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
    return map(lambda x: url_base + x, t)


def list2dict():
    dic = {}
    with open('/home/appdeploy/613108/tmall/cookies/cookies.txt') as f:
        # with open(r'D:\spider\tmall\cookeis\cookies.txt') as f:
        t = f.readlines()
    for tt in t:
        dic[tt.split('\t')[-2]] = tt.split('\t')[-1][:-1]
    return dic


class Handler(BaseHandler):
    crawl_config = {
        # 'headers': {
        #     'User-Agent': 'User-Agent:Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'
        # },
        # 'cookies': list2dict()
    }

    # def gen_url(self):
    #     pass

    def on_start(self):
        self.crawl(
            'http://rate.taobao.com/user-rate-UOmc0MCcYvFcL.htm', callback=self.index_page, fetch_type='js',
            js_script="""
            function(){
                windows.scrollTo(0,document.body.scrollHeight);
            }"""
        )

    def index_page(self):
        print self.response.content

if __name__=='__main__':
    H=Handler()
    H.on_start()