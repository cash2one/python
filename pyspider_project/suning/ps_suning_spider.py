#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on:2016/1/15 11:11
# Project:ps_suning_spider
# Author:yangmingsong

from pyspider.libs.base_handler import *
from ms_spider_fw.DBSerivce import DBService
import sys
import time

reload(sys)
sys.setdefaultencoding('utf8')

# config_text
db_name = 'platform_data'
table_name = 'suning'
table_title = 'product_url,catalogue,sub_catalogue,product_title,promotion_desc,origin_price,price,' \
              'product_stars,comment_count,sending_service,other_service,product_params,shop_name,' \
              'shop_href,product_rating,product_rating_avg,serice_rating,service_rating_avg,express_rating,' \
              'express_rating_avg,com_name_tel,crawl_time'
url_start = 'http://www.suning.com/emall/pgv_10052_10051_1_.html'  # start url for crawl,string
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

    @config(age=2 * 24 * 60 * 60)
    def step_first(self, response):
        d = response.doc
        for t in d('.listLeft>dl>dd>span>a').items():
            self.crawl(t.attr.href, callback=self.step_second)
        for x in d('.listRight>dl>dd>span>a').items():
            self.crawl(x.attr.href, callback=self.step_second)

    @config(age=30 * 24 * 60 * 60)
    def step_second(self, response):
        d = response.doc
        for t in d('.i-name .sellPoint').items():
            self.crawl(t.attr.href, callback=self.my_result, fetch_type='js',
                       js_script="""function(){windows.scrollTo(0,document.body.scrollHeight);}""")
        for x in d('.snPages a').items():
            if x.text().decode().isnumeric():
                self.crawl(x.attr.href, callback=self.step_second)

    @config(priority=2)
    def my_result(self, response):
        d = response.doc

        # inner fuction
        def thr_meta(m):
            return m if m else map(lambda x: '-', range(len(m)))

        def judge(x):
            return '-' if 'lower' in x else ''

        def price(p):
            pri = ''
            try:
                pri = p.split(' ')[1] + p.split(' ')[2] if len(p) > 2 else ''
            except IndexError:
                pri = p.split(' ')[1] if len(p) > 2 else ''
            finally:
                return pri

        rating_score = [t.text() for t in d('.clearfix>li .rating-val').items()]
        rating_score = thr_meta(rating_score)
        rating_icon = [t.attr('class') for t in d('.clearfix>li .si-icon').items()]  # for judge minus or other
        rating_icon = thr_meta(rating_icon)

        try:
            p_rating, s_rating, e_rating = rating_score[0], rating_score[3], rating_score[6]
            p_rating_avg, s_rating_avg, e_rating_avg = \
                map(lambda x: x[0] + x[1],
                    zip(map(judge, rating_icon), [rating_score[2], rating_score[5], rating_score[8]]))
        except IndexError:
            try:
                p_rating, s_rating, e_rating = rating_score[1][:-2], rating_score[3][:-2], rating_score[5][:-2]
                p_rating_avg, s_rating_avg, e_rating_avg = \
                    map(lambda x: x[0] + x[1],
                        zip(map(judge, rating_icon), [rating_score[2], rating_score[4], rating_score[6]]))
            except IndexError:
                p_rating = '|'.join(rating_score + rating_icon)
                p_rating_avg, s_rating, s_rating_avg, e_rating, e_rating_avg = ('-', '-', '-', '-', '-')

        pp_t1 = map(lambda x: x.text() if not x('span') else x('span').text(),
                    d('.procon-param td:nth-child(1)').items())
        pp_t2 = [t.text() for t in d('.procon-param td:nth-child(2)').items()]
        pp = zip(pp_t1, pp_t2)
        product_params = '+-+'.join(map(lambda x: x[0] + ":" + x[1], pp))

        promotion_price = d('#promotionPrice').text() if d('#promotionPrice').text() else d('#promoPrice').text()

        return [
            response.url,  # product url
            d('#category1').text(),  # main category
            d('.dropdown-text a').text(),  # sub category
            d('.proinfo-title>h1').text(),  # product title
            d('.proinfo-title>h2').text(),  # promotion describe
            price(d('#netPrice>del').text()),  # origin price
            price(promotion_price),
            d('.stars+span').text().split(' ')[0],  # product stars
            d('.totalReview').text().split(' ')[0],  # comment count
            d('#shopName').text(),  # sending service
            # other service
            '|'.join([t.text() for t in d('.proinfo-serv span').items() if not t.attr('style')]),
            product_params,
            d('#curShopName>a').text(),  # shop name
            d('#curShopName>a').attr.href,  # shop href
            p_rating,
            p_rating_avg,
            s_rating,
            s_rating_avg,
            e_rating,
            e_rating_avg,
            d('.detail-val').text(),  # company name and telephone
            time.strftime('%Y-%m-%d %X', time.localtime())
        ]

    # over ride method for result store to mysql
    def on_result(self, result):
        if result:
            db_server.data2DB(data=result)
        else:
            print u'result-->return None'
