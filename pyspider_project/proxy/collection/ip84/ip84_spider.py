#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on:2016/3/18 17:04
# Project:ip84_spider
# Author:yangmingsong

import urlparse
import requests
import threading
import re
from pyquery.pyquery import PyQuery
from Queue import Queue

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
    }
}

pattern_ip_address = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')
IP_addres_queue = Queue(0)


class Down_Loader(threading.Thread):
    def __int__(self, url_start):
        threading.Thread.__init__(self)
        self.url_start = url_start
        print self.url_start
        # self.thread_count = thread_count
        # initialization
        self.css = config_dictionary.get(self.url_start).get('css_selector_url')
        self.url_parse_d = urlparse.urlparse(url_start)._asdict()
        self.url_base = urlparse.urljoin(
                self.url_parse_d.get('scheme')
                , self.url_parse_d.get('netloc')
        )
        self.url_pool = set(list().append(self.url_start))
        self.url_pool_crawled = set()
        self.max_page = config_dictionary.get(self.url_start).get('max_page_count')
        self.lock = threading.Lock()

    def _stop_crawl(self):
        if self.max_page:
            if len(self.url_pool_crawled) >= self.max_page \
                    or len(self.url_pool) == len(self.url_pool_crawled):
                return True
        else:
            if len(self.url_pool) == len(self.url_pool_crawled):
                return True
        return False

    def _download(self):
        while not self._stop_crawl():
            url = self.url_pool.difference(self.url_pool_crawled).pop()
            try:
                r = requests.get(url)
                self.lock.acquire()
                self.url_pool_crawled.add(url)
                self._parse(r, url)
            except Exception, e:
                print e.message
                self.url_pool.add(url)
            finally:
                self.lock.release()

    def _parse(self, response, url):
        d = PyQuery(response)
        # page_turning
        new_url = map(lambda u: urlparse.urljoin(self.url_base, u),
                      map(lambda x: x.attr('href'),
                          d.find(self.css).items()
                          )
                      )
        self.url_pool.union(set(new_url))
        # IP address extracting
        rst = ':'.join(d.text().split(' '))
        proxy_list = re.findall(pattern_ip_address, rst)
        print proxy_list
        IP_addres_queue.put((proxy_list, url))

    def run(self):
        # t_p = []
        # while self.thread_count > 0:
        #     t_p.append(threading.Thread(target=self._download))
        #     self.thread_count -= 1
        # for tsk in t_p:
        #     tsk.start()
        # for tsk in t_p:
        #     tsk.join()
        self._download()

def proxies_collect():
    thread_pool = []
    for url in config_dictionary.keys():
        thread_pool.append(Down_Loader(args=(url)))
    for tsk in thread_pool:
        tsk.start()
    for tsk in thread_pool:
        tsk.join()


if __name__ == '__main__':
    proxies_collect()
