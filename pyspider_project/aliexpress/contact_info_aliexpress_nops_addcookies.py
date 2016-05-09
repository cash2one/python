#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on:2016/3/16 14:36
# Project:contact_info_aliexpress
# Author:yangmingsong

from ms_spider_fw.DBSerivce import DBService
import ms_proxy.proxy_collection as pc
import ms_proxy.proxy_test as pt
from pyquery.pyquery import PyQuery
from Queue import Queue, LifoQueue
import requests
import time
import re
import json
import threading
import random

# config_text
db_name = 'alibaba'
table_name = 'contact_info_aliexpress_com'
table_title = 'shop_url,contact_detail,crawl_time'
connect_dict = {
    'host': '',
    'user': '',
    'passwd': "",
    'charset': 'utf8'
}

# compile regular expression pattern
pattern_contact_info = re.compile('<th>(.+?)</th>.*?<td>(.+?)</td>', re.DOTALL)

proxies_queue = LifoQueue(0)


def proxy_collection():
    # get proxies from website
    proxies_list_website = pc.get_proxies_from_website()
    # at the same time , get other proxies from local database
    table_names_proxies = 'proxy_other_source,proxy_you_dai_li'
    proxies_list_local = list()
    for proxies_t_n in table_names_proxies.split(','):
        dbs = DBService(dbName='base', tableName=proxies_t_n, **connect_dict)
        proxies_list_local += map(lambda x: x[0], dbs.getData(var='proxy_port'))
    return list(set(proxies_list_website + proxies_list_local))


def proxies_test():
    proxies_list_total = proxy_collection()
    while True:
        for proxy in pt.test_from_list(proxies_list_total, 5):
            proxies_queue.put(proxy)


# database link object
db_server = DBService(dbName=db_name, tableName=table_name, **connect_dict)

_headers = {
    # 'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586",
    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'
}

