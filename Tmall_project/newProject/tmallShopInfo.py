# coding:utf-8
# __author__ = '613108'

from threading import Thread
from Queue import Queue
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from myTool import dirCheck, myUrlOpen, MyCsv
import urllib
import sys
import socket
import json
import re
import time

reload(sys)
# noinspection PyUnresolvedReferences
sys.setdefaultencoding('utf-8')
socket.setdefaulttimeout(60)


def get_keyword():
    web_driver = webdriver.PhantomJS()
    web_driver.get('http://www.tmall.com')
    web_driver.maximize_window()
    click_element = web_driver.find_elements_by_css_selector('.j_MenuNav.nav-item')[:2]
    text = list()
    time.sleep(10)
    for item in click_element:
        ActionChains(web_driver).move_to_element(item).perform()
        time.sleep(2)
        fra = web_driver.find_elements_by_css_selector('.label-list a')
        for item_inner in fra:
            t = item_inner.text
            if t:
                text.append(t)
    web_driver.quit()
    if text:
        text = list(set(map(lambda x: x.replace(u'双11', ''), text)))
        with open('d:/spider/tmall/keyWord.txt', 'a') as f:
            f.write('++' + '++'.join(text))
        return text
    raise ValueError("Not found any keyword in tmall front page.")

def push_keyword_too_queue(using_local_file=1):
    def open_local_file():
        with open('d:/spider/tmall/keyword.txt', 'r')as f:
            temp = f.read()
        if temp:
            k_w = temp.split('++')
            k_w = map(lambda x: x.replace('双11', ""), k_w)
            return list(set(k_w))
        raise ValueError("Not found any keyword , please check !")

    if not using_local_file:
        get_keyword()

    keyword = open_local_file()

    for item in keyword:
        if item:
            queue_get_shop_list_keyword.put(item)


def main_get_keyword():
    global queue_get_shop_list_keyword
    queue_get_shop_list_keyword = Queue(0)
    push_keyword_too_queue(using_local_file=1)


# noinspection PyPep8
class GetShopList(Thread):
    def __init__(self):
        Thread.__init__(self)

    @staticmethod
    def get_shop_info_from_taobao_search_page():
        while not queue_get_shop_list_keyword.empty():
            key_word = queue_get_shop_list_keyword.get()
            # noinspection PyPep8
            get_data = {
                'initiative_id': 'staobaoz_20120515',
                'q': key_word,
                'app': 'shopsearch',
                'fs': 1,
                'isb': 1,
                'goodrate': '',
                's': 0
            }
            url_start = 'https://s.taobao.com/search?' + \
                        urllib.urlencode(get_data)
            src = myUrlOpen.requestByProxy(url_start)
            src = src.decode('gbk', 'ignore')
            # rebuild on 2016/01/18
            page_count_temp = re.findall(r'"totalPage":\d+,?', src)
            if page_count_temp:
                page_count = int(page_count_temp[0].split(':')[1][:-1])
            else:
                continue
            print key_word.decode('utf-8'),
            print page_count
            if page_count:
                for i in range(0, page_count * 20, 20):
                    get_data = {
                        'initiative_id': 'staobaoz_20120515',
                        'q': key_word,
                        'app': 'shopsearch',
                        'fs': 1,
                        'isb': 1,
                        'goodrate': '',
                        's': i
                    }
                    url = 'https://s.taobao.com/search?' + \
                          urllib.urlencode(get_data)
                    queue_get_shop_list_url.put(url)

        while queue_get_shop_list_url.qsize() > 0:
            url = queue_get_shop_list_url.get()
            src = myUrlOpen.requestByProxy(url)
            pat = re.compile(r'g_page_config = {.+};')
            try:
                temp = re.findall(pat, src)[0][16:-1]
            except IndexError:
                print url
                print src
                continue
            res = json.loads(temp)
            try:
                res = res['mods']['shoplist']['data']['shopItems']
            except Exception, e:
                print(e.message)
                continue
            for item in res:
                for_score_collection = [
                    'mas', 'mg', 'sas', 'sg', 'cas', 'cg', 'sgr', 'srn', 'encryptedUserId'
                ]
                item_inner_2 = json.loads(item.get('dsrInfo').get('dsrStr'))
                score = map(lambda x: item_inner_2[x], for_score_collection)
                data_uid = item.get('uid')
                shop_href = 'http:' + item.get('shopUrl')
                shop_name = item.get('title')
                addr = item.get('provcity')
                brand = item.get('mainAuction')
                sale_monthly = item.get('totalsold')
                sku_count = item.get('procnt')
                if item.get('auctionsInshop'):
                    product_top_sale = reduce(
                            lambda x, y: x + y, map(
                                    lambda z: [z['nid'], z['url'], z['price']], item['auctionsInshop']
                            )
                    )
                else:
                    product_top_sale = map(lambda x: '-', range(12))
                if len(product_top_sale) < 12:
                    product_top_sale.extend(
                            map(lambda x: '-', range(12 - len(product_top_sale)))
                    )
                data = [shop_name, shop_href, addr, brand, sale_monthly, sku_count] + \
                       score + product_top_sale + \
                       [data_uid]
                queue_get_shop_list_result.put(data)

    def run(self):
        self.get_shop_info_from_taobao_search_page()


def main_get_shop_list(thread_count=50):
    main_get_keyword()

    global queue_get_shop_list_url, queue_get_shop_list_result
    queue_get_shop_list_url = Queue(0)
    queue_get_shop_list_result = Queue(0)

    get_shop_list_thread_pool = list()
    for i in range(thread_count):
        get_shop_list_thread_pool.append(GetShopList())
    for son_thread in get_shop_list_thread_pool:
        son_thread.start()
    for son_thread in get_shop_list_thread_pool:
        son_thread.join()

    title = 'name,href,addr,brnad,monthsale,productsum,dsr_desc_mark,' \
            'dsr_desc_avg,dsr_service_mark,dsr_service_avg,dsr_sending_mark,' \
            'dsr_sending_avg,sgr,srn,encryptedUserId,productDataNid_1,' \
            'product_link_1,price_1,productDataNid_2,product_link_2,price_2,' \
            'productDataNid_3,product_link_3,price_3,' \
            'productDataNid_4,product_link_4,price_4,shopDataUid'.split(',')

    result = list()
    while not queue_get_shop_list_result.empty():
        result.append(queue_get_shop_list_result.get())
    csv_writer = MyCsv.Write_Csv(
            path=dirCheck.dirGen('d:/spider/tmall/baseInfo'),
            name='shopInfo',
            title=title,
            result=result
    )
    csv_writer.add_title_data()
    print(u'Okay!')


if __name__ == '__main__':
    print('Start')
    main_get_shop_list(100)
