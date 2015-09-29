#coding:utf8
__author__ = '613108'
"""
提供代理抓取、检测、持久化及代理返回等等功能
"""
from spiderFrame.downLoad.DownLoader import DownLoader
from spiderFrame.downLoad import DownLoad_base_noFollow as DBN
from pyquery import PyQuery as pq

class DLer(DBN.DownLoadBase):
    def __init__(self):
        DBN.DownLoadBase.__init__(self)

    # override
    def startUrlList(self):
        DL=DownLoader('http://www.blackhatworld.com/blackhat-seo/f103-proxy-lists/')
        src=DL.highOrderUrllib2()
        d=pq(src)
        topicLink=d.find('.inner .threadtitle a')
        startUrl=[pq(item).attr('href') for item in topicLink[2:]]
        return startUrl

class ProxySupporter:
    def __init__(self):
        pass

    def gather(self):
        import time
        downloader=DLer()
        downloader.downLoad(100)
        i=0
        while i>10:
            print(i)
            if not DBN.queueForDownLoad.empty():
                src=DBN.queueForDownLoad.get(timeout=10)
                print(src)
            else:
                time.sleep(20)
                i+=1

    def test(self):
        """
        代理检测
        :return:
        """
        pass

    def persistence(self):
        """
        代理持久化
        :return:
        """
        pass

    def returnProxyList(self):
        """
        返回本地代理列表【如果本地无代理，则抓取】
        :return:
        """
        pass