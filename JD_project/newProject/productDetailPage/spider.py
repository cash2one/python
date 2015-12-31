# coding:utf8
__author__ = '613108'
# noinspection PyPep8Naming
import time

from pyquery import PyQuery as pq
from ms_spider_fw.downLoad import DownLoad_noFollow as DBN
from ms_spider_fw.DBSerivce import DBService
from ms_spider_fw.parser.PageParser import PageParser


# 源码下载：
class Dler(DBN.DownLoadBase):
    def __init__(self):
        DBN.DownLoadBase.__init__(self)

    def startUrlList(self):
        """
        # 方法重载
        :return:
        """
        dbs = DBService(dbName='jddata', tableName='jdproductbaseinfo2database')
        data = dbs.getData(var='productHref,sku', distinct=True)
        dataThirdPartBase = [item[0] for item in data if len(item[1]) >= 10]
        dataHadCrawled = DBService(dbName='jddata', tableName='thirdPartShopInfo').getData(var='productHref')
        if not dataHadCrawled:
            return dataThirdPartBase
        dataHadCrawled = set([item[0] for item in dataHadCrawled])
        dataThirdPart = [item for item in dataThirdPartBase if item not in dataHadCrawled]
        dataThirdPart = [item for item in dataThirdPart if item[:4] == 'http']
        # print len(dataThirdPart)
        return dataThirdPart


class PPer(PageParser):
    def __init__(self, pageSource):
        PageParser.__init__(self, pageSource=pageSource)

    def pageParser(self):
        """
        # 方法重载
        :return:
        """
        d = self.d
        companyName = d.find('.text.J-shop-name').text()
        companyName = companyName if companyName else '-'
        shopName = d.find('.name').text()
        shopName = shopName if shopName else '-'
        shopHref = d.find('.name').attr('href')
        shopHref = shopHref if shopHref else '-'
        # 第三方卖家则获取评分信息
        scoreSum = '-'
        scoreProduct = '-'
        scoreProductAvg = '-'
        scoreService = '-'
        scoreServiceAvg = '-'
        scoreExpress = '-'
        scoreExpressAvg = '-'
        scoreFrame = d.find('.score-infor>div').my_text()
        gradeHref = d.find('.evaluate-grade>strong>a').attr('href')
        gradeHref = 'http:' + gradeHref if gradeHref else '-'
        if scoreFrame:
            try:
                upDownFrame = d.find('.score-infor>div span i')  # .attr('class')
                upDownFrame = [pq(item).attr('class') for item in upDownFrame]
                # 总分
                scoreSum = scoreFrame[0]
                scoreProduct = scoreFrame[3]
                scoreService = scoreFrame[6]
                scoreExpress = scoreFrame[9]
                scoreProductAvg = scoreFrame[4] if upDownFrame[0] == 'up' else '-' + scoreFrame[4]
                scoreServiceAvg = scoreFrame[7] if upDownFrame[1] == 'up' else '-' + scoreFrame[7]
                scoreExpressAvg = scoreFrame[10] if upDownFrame[2] == 'up' else '-' + scoreFrame[10]
            except:
                pass
        return [companyName, shopName, shopHref, scoreSum, scoreProduct, scoreProductAvg, scoreService,
                scoreServiceAvg, scoreExpress, scoreExpressAvg, gradeHref]


def spiderMain():
    """
    # main主程序
    :return:
    """
    dler = Dler()
    dler.downLoad(100)

    DB = DBService(dbName='jddata', tableName='thirdPartShopInfo')
    DB.createTable(
        tableTitle=['productHref', 'companyName', 'shopName', 'shopHref', 'scoreSum', 'scoreProduct', 'scoreProductAvg',
                    'scoreService',
                    'scoreServiceAvg', 'scoreExpress', 'scoreExpressAvg', 'gradeHref'])

    while True:
        que = DBN.queueForDownLoad
        if not que.empty():
            url, src = que.get()
            pPer = PPer(src)
            temp = pPer.pageParser()
            # test=temp[0]
            # if test=='-':
            #     continue
            # else:
            #     print(test)
            print(temp[0])
            DB.data2DB(data=[url] + temp)
        else:
            time.sleep(1)


if __name__ == '__main__':
    spiderMain()
