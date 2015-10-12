# coding:utf8

__author__ = '613108'
import time
from spiderFrame.DBSerivce import DBService
from spiderFrame.downLoad import DownLoad_noFollow as DBN
from spiderFrame.parser.PageParser import PageParser


# 源码下载：
class Dler(DBN.DownLoadBase):
    def __init__(self):
        DBN.DownLoadBase.__init__(self)

    def startUrlList(self):
        db = DBService(dbName='jddata', tableName='thirdPartShopInfo')
        data = db.getData(var='shopHref', distinct=True)
        data = [item[0] for item in data]
        return data


class PPer(PageParser):
    def __init__(self, pageSource):
        PageParser.__init__(self, pageSource=pageSource)

    def pageParser(self):
        if self.pageSource:
            d = self.d
            appID=d.find('#pageInstance_appId').attr('value')
            return [appID]


def spiderMain():
    # 主程序
    dler = Dler()
    dler.downLoad(100)

    DB = DBService(dbName='jddata', tableName='thirdPartShopAppID')
    DB.createTable(tableTitle=['shopHref','appID'])

    while True:
        que = DBN.queueForDownLoad
        if not que.empty():
            url, src = que.get()
            pPer = PPer(src)
            temp = pPer.pageParser()
            print('='*30)
            print(url)
            print(temp)
            if temp:
                DB.data2DB(data=[url] + temp)
        else:
            time.sleep(1)


spiderMain()
