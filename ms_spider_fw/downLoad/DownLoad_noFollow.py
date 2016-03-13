# coding:utf8
__author__ = '613108'
from threading import Thread
from multiprocessing import Queue
# from ms_spider_fw.DBSerivce import DBService
from ms_spider_fw.UrlSupporter import UrlSupporter
from ms_spider_fw.downLoad.DownLoader import DownLoader
from myTool.listSplit import listSplit

# 本模块仅针对不需跟进的页面

queueForDownLoad = Queue(0)  # 模块变量，用于传递下载回来的源码


class DownLoadBase:
    def __init__(self):
        pass

    def startUrlList(self):
        """
        # 起始url，返回url列表
        # 针对不同项目需重载本方法
        :return:
        """
        pass
        """
        # FOR TEST:
        dbs = DBService(dbName='jddata', tableName='jdproductbaseinfo2database')
        data = dbs.getData(var='productHref,sku', limit=10000, distinct=True)
        startUrlList = [item[0] for item in data if len(item[1]) >= 10]
        return startUrlList
        """

    def urlListSplit(self, n):
        """
        # url列表分割，n为分割份数
        """
        data = self.startUrlList()
        F = lambda n, L: n if len(L) > n else len(L)
        n = F(n, data)
        if n == 0:
            raise
        urlList = listSplit(data, n)
        return urlList

    def genUrlSup(self, n):
        """
        # UrpSupport对象生产函数
        """
        urlList = self.urlListSplit(n)
        urlSupList = []
        for list in urlList:
            urlSup = UrlSupporter()
            urlSup.saveUrl(list)
            urlSupList.append(urlSup)
        return urlSupList

    class DownLoad(Thread):
        """
        # 下载线程类
        """

        def __init__(self, urlSoup):
            Thread.__init__(self)
            self.urlSoup = urlSoup

        def downLoade(self):
            while not self.urlSoup.isEmpty():
                url, src = DownLoader(self.urlSoup.next()[0]).getPageSource()
                queueForDownLoad.put((url, src))

        def run(self):
            self.downLoade()

    def downLoad(self, n):
        """
        # 源码下载主程序，n为下载线程数
        """
        import time
        urlSupList = self.genUrlSup(n)
        downLoadList = []
        for urlSup in urlSupList:
            downLoadList.append(self.DownLoad(urlSup))
        for item in downLoadList:
            time.sleep(0.1)
            item.setDaemon(True)  # 主线程结束则子线程停止执行
            item.start()
            # for item in downLoadList:
            #     item.join()