_cookie_d = {
    1:"""ali_apache_tracktmp=W_signed=Y; acs_usuc_t=acs_rt=54ff5f6001ba467ebbfa62ae5074402f; xman_t=V+LPik1ZZPSqaSP1AWO1Vve/wFq8tpaQaGIgHdvkHHsKEZ1lYonxs0xx9gYj8ViOh4/U7M4EnKtrj62rdlywWZiADNBSK3NqDWyato/3uOj/jVVU7uZofbl6o6FucyIM5mOT2jsdKZh8Glt1AjWR8zJxrDzyJCSSr475iI033mtuc89hsJAwGtr/APCjl8m/r0kgeJZoYfkaBWzEyqo4yST8nuyIuCGeXeuXl0JRoD9ph4n167O2VsFRSgUHsLUVUk8e4i4pOrDrk0hdgAw+N/Cn8ivGje2iIhLKqTy8Grxj2ImnC2Z7vg1qQF/ufI4m9bY84kI0WlAjtlILVcMKO8dG+4EZXqqpFmyt35g+9L0TUo21RLd3b6I1NhsGj4+ygQfkTxTjNPYl9YAZSpiBa5Vcj2oNyQK4JAqesha9EmK3QO8GGQPy1SIdPqsVwCXD9PT30CMgeXC8L1sU7HEhx6502wKXaYkJGVmJFkG9549QABrR3mAlCaTOf9etQ+2gjlWxPq3y54wDjzOvUSm8kgBAnV7ri90cK7XRBNp366SDUKsM70UbYaMo3KVrKiEVhYerbBW/jmbUuHlRym3+EUFL9vX2aIhd3F0yPzBa4HmEQPdeFaRYYfq3ZFD8wlVq98n58wXJglQ=; intl_locale=en_US; __utmc=3375712; xman_us_t=x_lid=us1152696166czqw&sign=y&x_user=Wh44jZKeDVGTZyJFlgcwB6QOiDqM+A9F93W4O4rNswE=&ctoken=z6f_4anq9xcf&need_popup=y; aep_usuc_t=ber_l_fg=A0; ali_apache_id=68.235.57.102.1459057620375.565330.0; ali_apache_track=mt=1|ms=|mid=us1152696166czqw; xman_us_f=x_l=0&x_locale=en_US&no_popup_today=n&x_user=US|matthew|lee|ifm|772058806&last_popup_time=1459057866615; aep_usuc_f=region=US&site=glo&b_locale=en_US&isb=y&isfm=y&c_tp=USD&x_alimid=772058806&reg_ver=new; intl_common_forever=FwVXfMj9VbY2/xg7bluI6O3ncFwoAbWqN9oBNVM2iEn3cAz/KJmaTw==; xman_f=efOb6v80u6SYujFDdHUm5rtbz+2Iu8qIN8rWAW0CimXeSD7tcm0Sk+6/6V9IJrTOaZkO+bw2IsSnMpIXcIp+W72cn2eVCKe3/Wr+6OabzROwo9+qaFns+W3sqnPUh8d497uPnK7D/DdrD0a1ismpHBBoU4mbQU9Y/pkjZygxFTs92/TKwf6j8DXxt/d8ZIeAQlsAET7KAJE9uLxafjgqVJC8aWQU3Cc7us/12pqSsLVDui0lukBbCepKi8NMTMCBJtU1oJ9wQXNdOIqpoTj4xaeG6wxvj1cus/9iw1MjFU9Z5c+S1ra25W/dTSmow7hgNSIGeJbV4KROHHLIfrB12SwT/4aWOftmlkKSJcXohQor7U1UqbuT1gVfdjT+GrZMVMARFNTlamYi1FwEICjt2Q8rwKW47hfe; __utma=3375712.1960626007.1459057532.1459057532.1459057532.1; __utmb=3375712.10.10.1459057532; __utmz=3375712.1459057532.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; ali_beacon_id=68.235.57.102.1459057620375.565330.0; _ga=GA1.2.1960626007.1459057532; _gat=1; cna=6GF+D4WH4lsCAUTrOWbThqZe; isg=85231DBE5BED9A1A51211C6C145C8A33; l=Alpa8hwp0sjYyUZxwDbgKp3CKg58Md5y; aep_common_f=URxXRSeJiKru37WsCeigBc55QdFVvwNCXX89GyD+soYBWF/QsxUo9Q==; aep_history=keywords%5E%0Akeywords%09%0A%0Aproduct_selloffer%5E%0Aproduct_selloffer%0932441903549%0932359811121; JSESSIONID=022739661EACC6341EE5336B27EDFD72; u_info=LaksWQcsR0qq7DAxKc4IVsI1yk3CQUVZxmEFe+p9RuA=; d_ab_f=d682ed45da694007a709c9d8846cc04c""",
}


def gen_cookie():
    return dict(
            map(lambda x: (x.split('=', 1)[0].strip(), x.split('=', 1)[1]),
                _cookie_d.get(random.randint(1, len(_cookie_d))).split(';'))
    )


