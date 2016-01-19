#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on:2016/1/8 14:13
# Project:ps_meitun_spider
# Author:yangmingsong

from pyspider.libs.base_handler import *
import sys
from ms_spider_fw.DBSerivce import DBService
import time
from selenium.webdriver import PhantomJS
from selenium.webdriver.common.action_chains import ActionChains
from pyquery import PyQuery as pq

reload(sys)
sys.setdefaultencoding('utf8')

db_server = DBService(dbName='industry_data__mon_baby', tableName='meitun', host='10.118.187.12',
                      user='admin', passwd='admin', charset='utf8')


# db_server.createTable(tableTitle=[
#     'product_url',
#     'product_title',
#     'price_del',
#     'discount',
#     'price_origin',
#     'sale',
#     # 'express_price',
#     'crawl_time'
# ])


def catalog_url(url='http://www.meitun.com/'):
    # catalog_url is AJAX,use phantomJS
    driver = PhantomJS()
    driver.get(url)
    driver.maximize_window()
    mov_ele = driver.find_element_by_css_selector('.nav>ul>li:nth-child(1)')
    # the mouse move to the lazy layout element,and perform
    ActionChains(driver).move_to_element(mov_ele).perform()
    time.sleep(3)
    response = driver.page_source
    driver.quit()
    # use pyquery parser the page source,more quickly
    d = pq(response)
    return map(lambda x: 'http:' + pq(x).attr('href'), d.find('.cg-pdts a'))


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl(catalog_url(), callback=self.step_first, fetch_type='js',
                   js_script="""function(){windows.scrollTo(0,document.body.scrollHeight);}""")

    # function for handle inner_framework using phantomJS
    @config(age=2 * 24 * 60 * 60)
    def on_start_again(self, url):
        driver = PhantomJS()
        driver.get(url)
        time.sleep(2)
        driver.maximize_window()
        t = driver.find_element_by_css_selector('.page-txt').text
        res_t = []
        if t:
            t = int(t.split('/')[1][:-1]) - 1  # get the page count
            # the count of page turning should be i-1
            while t:
                t -= 1
                move_ele = driver.find_element_by_css_selector('#next')
                ActionChains(driver).move_to_element(move_ele).click()
                time.sleep(1)
                res_t.append(driver.page_source)
        driver.quit()
        for item in res_t:
            self.step_first(item)

    @config(age=10 * 24 * 60 * 60)
    def step_first(self, response):
        try:
            d = response.doc
            if d('#next'):
                self.on_start_again(response.url)
            for t in d('.r1>a').items():
                url_t = t.attr('href')
                self.crawl(url_t, callback=self.my_result)
        # because function 'on_start_again' return is str,doesn`t have attr 'doc'
        except:
            temp = pq(response).find('.r1>a').items()
            for t in temp:
                url_t = 'http:' + pq(t).attr('href')
                self.crawl(url_t, callback=self.my_result)

    def my_result(self, response):
        d = response.doc
        return [
            response.url,  # page url
            d('.sname').text(),  # page title
            d('#meitun_pirce').text(),  # price sell
            d('.discount').text(),
            d('#basic_price').text(),  # oringin price
            d('.fcr').text(),  # sale count
            # d('.freight').text(),
            time.strftime('%Y-%m-%d %X', time.localtime())
        ]

    def on_result(self, result):
        if result:
            db_server.data2DB(data=result)
        else:
            print u'result-->return None'