#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on:2016/2/23 17:45
# Project:temp
# Author:yangmingsong

from pyquery.pyquery import PyQuery as pq
import requests as req
url_test='http://www.suning.com/emall/pgv_10052_10051_1_.html'
d=pq(req.get(url_test).text)
cate={}
for t_0 in d('.listLeft').items():
    cate[t_0.prev().text()]={}
    for t_1 in t_0('dl').items():
        cate[t_0.prev().text()][t_1('dt a').text()]={}
        cate[t_0.prev().text()][t_1('dt a').text()]['id']=t_1('dt a').attr('id')
        i=0
        for t_2 in t_1('dd a').items():
            cate[t_0.prev().text()][t_1('dt a').text()][i]={}
            cate[t_0.prev().text()][t_1('dt a').text()][i]['name']=t_2.text()
            cate[t_0.prev().text()][t_1('dt a').text()][i]['id']=t_2.attr('id')
            i+=1

url_for_base_info='http://list.suning.com/emall/showProductList.do?ci=410504&pg=03&cp=3&il=0&iy=0&n=1&cityId=9051'