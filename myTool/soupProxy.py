#coding:utf-8
__author__ = 'Administrator'

import urllib2,os,csv,time,sys,random,socket
reload(sys)
sys.setdefaultencoding('utf-8')
from bs4 import BeautifulSoup
socket.setdefaulttimeout(60)

def get_soup(url,proxy):
        proxy=proxy[0]+':'+proxy[1]
        opener=urllib2.build_opener(urllib2.ProxyHandler({'http':r'http://'+proxy}))
        urllib2.install_opener(opener)
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0')]
        response=opener.open(url)
        soup=BeautifulSoup(response.read(),from_encoding='utf-8')
        response.close()
        return soup

# class Get_soup_proxy(Thread):
#     def __init__(self,url,proxy_port):
#         Thread.__init__(self)
#         self.url=url
#         self.proxy_port=proxy_port
#
#     def get_soup(self):
#         proxy=self.proxy_port[0]+':'+self.proxy_port[1]
#         opener=urllib2.build_opener(urllib2.ProxyHandler({'http':r'http://'+proxy}))
#         urllib2.install_opener(opener)
#         opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0')]
#         response=opener.open(self.url)
#         soup=BeautifulSoup(response.read(),from_encoding='utf-8')
#         response.close()
#         return soup
#
#     def run_test(self):
#         self.get_soup()
#
# if __name__=='__main__':
#     proxy_port=is_proxy_exists()
#     queue_proxy=Queue(0)
#     for item in proxy_port:
#         queue_proxy.put(item)
#     print(queue_proxy.qsize())
#     Proxy_urllib2_thread=[]
#     for i in range(20):
#         temp=queue_proxy.get()
#         Proxy_urllib2_thread.append(Get_soup_proxy('http://www.tmall.com',temp))
#         queue_proxy.put(temp)
#     for item in Proxy_urllib2_thread:
#         item.start()
#     for item in Proxy_urllib2_thread:
#         item.join()
#     print(queue_proxy.qsize())