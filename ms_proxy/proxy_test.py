#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Rebuild on:2016/3/18 15:00
# Project:proxy_test
# Author:yangmingsong

import requests
import json
import re
from pyquery.pyquery import PyQuery as pq
from threading import Thread
from requests.auth import HTTPProxyAuth

P_A = HTTPProxyAuth('sfHoujt', 'sf654321')
patt_ip = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')


def original_ip_address():
    t = requests.get('http://httpbin.org/ip').text
    return json.loads(t).get('origin')


original = original_ip_address()


def test(proxy, **kwargs):
    """
    proxy_test the given proxy(single proxy be given) and port is ok,return true fo false
    :param proxy: ip address ; like '10.1.12.117' ;
    or it can be given like this '10.1.12.117:8080'
    :param kwargs:would be given as port number , timeout number
    :return: True or False

    Usage:
    test(proxy='12.1.1.1:8080')
    or
    test(proxy=12.1.1.113,port=9090,timeout=1)
    """

    if ':' in proxy:
        proxy_port = proxy
    elif 'port' in kwargs:
        port = kwargs.get('port')
        proxy_port = str(proxy) + str(port)
    else:
        raise ValueError('proxy or port not collect!')
    s = requests.Session()
    proxy_OK = {'http': 'http://%s' % proxy_port}

    try:
        res = s.get('https://list.tmall.com/search_product.htm?q=Q9197%B0%AE%D4%DE+%BA%FB%B5%FB%BD%E1%B4%CC%D0%E5%CF%B5%B4%F8%D0%D4%B8%D0%C7%E9%C8%A4%C4%DA%BF%E3+++++9197%D0%C2%B7%DB%C9%AB', proxies=proxy_OK, auth=P_A, timeout=kwargs.get('timeout'))
        print res.text[:500]
    except Exception, e:
        # print e.message
        return False

    ip_return = re.findall(patt_ip, res.text)
    if ip_return \
            and proxy.split(':')[0] == ip_return[0] \
            and len(ip_return) == 1 \
            and original not in ip_return \
            and len(res.text) < 100:
        return True

    return False


def _test(proxy, **kwargs):
    t = test(proxy, **kwargs.get('kwargs'))
    if t:
        return proxy
    return None


def test_from_url(url, timeout=1):
    """
    get proxy from given url address , and collect proxy and port ; then test them ;
    return a list of useful proxy_s
    :param url:
    :param timeout: second(s) , default 1 second
    :return:

    usage:
    url = 'http://www.ip84.com/pn'
    proxy_list = test_from_url(url)
    or like this: proxy_list = test_from_url(url , timeout=3)
    """
    patt_pp = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d]):\d{1,5}')
    t = requests.get(url, verify=True).text
    txt = ':'.join(pq(t).text().split(' '))
    proxy_port = list(set(re.findall(patt_pp, txt)))
    return test_from_list(proxy_list=proxy_port, timeout=timeout)


def test_from_list(proxy_list, timeout=1):
    """
    should be given a proxy list for test
    :param proxy_list: list object should be given[ip,ip,ip]
    :param timeout: default 1 second
    :return:
    """

    class _test_c(Thread):
        def __init__(self, p, **kwargs):
            Thread.__init__(self)
            self.p = p
            self.kwargs = kwargs
            self._res = None

        def __t(self):
            self._res = _test(self.p, kwargs=self.kwargs)

        def run(self):
            self.__t()

        @property
        def get_rst(self):
            return self._res

    if proxy_list:
        print 'Total proxy is %s, the testing is on going...' % len(proxy_list)
        thread_pool = []
        for item in proxy_list:
            thread_pool.append(_test_c(item, timeout=timeout))
        for item in thread_pool:
            item.start()
        for item in thread_pool:
            item.join()
        return filter(lambda x: 1 if x else 0, map(lambda x: x.get_rst, thread_pool))
    else:
        raise ValueError('Not found any proxies , please check!')


if __name__ == '__main__':
    t = requests.get('http://dly.134t.com/query.txt?key=NP1FA878EA&word=&count=1000')
    t = t.text
    tt = map(lambda x: x.replace('\r', ''), t.split('\n'))
    tt = list(set(tt))
    t = test_from_list(tt, 5)
    print t
    print len(t) / float(len(tt))
