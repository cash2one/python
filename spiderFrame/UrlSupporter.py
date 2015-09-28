# coding:utf8
__author__ = 'Administrator'
"""
URL资源管理者
"""


class UrlSupporter:
    def __init__(self):
        # self.__init__()
        self.urlTotal=set()
        self.urlUsed=set()

    def saveUrl(self, urlTarget):
        """
        # url补充，所有的urlTarget全部收录并去重
        # urlTarget可为字符串或List形式
        :param url:
        :return:
        """
        if isinstance(urlTarget, list):
            for item in urlTarget:
                self.urlTotal.add(item)
        elif isinstance(urlTarget, str):
            self.urlTotal.add(urlTarget)
        else:
            print(u'-->UrlSupport->saveUrl 参数出错，应为str或list.')

    def next(self, n=1):
        """
        # url提取
        :param n:
        :return:
        """
        import random
        urlList = [item for item in self.urlTotal if item not in self.urlUsed]
        urlForReturn = random.sample(urlList, n)
        self.urlUsed.add(urlForReturn[0])
        return urlForReturn

    def isEmpty(self):
        """
        url pool是否已经为空，为空则返回True
        :return:
        """
        if len(self.urlTotal) == len(self.urlUsed):
            return True
        return False
