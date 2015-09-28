#coding:utf-8
__author__ = '613108'

import urllib2
import re
import threading
import time

ip_get=[]
ip_ok=[]

# IP正则
pat=re.compile(r'<td>\d+.\d+.\d+.\d+</td><td>.+?</td><td>.+?</td><td>.+?</td>')
pat_html=re.compile(r'\s+')
pat_ip=re.compile(r'\d+.\d+.\d+.\d+')
pat_port=re.compile(r'\d+')
pat_addr=re.compile(ur'[\u4e00-\u9fa5]{1,8}')

class ProxyGet():
    def __init__(self,url):
        self.url=url

    def getProxy(self):
        req=urllib2.urlopen(url=self.url)
        result=req.read()
        # print(result.decode('UTF-8'))
        # print('*'*30)
        result=re.sub(pat_html,'',result)
        matchs=pat.findall(result.decode('UTF-8'))
        for row in matchs:
            ip=pat_ip.findall(row)[0]
            port=pat_port.findall(row)[-1]
            addr=pat_addr.findall(row)[0]
            type=pat_addr.findall(row)[-1]
            ip_all=[ip,port,addr,type]
            ip_get.append(ip_all)

    def run(self):
        self.getProxy()

class CheckProxy(threading.Thread):
    def __init__(self,proxy_list):
        threading.Thread.__init__(self)
        self.proxylist=proxy_list
        self.timeout=5
        self.testurl='http://www.baidu.com'
        self.teststr='030173'

    def checkproxy(self):
        cookies=urllib2.HTTPCookieProcessor
        for item in self.proxylist:
            proxyHandler=urllib2.ProxyHandler({'http':r'http://%s:%s'%(item[0],item[1])})
            opener=urllib2.build_opener(cookies,proxyHandler)
            opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0')]
            t=time.time()
            try:
                req=opener.open(self.testurl,timeout=self.timeout)
                result=req.read()
                timeused=time.time()-t
                pos=result.find(self.teststr)

                if pos>1:
                    item.append(timeused)
                    ip_ok.append(item)
                else:
                    continue
            except:
                continue

    def run(self):
        self.checkproxy()

if __name__=='__main__':
    CheckThread=[]

    proxy=ProxyGet('http://www.xici.net.co/')
    proxy.run()
    # 开启20个线程检验：
    for i in range(20):
        temp=CheckProxy(ip_get[((len(ip_get)+19)/20)*i:((len(ip_get)+19)/20)*(i+1)])
        CheckThread.append(temp)

    for i in range(len(CheckThread)):
        CheckThread[i].start()

    for i in range(len(CheckThread)):
        CheckThread[i].join()

    print(len(ip_ok))
    for item in ip_ok:
        for item in item:
            print(item)