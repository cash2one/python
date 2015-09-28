# coding:utf8
__author__ = 'Administrator'
"""
类说明：
仅包含页面分析（父类），使用过程中构造子类使用【可继承本类方法（或重载方法）】
（针对每类网址定制）
"""
from pyquery import PyQuery as pq


class PageParser:
    def __init__(self, pageSource):
        self.pageSource=pageSource
        if pageSource:
            self.d = pq(pageSource)
        else:
            self.d = None

    def targetArea(self,cssMark):
        """
        # 返回指标区域代码
        :param cssMark:
        :return:List
        """
        targetCode = None
        if self.d:
            d = self.d
            targetCode = d.find(cssMark)
        return targetCode

    def targetUrl(self, cssMark, urlAttr='href',urlHeader=None):
        """
        # 发现待跟进URL,用于后续抓取，参数说明：
        # cssMark:用于锁定发现链接的区域
        # urlAttr:链接对应的属性值，如“href”或“src”等，默认为“href”
        # urlHeader:在返回链接为相对地址的情况下适用，一般都是地址栏“？”前面的内容；默认为None
        :return:
        """
        targetCode=self.targetArea(cssMark=cssMark)
        urlList = None
        if targetCode:
            urlList = [pq(item).attr(urlAttr) for item in targetCode]
            if urlHeader:
                urlList=[urlHeader+temp for temp in urlList]
        return urlList

    def charset(self,cssMark='meta'):
        """
        返回网页编码(meta)
        :return:
        """
        targetCode=self.targetArea(cssMark)
        print(targetCode)
        return targetCode

    def getTitle(self,cssMark='title'):
        """
        返回网页title
        :return:
        """
        targetCode=self.targetArea(cssMark)
        return pq(targetCode).text()

    def pageLen(self):
        """
        返回网页长度
        :return:
        """
        return len(self.pageSource)

    def pageParser(self):
        """
        # 页面解释器；针对每个页面需定制（方法重载）
        :return:
        """
        pass