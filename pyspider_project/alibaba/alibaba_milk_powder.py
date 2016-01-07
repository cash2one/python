#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on:2016/1/6 15:24
# Project:alibaba_cow_powder
# Author:yangmingsong

from pyspider.libs.base_handler import *
from myTool.myProxy import proxyExistsAll
import urllib
import sys

reload(sys)
sys.setdefaultencoding('utf8')


def gen_url():
    def kw_template():
        kw = u'荷兰牛栏 德国爱他美 荷兰美素 惠氏 德国喜宝有机 德国喜宝益生菌 德国特福芬 澳洲可瑞康 新西兰A2  雅培  ' \
             u'英国惠氏 英国牛栏 英国爱他美  新西兰可瑞康 澳洲贝拉米 阿拉欧 Nannycare 日本明治 澳洲爱他美 Nutrilon ' \
             u'SIMILAC 多美滋 Guigoz 美赞臣 意大利爱他美 桂格 固力果 德国凯莉泓乐 plasmon 意大利美林 澳滋 德国牛栏 ' \
             u'美素佳儿 VIPLUS  安满 campina 卡瑞特滋   安佳 纽优乳  kinfield'
        return list(set([i.encode('GBK') for i in kw.split(' ') if i]))

    k_w = kw_template()
    url_base = "http://s.1688.com/selloffer/offer_search.htm?"
    url_par = [[('uniqfield', 'pic_tag_id'),
                ('keywords', t),
                ('earseDirect', 'false'),
                ('showStyle', 'img'),
                ('n', 'y')] for t in k_w
               ]
    # other method
    # url_par_2 = map(lambda par: '&'.join(map(lambda inner: '='.join(inner), par)), url_par)
    # urls = [url_base + item for item in url_par_2]
    return [url_base + urllib.urlencode(par) for par in url_par]


def my_proxy():
    p_p=proxyExistsAll(path='/home/appdeploy/613108/proxy')
    # p_p = proxyExistsAll()
    proxy_port = map(lambda x: ':'.join(x[:-1]), p_p)
    return proxy_port


class Handler(BaseHandler):
    crawl_config = {
        'proxy': my_proxy()
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl(gen_url(), callback=self.index_page, fetch_type='js', timeout=8,
                   js_script=
                   """
                    function(){
                        windows.scrollTo(0,document.body.scrollHeight);
                    }"""
                   )

    def index_page(self,response):
        d=response.doc
        self.on_result(self.my_result(d))
        for t in d('.fui-paging-list a').items():
            self.crawl(t.attr('href'),callback=self.index_page)

    def my_result(self,response):
        d=response
        return {
            'res':[{
                'company_name':di('div:nth-child(2) a:nth-child(2)').text()
            } for di in d('.sm-offerimg-company').items()]
        }


if __name__ == '__main__':
    print gen_url()
