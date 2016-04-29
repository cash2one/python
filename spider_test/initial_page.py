# -*- encoding: utf-8 -*-

import urllib2
from pyquery.pyquery import PyQuery
from Queue import Queue
import sys

reload(sys)
sys.setdefaultencoding("utf8")

# 初始化
# 起始网页
initial_url = "http://www.163.com"
# 维护一个已经看过的url池
seen = set()
# 维护一个待抓取的队列，把初始网页地址压入队列
url_queue = Queue()
url_queue.put(initial_url)


# 下载器
def download_page(url=initial_url):
    headers_ = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
        "Rerefer": 'http:www.163.com'
    }
    request_ = urllib2.Request(url=url, headers=headers_)
    response_ = urllib2.urlopen(request_)
    return response_.read().decode('gb18030', 'ignore')


# 解释器
def page_parse(pq_object, css_selector):
    result_list = list()
    for item in pq_object.find(css_selector).items():
        result_list.append((item.text(), item.attr('href')))
    return result_list


# 持久化
def page_store(file, store_path=r'd:\163.txt'):
    if file:
        with open(store_path, 'a')as f:
            f.write('\n')
            f.write(file)
            f.write('\n')


def main():
    css_selector_temp = {
        'http://www.163.com': '.m-list.list-main.interval>li>a',
    }
    while url_queue.qsize():
        url = url_queue.get()
        try:
            page_html_temp = download_page(url=url)
            # 成功下载则维护进seen
            seen.add(url)
            print u'成功抓取 : %s' % url
        except:
            page_html_temp = None
            # 否则url入队
            url_queue.put(url)
        if page_html_temp:
            d = PyQuery(page_html_temp)
            # 解释页面，选择合造的selector
            if url == 'http://www.163.com':
                css_selector_inner = css_selector_temp.get(url)
            else:
                css_selector_inner = '#endText>p'
            parse_result = page_parse(pq_object=d, css_selector=css_selector_inner)
            # 提取待跟进url
            url_todo = set(
                    filter(lambda x: 1 if x else 0,
                           map(lambda x: x[1] if not x[1] == None else None, parse_result))
            )
            for url in url_todo:
                # 若已抓取则忽略，否则入队
                if not url in seen:
                    url_queue.put(url)

            # 持久化
            for item in parse_result:
                for text in item:
                    page_store(text)


if __name__ == '__main__':
    main()
