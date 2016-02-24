#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on:2016/2/23 10:31
# Project:temp
# Author:yangmingsong

import requests as req
import re
from pyquery.pyquery import PyQuery
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')

pat_page_config = re.compile('pageConfig = (.+?);', re.DOTALL)
pat_word = re.compile('\w+:')
pat_score = re.compile('<span class="score-desc">(.+?)<.+?"number">(.+?)<.+?<'
                       'i class="(\w+?)">.+?"percent">(.+?)<', re.DOTALL)
pat_par = re.compile('<li title=.+?>(.+?)</li>')

res_t = req.get('http://item.jd.com/1290976.html')
txt = res_t.text
d = PyQuery(txt)

data_temp = re.findall(pat_page_config, txt)[0]
data = re.sub('\s+', '', data_temp)
data = data.replace("'", '"')
data_sub = re.findall(pat_word, data)
for w in data_sub:
    if w == 'http:':
        continue
    else:
        temp = data.replace(w, '"' + w[:-1] + '"' + ':')
        data = temp
data=json.loads(data)

temp = list(d('.breadcrumb a').items())[:-1]
cate = {temp.index(t): t.text() for t in temp}

temp = list(d('.lh>li img').items())
img_src = {temp.index(t): t.attr('src') for t in temp}

temp = list(d('.label+.text').items())
template={0:'com_name',1:'addr'}
com_info = {template[temp.index(t)]: t.text() for t in temp}
shop_info={'shop_name':d('.name').attr('title'),'shop_href':d('.name').attr('href')}
shop=dict(com_info.items()+shop_info.items())

score_total = {'score_sum': d('.score-sum a').text()}
score_detail = re.findall(pat_score, txt)
score_detail = {t[0]: {'score': t[1], 'up_down': t[2], 'rate': t[3]} for t in score_detail if len(t) == 4}
score = dict(score_total.items() + score_detail.items())

product_parameters_t=re.findall(pat_par, txt)
product_parameters={t.split('：',1)[0]:t.split('：',1)[1] for t in product_parameters_t}

detail = {'catagory': cate, 'image_src': img_src, 'shop_com_information': shop, 'score_detail': score,
                  'product_parameters': product_parameters,'sku_info':data}

print json.dumps(detail)