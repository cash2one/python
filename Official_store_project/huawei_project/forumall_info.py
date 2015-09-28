# coding:utf-8
__author__ = '613108'

from bs4 import BeautifulSoup
import urllib2
from selenium import webdriver
from threading import Thread
import time
import sys

reload(sys)
sys.setdefaultencoding("utf-8")
sys.path.append('C:/Users/613108/Desktop/Project/myTool')
import My_Csv

send_headers = {'Referer': 'www.baidu.com/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Connection': 'keep-alive'}

result = []


class Url_Gen():
    def __init__(self, url):
        self.url = url

    def get_pageTotal(self):
        driver = webdriver.PhantomJS()
        driver.get(self.url)
        page_total = driver.find_element_by_css_selector('.last').text
        page_total = int(page_total[4:])
        driver.quit()
        return page_total

    def get_urlList(self):
        url_begin_start = 'http://club.huawei.com/forumall-'
        url_begin_end = '.html'
        page_total = self.get_pageTotal()
        url_list = [url_begin_start + str(i + 1) + url_begin_end for i in range(page_total)]
        return url_list


class Data_Get(Thread):
    def __init__(self, url_list):
        Thread.__init__(self)
        self.url_list = url_list

    def get_data(self):
        ok = 1
        try:
            for url in self.url_list:
                print(url)
                req = urllib2.Request(url, headers=send_headers)
                req = urllib2.urlopen(req)
                soup = BeautifulSoup(req, from_encoding='UTF-8')
                frames = soup.find_all(attrs={'class': 'thdpp-cont'})
                # print(len(frames))
                for item in frames:
                    thd_topic = item.find(attrs={'class': 's xst'}).string
                    thd_view = item.find(attrs={'class': 'thd-ico thd-view'}).string
                    thd_href = 'http://club.huawei.com/' + item.find(attrs={'class': 's xst'})['href']
                    second_frame = item.find(attrs={'class': 'thd-sinfo'})
                    thd_replies = second_frame.find(attrs={'class': 'thd-ico thd-replies'}).string
                    thd_plate = second_frame.find_all('em')[0].a.string.replace('\r\n', '').replace('	', '')
                    thd_username = second_frame.find_all('em')[0].find_all('a')[1].contents[0].replace('\r\n',
                                                                                                       '').replace(
                        '	', '')
                    # thd_username=second_frame.find_all('em')[0].a.nextSibling.next_element.contents[0]
                    try:
                        thd_publictime = second_frame.find_all('em')[1].span.span['title']
                    except:
                        try:
                            thd_publictime = second_frame.find_all('em')[1].span.string
                        except:
                            thd_publictime = '-'
                    temp = [thd_topic, thd_href, thd_plate, thd_username, thd_publictime, thd_view, thd_replies]
                    result.append(temp)
                    # print(thd_topic)
                    # for temp in result:
                    #     print(temp)
        except:
            ok = 0
        return ok

    def run(self):
        # ok=self.get_data()
        # while not ok:
        #     time.sleep(5);ok=self.get_data()
        self.get_data()


if __name__ == '__main__':
    # url_list=['http://club.huawei.com/forumall-2.html']
    # Data_Get_thread=Data_Get(url_list)
    # Data_Get_thread.start()
    url_list = Url_Gen('http://club.huawei.com/forumall-1.html')
    url_list = url_list.get_urlList()
    Data_Get_thread = []
    # 开启20个线程
    thread_count = 50
    for i in range(thread_count):
        temp = Data_Get(url_list[((len(url_list) + thread_count - 1) / thread_count) * i:((len(
            url_list) + thread_count - 1) / 20) * (i + 1)])
        Data_Get_thread.append(temp)
    for i in range(len(Data_Get_thread)):
        Data_Get_thread[i].start()
    for i in range(len(Data_Get_thread)):
        Data_Get_thread[i].join()

    writer = My_Csv.Write_Csv('D:/spider/huawei', 'huawei_forum', result)
    writer.add_title(
        ['thd_topic', 'thd_href', 'thd_plate', 'thd_username', 'thd_publictime', 'thd_view', 'thd_replies'])
    writer.add_data()

    print(u'华为论坛信息已经收集完毕！')