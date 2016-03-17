#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on:2016/3/17 18:30
# Project:temp3
# Author:yangmingsong
import requests
from pyquery.pyquery import PyQuery

h = """Host: www.diytrade.com
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Referer: http://www.diytrade.com/china/main.html
Connection: keep-alive
If-Modified-Since: Thu, 17 Mar 2016 10:26:06 GMT
Cache-Control: max-age=0"""
_header = dict(map(lambda x: x.split(':', 1), h.split('\n')))

_response = requests.get(
        url='http://www.diytrade.com/china/pc.html',
        headers=_header
)

d = PyQuery(_response.content)
# keyword list
keyword_list = dict(map(lambda x: (x.text().strip(), x.attr('href')),
                        d.find('.hotKW>li>a').items()
                        )
                    )