# for testing cookies
# _cookie_t = """ali_apache_id=101.105.37.177.1438705554786.260685.7; xman_us_f=x_l=1&x_locale=en_US&no_popup_today=n&x_user=US|yang|young|ifm|768474461&last_popup_time=1457712623354; aep_usuc_f=region=US&site=glo&b_locale=en_US&isb=y&isfm=y&c_tp=USD&x_alimid=768474461&reg_ver=new; intl_common_forever=rL5z+pTJEMOqSRr7MKiguZ9Lihf5oTyQRXJT8FtnVwNdRxp5uU1O5Q==; xman_f=6h/npGRCn8PCxoOVd+ue381gNqVAQGBg6f+jrlxyGbjxI6OUURdWZejPr1msspHIQEwM8SJpZNIUm14F+GhdzSfktjgh5/GMO5yA+qU1wD2owvJzr3HKslkoZaZcsKtcNz3AvPuo9SeiXrF7jgd1QXPY/UKDRO0nX4/1v6rGB6aWdfYMKt318vLhWIrmQrZQ4oheJxWqlJvixq92djQGQqnIfqMEtiGiYak3o51oWkCRF4N81S9LxC18FPxXHwjYyIAoUDWv7BVeykIDtRJtbS5sdMne0gc2pupQJx9sdHEJEr3GehcGxdpUJiYRC6lIX+3y8vior2X4xrdYH2agXOY9VFF5GExTbAdNQxhr6oBDhNkL/lM42Ee7JgqXK4tTRVpXQ+XekMIymgMmxR0oVyJ4BNOOlrLb; ali_beacon_id=220.152.150.99.1433075894474.773074.1; cna=PDviDaz2VHICAdyYlirqiemC; __utma=3375712.324010086.1438705507.1458384428.1458388505.11; l=AgAA/C6h38RBbszMOKKq5h4L8IDS7ORb; aep_history=keywords%5E%0Akeywords%09%0A%0Aproduct_selloffer%5E%0Aproduct_selloffer%0932328512449%0932320594174%0932379793562%0932312953658%0932602972005; _umdata=8D5462A7710B16F8D1DE8DF86205FD525C80C1F3E9ED159353D27A988B78E33A486FC569B0FB883C6705A9C6F940A638B43E266F5C7442047DCA4915D89FB7108E94AD13019CB44D; __utmz=3375712.1458388505.11.2.utmcsr=aliexpress.com|utmccn=(referral)|utmcmd=referral|utmcct=/category/200003482/dresses.html; _ga=GA1.2.324010086.1438705507; ali_apache_track=mt=1|ms=|mid=us1149212384ijsz; isg=580CC597EE0CF236F5283A13388FEF5B; d_ab_f=f12887f4ca9643129dfe6be772bb1c8d; aep_common_f=q4D4WHUu8LURVHlV+ZWTmdw4tcu1GZaUE+q0QzAaL+l3PdjHUgygiQ==; JSESSIONID=2848429EB23B3C6BB077C066C1B1923F; acs_usuc_t=acs_rt=243129bb6ae3438c9a9bfc4c59b82a31; xman_t=yPdVpMwygp/1uJRRe/aRCOVu7qxTo0j4NxOaYy1Px7+qxl/YeFLljop+D4dXpySUtoLvePze6njxvzuEHviXYvtqd7EcYDCOUJ+GOEwyBeb/R+fsYaSOILTOMizYulrgJkbq8zl6+RdWiTldpJAiqyIXsyk8bOy0OKfiyjCfT+5NqCvCGraThzyhQiTkQCaNGuHol2OAe5xLIZWKP08FwdjqX9RnxhBLMniaDJNjufN8RukWlkIXAfqxvLLM5Z37a1kIcQ4Uut26XfxPJhpzMod9sv8GNlvNdTibgvAqL5HQHh+MtWevinhVLJX2NtXdM/WVapXaLTjtQf71x7yMwWVFjPF9GE2NXenpinDrg7oRy3oBM7FwYpvqiy28LItoRKlXzL8Xmf/EwsTEpX7IS9Fi0+7Ts6yWhL3+MdA1grGNUsltGr9a5kS/yZiF4MmdUNlbsEp4uAcpjT5gcMyDxXnmDz/RDHHL1ayvGndWISTpF6SNqd6LO+gd76Hm3e+uo6WX3VvNCRWzC/hpZ92mZ2RHOpCuvZvYKKskYSCF3HwoZANaLFIk+g04LqADCTPjQUE+jm1UG/l3VbrhzQ8wkOzdBJ4/cJ29iTj1I67dcgGVs9F795wUOu8Qcux/bnOp; intl_locale=en_US; __utmc=3375712; _mle_tmp0=eNrz4A12DQ729PeL9%2FV3cfUx8KvOTLFSsjQ2dzRxczUyMHI2dXU1dLF0dDV1MXUysDA3M3BydXZS0kkusTI0MbUwtjCxMDMyMDTWSUxGE8itsDKojQIApWsX%2Fw%3D%3D; ali_apache_tracktmp=W_signed=Y; u_info=PzPojPc60gU9BgN7gGdVe/HeSj7zFohb8RmPP904RxI=; __utmb=3375712.7.10.1458388505; xman_us_t=x_lid=us1149212384ijsz&sign=y&x_user=tMwQ8hJci/ZHhxqofsUOYS/G9Uo5udG12uV1XaI35NY=&ctoken=ibova_l11_rq&need_popup=y&l_source=aliexpress; aep_usuc_t=ber_l_fg=A0; __utmt=1; _gat=1"""
# _cookie = dict(map(lambda x: (x.split('=', 1)[0].strip(), x.split('=', 1)[1]),_cookie_t.split(';')))


