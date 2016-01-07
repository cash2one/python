#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on:2016/1/7 10:17
# Project:spider_third_page
# Author:yangmingsong

from pyquery import PyQuery as pq
from ms_spider_fw.downLoad import DownLoad_noFollow as DBN
from ms_spider_fw.DBSerivce import DBService
from ms_spider_fw.parser.PageParser import PageParser
import time
from selenium.webdriver import Firefox

DB = DBService(dbName='alibaba', tableName='alibaba_cow_powder_3')


def gen_url():
    DB = DBService(dbName='alibaba', tableName='alibaba_cow_powder_3')
    url_detail_page = DB.getData(var='credit_detail_href', distinct=True)
    urls = map(lambda x: x[0] if x else ' ', url_detail_page)
    url = []
    for t in urls:
        if t:
            url.append(t)
    return url


def gen_url_contactinfo():
    urls_begin = gen_url()
    return map(lambda x: [x] + [x.replace('creditdetail', 'contactinfo')], urls_begin)


def get_parser(url, driver):
    import random
    time.sleep(abs(random.gauss(5, 5)))
    driver.get(url)
    print(driver.title)
    contacts_name = '-'
    contacts_sex = '-'
    contacts_job = '-'
    try:
        contacts_name = driver.find_element_by_css_selector('.contact-info .membername').text
        contacts_sex = driver.find_element_by_css_selector('.contact-info>dl>dd').text.split(' ')[1]
        contacts_job = driver.find_element_by_css_selector('.contact-info>dl>dd').text.split('（')[1]
        contacts_job = contacts_job.split('）')[0]
    except:
        pass
    phone_frames = driver.find_elements_by_css_selector('.contcat-desc dl')
    cell_phone = '-'
    tel_phone = '-'
    fax_phone = '-'
    shop_addr = '-'
    for i in range(len(phone_frames)):
        text = driver.find_element_by_css_selector(".contcat-desc dl:nth-child(" + str(i + 1) + ") dt").text.strip()
        if text == u'移动电话：':
            cell_phone = driver.find_element_by_css_selector(".contcat-desc dl:nth-child(" + str(i + 1) + ") dd").text
            continue
        elif text == u'电      话：':
            tel_phone = driver.find_element_by_css_selector(".contcat-desc dl:nth-child(" + str(i + 1) + ") dd").text
            continue
        elif text == u'传      真：':
            fax_phone = driver.find_element_by_css_selector(".contcat-desc dl:nth-child(" + str(i + 1) + ") dd").text
            continue
        elif text == u'地      址：':
            shop_addr = driver.find_element_by_css_selector(".contcat-desc dl:nth-child(" + str(i + 1) + ") dd").text
            continue
    spider_time = time.strftime("%Y-%m-%d %X", time.localtime())
    result = [contacts_name, contacts_sex, contacts_job, cell_phone, tel_phone, fax_phone, shop_addr, spider_time, url]
    DB = DBService(dbName='alibaba', tableName='alibaba_cow_powder_phone')
    DB.data2DB(data=result)


def temp_main():
    urls = map(lambda x: x[1], gen_url_contactinfo())
    urls = map(lambda x: x + '?spm=a2615.7691481.0.0.OCyk7j', urls)
    driver = Firefox()
    driver.maximize_window()
    for url in urls:
        print(url)
        get_parser(url, driver)


# class Dler(DBN.DownLoadBase):
#     def __init__(self):
#         DBN.DownLoadBase.__init__(self)
#
#     def startUrlList(self):
#         return map(lambda x: x[1], gen_url_contactinfo())
#
#
# class PPer(PageParser):
#     def __init__(self, pageSource):
#         PageParser.__init__(self, pageSource=pageSource)
#
#     def pageParser(self):
#         res = []
#         d = self.d
#         print(d.find('title').text())
#         contact_name=d.find('.contact-info .membername').text()
#         contacts_sex=d.find('.contact-info .membername').next().text()
#         print contact_name,contacts_sex
#         return res
#
#
# def spiderMain():
#     dler = Dler()
#     dler.downLoad(10)
#
#     # DB = DBService(dbName='alibaba', tableName='alibaba_cow_powder_contactinfo')
#     # DB.createTable(tableTitle=[])
#
#     while True:
#         que = DBN.queueForDownLoad
#         if not que.empty():
#             url, src = que.get()
#             pPer = PPer(src)
#             temp = pPer.pageParser()
#             if temp:
#                 temp = map(lambda x: x + [url], temp)
#                 # DB.data2DB(data=temp)
#                 print(u'++成功:%s' % url)
#             else:
#                 print(u'--失败:%s' % url)
#         else:
#             time.sleep(1)


if __name__ == '__main__':
    DB = DBService(dbName='alibaba', tableName='alibaba_cow_powder_phone')
    DB.createTable(tableTitle=['contacts_name', 'contacts_sex', 'contacts_job', 'cell_phone', 'tel_phone', 'fax_phone',
                               'shop_addr', 'spider_time', 'url'])
    temp_main()
