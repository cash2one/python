# coding:utf-8
__author__ = '613108'

import urllib2
import re, random
import threading
import time
import gzip
import cStringIO
from selenium import webdriver
from Queue import Queue
import csv
import os
import MyCsv
import socket
socket.setdefaulttimeout(180)

ip_get = []
ip_ok = []
queue_for_check = Queue(0)
queue_for_get_proxy = Queue(0)

# IP正则
pat = re.compile(r'<td>\d+.\d+.\d+.\d+</td><td>.+?</td><td>.+?</td><td>.+?</td>')
pat_html = re.compile(r'\s+')
pat_ip = re.compile(r'\d+.\d+.\d+.\d+')
pat_port = re.compile(r'\d+')
pat_addr = re.compile(ur'[\u4e00-\u9fa5]{1,8}')

pat_2 = re.compile(r'\d+.\d+.\d+.\d+.*?<br />')
pat_ip_2 = re.compile(r'\d+.\d+.\d+.\d+')
pat_port_2 = re.compile(r':.*?@')
pat_addr_2 = re.compile(r'#.*?<')


class ProxyGet_1():
    def __init__(self, url):
        self.url = url

    def getProxy(self):
        req = urllib2.urlopen(url=self.url)
        result = req.read()
        # print(result.decode('UTF-8'))
        # print('*'*30)
        result = re.sub(pat_html, '', result)
        matchs = pat.findall(result.decode('UTF-8'))
        for row in matchs:
            ip = pat_ip.findall(row)[0]
            port = pat_port.findall(row)[-1]
            addr = pat_addr.findall(row)[0]
            type = pat_addr.findall(row)[-1]
            ip_all = [ip, port, addr, type]
            ip_get.append(ip_all)

    def run(self):
        self.getProxy()


