#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on:2016/1/11 18:45
# Project:ps_okbuy_spider
# Author:yangmingsong

from pyspider.libs.base_handler import *
from ms_spider_fw.DBSerivce import DBService
import urlparse
import time

# config text
db_name = 'industry_data__clothes_shoes'  # database name for store data
table_name = 'okbuy'  # table name for store data
table_title = 'catalog,product_name,product_url,brand_name,price,discount,origin_price,color_list,' \
              'size_list,comment_count,collection_count,product_parameters,crawl_time'
url_start = 'http://www.okbuy.com/brand/brandcat'  # start url for crawl
connect_dict = {'host': '10.118.187.12', 'user': 'admin', 'passwd': 'admin', 'charset': 'utf8'}

# script
db_server = DBService(dbName=db_name, tableName=table_name, **connect_dict)
if not db_server.isTableExist():
    db_server.createTable(tableTitle=table_title.split(','))


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl(url_start, callback=self.step_first)

    @config(age=10 * 24 * 60 * 60)
    def step_first(self, response):
        url_base = 'http://www.okbuy.com/'
        for each in response.doc('.t-abcconr-new>a').items():
            t = urlparse.urlparse(each.attr.href)
            url = urlparse.urljoin(url_base, t.path)
            self.crawl(url, callback=self.step_second)

    def step_second(self, response):
        d = response.doc
        for t in d('.frame .altName>a').items():
            self.crawl(t.attr.href, callback=self.my_result, fetch_type='js',
                       js_script="""function(){windows.scrollTo(0,document.body.scrollHeight);}""")
        for n in d('#bottom_pagenum>span>a').items():
            self.crawl(n.attr.href, callback=self.step_second)

    @config(priority=2)
    def my_result(self, response):
        # inner function for extract 'color'discribe text in list object
        def extract_color(lst):
            if not isinstance(lst, list):
                return ''
            else:
                for item in lst:
                    if u'色' in item:
                        return item
            return ''

        d = response.doc
        try:  # used for extract product parameters
            pdt_pars_tle = d('.prInfoTable>tbody>tr>th').text().split(' ')
            if u'季节：' in pdt_pars_tle:
                pdt_pars_tle.remove(u'季节：')
            pdt_pars_dtl = d('.prInfoTable>tbody>tr>td').text().split(' ')
            pdt_pars = '|'.join(map(lambda x: x[0] + x[1], zip(pdt_pars_tle, pdt_pars_dtl)))
        except:
            pdt_pars = ''
        return [
            '|'.join(d('.prodConTopInTit>p>a').text().split(' ')[:-1]),  # catalogue name
            d('.prodAllName').text(),  # product full name
            response.url,  # product url
            d('.prodbrandlink>a').text(),  # brand name
            d('#prodPriceAj').text(),  # product price
            d('#prodDiscount').text(),  # product discount
            d('#prodPriceOffl').text(),  # origin price
            # use inner function 'extract_color' to extract colos info , join color list with '|'
            '|'.join([extract_color(t.attr['alt'].split('-')) for t in d('.prodColorImg img:nth-child(1)').items()]),
            '|'.join([t.text() for t in d('#sizeList .text').items()]),  # product size list,join with '|'
            d('#prodallCom>span').text(),  # comment number
            d('#prodspan').text()[:-3],  # how many people like this
            pdt_pars,
            time.strftime('%Y-%m-%d %X', time.localtime())
        ]

    # over ride method for result store to mysql
    def on_result(self, result):
        if result:
            db_server.data2DB(data=result)
        else:
            print u'result-->return None'