def crawled_urls():
    if not db_server.isTableExist():
        db_server.createTable(tableTitle=table_title.split(','))
        return []
    else:
        return map(
                lambda x: x.rsplit('/', 1)[0] + '/contactinfo/' + x.rsplit('/', 1)[1] + '.html',
                map(lambda x: x[0], db_server.getData(var='shop_url'))
        )


crawled_urls = crawled_urls()


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


all_urls = gen_url()


def download_page(url):
    _cookie = gen_cookie()
    _proxy = proxies_queue.get(timeout=36000)
    print "--PROXY => %s ; COOKIES => %s" % (_proxy, _cookie.get('ali_apache_id'))
    try:
        r = requests.get(url, cookies=_cookie, headers=_headers,
                         proxies={'http': 'http://%s' % _proxy}, timeout=5)
        response = r.content
        r.close()
        return response, _proxy
    except Exception:
        return None, _proxy


def page_parse(content, url):
    d = PyQuery(content)
    # print content[:200].encode('utf8')
    shop_name = d.find('.shop-name>a').text()
    shop_years = d.find('.shop-time>em').text()
    open_time = d.find('.store-time>em').text()
    contact_person = d.find('.contactName').text()
    contact_block = d.find('.box.block.clear-block').html()
    contact_detail = re.findall(pattern_contact_info, contact_block)
    crawl_time = time.strftime('%Y-%m-%d %X', time.localtime())
    return [
        url.replace('contactinfo/', '').replace('.html', ''),
        json.dumps(dict([
                            ('shop_name', shop_name),
                            ('contact_url', url),
                            ('shop_years', shop_years),
                            ('open_time', open_time),
                            ('contact_person', contact_person)
                        ] + contact_detail)
                   ),
        crawl_time
    ]


def __page_parse(url):
    content, proxy = download_page(url)
    return page_parse(content, url)


class Aliexpress_Company_Contact_Information_Spider(object):
    def __init__(self):
        self.queue_urls = Queue(0)
        self.crawled_url = crawled_urls
        self.gen_urls = all_urls
        self.url_start = list(set(self.gen_urls).difference(set(self.crawled_url)))

    def __url_putting(self):
        for url in self.url_start:
            self.queue_urls.put(url)

    def single_thread(self, lock):
        while self.queue_urls.qsize():
            url = self.queue_urls.get()
            content, proxy = download_page(url)
            try:
                page_data = page_parse(content, url)
                proxies_queue.put(proxy)
                print page_data
                db_server.data2DB(data=page_data)
            except Exception, e:
                print e.message
                self.queue_urls.put(url)

    def __gen_thread_and_run(self, thread_lock, thread_count=3):
        run_thread_pool = list()
        run_thread_pool.append(threading.Thread(target=proxies_test))
        while thread_count > 0:
            run_thread_pool.append(
                    threading.Thread(target=self.single_thread, args=(thread_lock,),
                                     name='SPIDER_' + str(thread_count)))
            thread_count -= 1
        for task in run_thread_pool:
            task.start()
        for task in run_thread_pool:
            task.join()

    def crawl(self, thread_count=3):
        self.__url_putting()
        thread_lock = threading.Lock()
        self.__gen_thread_and_run(thread_count=thread_count, thread_lock=thread_lock)


if __name__ == '__main__':
    spider = Aliexpress_Company_Contact_Information_Spider()
    spider.crawl(4)