class ProxyGet_2(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        # self.url=url

    def getProxy(self):
        # send_headers = [{'Referer':'www.youdaili.net',
        #                 'User-Agent':'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
        #                 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        #                 'Connection':'keep-alive'}]
        header_1 = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0')]
        proxy_port = get_last_proxy()
        proxy = random.sample(proxy_port, 1)[0]
        proxyHandler = urllib2.ProxyHandler({'http': r'http://%s:%s' % (proxy[0], proxy[1])})
        # r=urllib2.Request(self.url,headers=send_headers)
        # req=urllib2.urlopen(r)
        opener = urllib2.build_opener(proxyHandler)
        while queue_for_get_proxy.qsize() > 0:
            url = queue_for_get_proxy.get()
            try:
                opener.addheaders = header_1
                req = opener.open(url)
                result = req.read()
                req.close()
            except:
                queue_for_get_proxy.put(url)
                proxy_port = get_last_proxy()
                proxy = random.sample(proxy_port, 1)[0]
                proxyHandler = urllib2.ProxyHandler({'http': r'http://%s:%s' % (proxy[0], proxy[1])})
                print(u'请求失败，更换代理：%s:%s' % (proxy[0], proxy[1]))
                opener = urllib2.build_opener(proxyHandler)
                continue
            try:
                # gzip格式处理
                data = cStringIO.StringIO(result)
                gz = gzip.GzipFile(fileobj=data)
                result = gz.read()
                gz.close()
            except:
                pass
            # 文件头
            # print(req.info())
            matchs = pat_2.findall(result)
            for row in matchs:
                row = row.decode('UTF-8')
                try:
                    ip = pat_ip_2.findall(row)[0]
                    port = pat_port_2.findall(row)[0][1:][:-1]
                    addr = pat_addr_2.findall(row)[0][1:][:-1]
                    # print(addr)
                    if addr.find(u'匿') > 0:
                        pass
                    else:
                        continue
                    ip_all = [ip, port, addr]
                    ip_get.append(ip_all)
                except:
                    continue

    def run(self):
        self.getProxy()


class CheckProxy(threading.Thread):
    def __init__(self, proxy_list=''):
        threading.Thread.__init__(self)
        self.proxylist = proxy_list
        self.timeout = 5
        self.testurl = 'http://www.baidu.com'
        self.teststr = '030173'

    def checkproxy(self):
        cookies = urllib2.HTTPCookieProcessor
        # 列表分割法,弃用(若线程挂掉则损失部分代理)
        # for item in self.proxylist:
        # queue共享法
        while queue_for_check.qsize() > 0:
            item = queue_for_check.get()
            proxyHandler = urllib2.ProxyHandler({'http': r'http://%s:%s' % (item[0], item[1])})
            opener = urllib2.build_opener(cookies, proxyHandler)
            opener.addheaders = [
                ('User-agent', 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0')]
            t = time.time()
            try:
                req = opener.open(self.testurl, timeout=self.timeout)
                result = req.read()
                timeused = time.time() - t
                pos = result.find(self.teststr)

                if pos > 1:
                    item.append(timeused)
                    ip_ok.append(item)
                    # for i in item:
                    #     print(i)
                else:
                    continue
            except:
                continue

    def run(self):
        self.checkproxy()


class Get_StartUrl():
    def get_urllist_first(self):
        result = []
        driver = webdriver.PhantomJS()
        # driver=webdriver.Chrome()
        driver.maximize_window()
        driver.get('http://www.youdaili.net/')  # 默认获取代理网址
        # print(driver.page_source)
        frames = driver.find_elements_by_class_name('m_box2')
        frame_need = frames[3]
        frames_need = frame_need.find_elements_by_css_selector('li a')
        for item in frames_need:
            temp = item.get_attribute('href')
            result.append(temp)
        driver.quit()
        return result

    def get_urllist(self):
        result_first = self.get_urllist_first()
        driver = webdriver.PhantomJS()
        result = []
        for item in result_first:
            try:
                driver.get(item)
                frames = driver.find_elements_by_css_selector('.pagelist>li>a')
                frames = frames[3:-1]
                for item in frames:
                    temp = item.get_attribute('href')
                    result.append(temp)
            except:
                continue
        result = result + result_first
        driver.quit()
        return result


def is_proxy_exists():
    proxy_port = []
    file_name = str(time.strftime('%Y-%m-%d'))
    # file_name='2015-08-01'
    file_name = 'd:/spider/proxy/proxy_' + file_name + '.csv'
    if os.path.exists(file_name):
        with open(file_name) as proxy_csv:
            reader = csv.reader(proxy_csv)
            for line in reader:
                if line[0] == 'ip':
                    pass
                else:
                    proxy_port.append([line[0], line[1]])

    else:
        print('*' * 15 + u'暂无代理；正在抓取，请稍后' + '*' * 15)
        main()
        with open(file_name) as proxy_csv:
            reader = csv.reader(proxy_csv)
            for line in reader:
                if line[0] == 'ip':
                    pass
                else:
                    proxy_port.append([line[0], line[1]])
    return proxy_port


def proxyExistsAll(path=r'D:\spider\proxy'):
    is_proxy_exists()

    ip = []
    file_name = str(time.strftime('%Y-%m-%d'))
    # file_name='2015-08-01'
    file_name = 'd:/spider/proxy/proxyAll_' + file_name + '.csv'
    i = 0
    if os.path.exists(file_name):
        with open(file_name) as proxy_csv:
            reader = csv.reader(proxy_csv)
            for line in reader:
                if i == 0:
                    pass
                else:
                    ip.append(line)
                i += 1
    else:
        proxyList=[]
        for item in os.listdir(path):
            with open(path + '/' + item, 'r') as f:
                reader = csv.reader(f)
                i = 1
                for row in reader:
                    if i == 1:
                        pass
                    else:
                        proxyList.append((row[0],row[1]))
                    i += 1
        resultTemp = set(proxyList)
        for item in resultTemp:
            queue_for_check.put(list(item))

        # 开启300个线程检验：
        print(u'开始检验~~~')
        thread_count = 300
        CheckProxy_thread = []
        for i in range(thread_count):
            CheckProxy_thread.append(CheckProxy())
        for item in CheckProxy_thread:
            item.start()
        for item in CheckProxy_thread:
            item.join()

        ip = [item[:-1] for item in ip_ok]
        file_name = str(time.strftime('%Y-%m-%d'))
        with open('d:/spider/proxy/proxyAll_' + file_name + '.csv', 'wb') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['ip', 'port', 'time'])
            for item in ip_ok:
                try:
                    writer.writerow(item)
                except:
                    continue
    return ip


# 返回最新的代理列表,用于当时代理的抓取
def get_last_proxy(href_file_path='d:/spider/proxy'):
    proxy_port = []
    file_list = os.listdir(href_file_path)
    file_name_list = [href_file_path + '/' + item for item in file_list]
    temp_time = os.stat(file_name_list[0]).st_ctime
    temp_file_name = file_name_list[0]
    for item in file_name_list:
        # 判断是否为目录，如为目录则跳过
        if os.path.isdir(item): continue
        # 获取各文件创建时间
        file_create_time = os.stat(item).st_ctime
        if temp_time <= file_create_time:
            temp_time = file_create_time
            temp_file_name = item
    with open(temp_file_name) as proxy_csv:
        reader = csv.reader(proxy_csv)
        for line in reader:
            if line[0] == 'ip':
                pass
            else:
                proxy_port.append([line[0], line[1]])
    return proxy_port


def main():
    CheckThread = []
    ProxyGenThread = []
    # 获取代理列表网站
    print('*' * 15 + u'返回待抓取代理的网址' + '*' * 15)
    target_get = Get_StartUrl()
    target = target_get.get_urllist()

    print('*' * 15 + u'已取得待抓取代理的网址，开始抓取代理' + '*' * 15)

    for item in target:
        queue_for_get_proxy.put(item)

    # 开户10个进程抓取代理
    thread_count = 10
    ProxyGet_thread = []
    for i in range(thread_count):
        ProxyGet_thread.append(ProxyGet_2())
    for item in ProxyGet_thread:
        item.start()
    for item in ProxyGet_thread:
        item.join()

    # for url in target:
    #     proxy_2=ProxyGet_2(url)
    #     ProxyGenThread.append(proxy_2)
    #
    # for i in range(len(ProxyGenThread)):
    #     ProxyGenThread[i].start()
    #
    # for i in range(len(ProxyGenThread)):
    #     ProxyGenThread[i].join()

    print('*' * 15 + u'抓取完毕，开始检验代理' + '*' * 15)

    # 开启50个线程检验：
    # queue方法
    thread_count = 50

    for item in ip_get:
        queue_for_check.put(item)

    CheckProxy_thread = []
    for i in range(thread_count):
        CheckProxy_thread.append(CheckProxy())
    for item in CheckProxy_thread:
        item.start()
    for item in CheckProxy_thread:
        item.join()

    # 分割列表法
    # for i in range(50):
    #     temp=CheckProxy(ip_get[((len(ip_get)+49)/50)*i:((len(ip_get)+49)/50)*(i+1)])
    #     CheckThread.append(temp)
    #
    # for i in range(len(CheckThread)):
    #     CheckThread[i].start()
    #
    # for i in range(len(CheckThread)):
    #     CheckThread[i].join()

    file_name = str(time.strftime('%Y-%m-%d'))
    with open('d:/spider/proxy/proxy_' + file_name + '.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['ip', 'port', 'type'])
        for item in ip_ok:
            try:
                writer.writerow([item[0], item[1], item[3]])
            except:
                continue

    print('*' * 15 + u'代理抓取程序已运行完毕' + '*' * 15)


if __name__ == '__main__':
    # main()
    proxyExistsAll()
    print (u'跑完了~~~')