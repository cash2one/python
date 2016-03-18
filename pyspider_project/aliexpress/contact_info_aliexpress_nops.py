#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on:2016/3/16 14:36
# Project:contact_info_aliexpress
# Author:yangmingsong

from ms_spider_fw.DBSerivce import DBService
from pyquery.pyquery import PyQuery
from Queue import Queue
import requests
import time
import re
import json
import threading
import random

pat = re.compile('<th>(.+?)</th>.*?<td>(.+?)</td>', re.DOTALL)

# config_text
db_name = 'alibaba'
table_name = 'contact_info_aliexpress'
table_title = 'shop_url,contact_detail,crawl_time'
connect_dict = {
    'host': '10.118.187.12',
    'user': 'admin',
    'passwd': 'admin',
    'charset': 'utf8'
}

proxy_api_config = {
    1: 'http://www.wy96.com/api.asp?key=20160318103618532&getnum=20&notport=8088&'
       'anonymoustype=3&filter=1',
    2: 'http://qsdrk.daili666api.com/ip/?tid=557893998216459&num=20&sortby=time'
}

queue_proxy = Queue(0)

db_server = DBService(dbName=db_name, tableName=table_name, **connect_dict)

_headers = {
    'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'
}


def crawled_urls():
    if not db_server.isTableExist():
        db_server.createTable(tableTitle=table_title.split(','))
        return []
    else:
        return map(
                lambda x: x.rsplit('/', 1)[0] + '/contactinfo/' + x.rsplit('/', 1)[1] + '.html',
                map(lambda x: x[0], db_server.getData(var='shop_url'))
        )


def gen_url():
    def url_join(t):
        if '.html' in t:
            return None
        else:
            temp = t.rsplit('/', 1)
            return temp[0] + '/contactinfo/' + temp[1] + '.html'

    def change_par(x):
        if '//www' in x:
            return url_join(x)
        elif '//pt' in x:
            return url_join(x.replace('//pt', '//www'))
        elif '//ru' in x:
            return url_join(x.replace('//ru', '//www'))
        elif '//es' in x:
            return url_join(x.replace('//es', '//www'))
        else:
            return None

    db_g = DBService(dbName=db_name, tableName='aliexpress_temp', **connect_dict)
    href_list_t = db_g.getData(var='store_href', distinct=True)
    href_s = map(
            lambda t: change_par(t), map(
                    lambda x: x[0], href_list_t
            )
    )
    return list(set(filter(lambda x: 1 if x else 0, href_s)))


def proxy_api():
    while True:
        api_url = proxy_api_config.get(random.randint(1, len(proxy_api_config)))
        ip_total_i = requests.get(api_url).text
        for proxy in list(set(filter(lambda x: 1 if x else 0, ip_total_i.split('\r\n')))):
            queue_proxy.put(proxy)
        time.sleep(5)


def download_page(url):
    def proxy():
        p = queue_proxy.get()
        if p: return p
        time.sleep(1)
        proxy()

    t = proxy()
    print t
    proxy_0 = 'http://%s' % t
    proxy_t = {'http': proxy_0}
    header = _headers
    header = dict(
            header.items() + {'Referer': url.replace('contactinfo/', '').replace('.html', '')}.items()
    )
    response = requests.get(url, proxies=proxy_t, headers=header, verify=False, timeout=3)
    return response.content


def __page_parse(content, url):
    d = PyQuery(content)
    shop_name = d.find('.shop-name>a').text()
    shop_years = d.find('.shop-time>em').text()
    open_time = d.find('.store-time>em').text()
    contact_person = d.find('.contactName').text()
    contact_block = d.find('.box.block.clear-block').html()
    contact_detail = re.findall(pat, contact_block)
    crawl_time = time.strftime('%Y-%m-%d %X', time.localtime())
    return [
        url.replace('contactinfo/', '').replace('.html', ''),
        json.dumps(
                dict([
                         ('shop_name', shop_name),
                         ('contact_url', url),
                         ('shop_years', shop_years),
                         ('open_time', open_time),
                         ('contact_person', contact_person)
                     ] + contact_detail)
        ),
        crawl_time
    ]


def page_parse(url):
    content = download_page(url)
    return __page_parse(content, url)


if __name__ == '__main__':
    queue_urls = Queue(0)
    queue_status = Queue(0)
    crawled_url = crawled_urls()
    gen_urls = gen_url()
    url_start = list(set(gen_urls).difference(set(crawled_url)))
    for url in url_start:
        queue_urls.put(url)


    def _run():
        while queue_urls.qsize():
            url = queue_urls.get()
            try:
                page_data = page_parse(url)
                print page_data
                db_server.data2DB(data=page_data)
            except Exception, e:
                print e.message
                queue_urls.put(url)
                queue_status.put('err')
                # if queue_status.qsize()%66=


    def run(thread_count):
        thread_pool = []
        proxy_thread = threading.Thread(
                target=proxy_api
        )
        thread_pool.append(proxy_thread)
        while thread_count > 0:
            thread_pool.append(threading.Thread(target=_run))
            thread_count -= 1
        for tsk in thread_pool:
            tsk.start()
        for tsk in thread_pool:
            tsk.join()


    run(20)
