#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on:2016/3/18 17:04
# Project:ip84_spider
# Author:yangmingsong

import urlparse
import requests
from threading import Thread
import re
from pyquery.pyquery import PyQuery
from Queue import Queue
import threading

# config text match to each proxy website
# make sure the website contain proxy_port in base page_source
config_dictionary = {
    'http://www.ip84.com/gw': {
        'css_selector_url': '.pagination>a',
        'basejoin': True,
        'max_page_count': 50
    },
    'http://www.ip84.com/gn': {
        'css_selector_url': '.pagination>a',
        'basejoin': True,
        'max_page_count': 50
    },
    "http://www.ip84.com/pn": {
        'css_selector_url': '.pagination>a',
        'basejoin': True,
        'max_page_count': 50
    },
    "http://www.mimiip.com/gngao/1": {
        'css_selector_url': '.pagination>a',
        'basejoin': True,
        'max_page_count': 50
    },
    "http://www.mimiip.com/gnpu/": {
        'css_selector_url': '.pagination>a',
        'basejoin': True,
        'max_page_count': 1
    },
    "http://www.mimiip.com/hw": {
        'css_selector_url': '.pagination>a',
        'basejoin': True,
        'max_page_count': 1
    }
}

# re pattern
pattern_ip_address = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d]):\d{1,5}')
# store result data , threading safe
proxy_port_queue = Queue(0)


class Down_Loader(Thread):
    def __init__(self, url_start, thread_num=3):
        Thread.__init__(self)
        self.__url_start = url_start
        self.thread_count = thread_num
        # initialization
        self.__css = config_dictionary.get(url_start).get('css_selector_url')
        self.__url_parse_d = urlparse.urlparse(url_start)._asdict()
        self.__url_base = self.__url_parse_d.get('scheme') + '://' \
                          + self.__url_parse_d.get('netloc')
        self.__url_pool = {url_start}
        # if python version is 2.6 , using next statement
        # self.__url_pool = set([url_start])
        self.__url_pool_crawled = set()
        self.__max_page = config_dictionary.get(url_start).get('max_page_count')

    def _stop_crawl(self):
        if self.__max_page:
            if len(self.__url_pool_crawled) >= self.__max_page \
                    or len(self.__url_pool) == len(self.__url_pool_crawled):
                return True
        else:
            if len(self.__url_pool) == len(self.__url_pool_crawled):
                return True
        return False

    def _download(self, lock):
        while not self._stop_crawl():
            lock.acquire()
            url = self.__url_pool.difference(self.__url_pool_crawled).pop()
            self.__url_pool_crawled.add(url)
            lock.release()
            print url
            r = None
            try:
                r = requests.get(url, timeout=1).content
            except Exception, e:
                print e.message
                self.__url_pool.add(url)
                # self.__url_pool_crawled.remove(url)
            if r: self._parse(r)

    def _parse(self, response):
        d = PyQuery(response)
        # page_turning
        __url = map(lambda x: x.attr('href'),
                    d.find(self.__css).items()
                    )
        if config_dictionary.get(self.__url_start).get('basejoin'):
            new_url = map(lambda u: urlparse.urljoin(self.__url_base, u), __url)
        else:
            new_url = __url
        self.__url_pool = self.__url_pool.union(set(new_url))
        # IP address extracting
        rst = ':'.join(d.text().split(' '))
        proxy_list = re.findall(pattern_ip_address, rst)
        proxy_port_queue.put((proxy_list, self.__url_base))

    def run(self):
        __thread_pool_inner = list()
        __lock = threading.Lock()
        while self.thread_count > 0:
            __thread_pool_inner.append(
                    threading.Thread(target=self._download, args=(__lock,))
            )
            self.thread_count -= 1
        for tsk in __thread_pool_inner:
            tsk.start()
        for tsk in __thread_pool_inner:
            tsk.join()


def __proxies_collect():
    thread_pool_outer = list()
    for url in config_dictionary.keys():
        thread_pool_outer.append(Down_Loader(url, 3))
    for tsk in thread_pool_outer:
        tsk.start()
    for tsk in thread_pool_outer:
        tsk.join()


def get_proxies_from_website():
    __proxies_collect()
    rst_proxy = list()
    while proxy_port_queue.qsize():
        rst_proxy += proxy_port_queue.get()[0]
    return list(set(rst_proxy))


if __name__ == '__main__':
    # proxy_port_list = get_proxies_from_website()
    # for proxy_port in proxy_port_list:
    #     print proxy_port
    with open('ms_proxy_config','wb')as f:
        f.write('yes,it,is my config text')