# coding:utf8

__author__ = '613108'
import time
from ms_spider_fw.DBSerivce import DBService
from ms_spider_fw.downLoad import DownLoad_noFollow as DBN
from ms_spider_fw.parser.PageParser import PageParser


# 源码下载：
class Dler(DBN.DownLoadBase):
    def __init__(self):
        DBN.DownLoadBase.__init__(self)

    def startUrlList(self):
        db = DBService(dbName='jddata', tableName='thirdPartShopAppID')
        data = db.getData(var='appID')
        data = ['http://mall.jd.com/view_search-'+item[0]+'-0-5-1-24-1.html' for item in data if item[0]]
        return data


class PPer(PageParser):
    def __init__(self, pageSource):
        PageParser.__init__(self, pageSource=pageSource)

    def pageParser(self):
        d = self.d
        titleS = d.find('.user-jGoodsList>ul>li .jDesc>a').my_text()
        judgeCount = d.find('.user-jGoodsList>ul>li .jDesc>a').attr('href')
        productSum = d.find('.jPage>em').text()
        return titleS,judgeCount,productSum


def spiderMain():
    # 主程序
    dler = Dler()
    dler.downLoad(100)

    DB = DBService(dbName='jddata', tableName='thirdPartShopSearchPage')
    DB.createTable(tableTitle=['tttt'])

    while True:
        que = DBN.queueForDownLoad
        if not que.empty():
            url, src = que.get()
            pPer = PPer(src)
            temp = pPer.pageParser()
            print('='*30)
            print(url)
            for item in temp:
                print(item)
            # DB.data2DB(data=[url] + temp)
        else:
            time.sleep(1)


spiderMain()
