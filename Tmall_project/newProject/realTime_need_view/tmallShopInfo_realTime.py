# coding:utf-8
__author__ = '613108'
import time
import urllib
import sys
import socket
import json
import os
import csv
import random
from threading import Thread
from Queue import Queue

from pyquery import PyQuery as pq

from myTool import dirCheck, myUrlOpen, MyCsv

reload(sys)
sys.setdefaultencoding('utf-8')
socket.setdefaulttimeout(60)


class GetKeyWord():
    def __init__(self):
        pass

    def run(self):
        from ms_spider_fw.DBSerivce import DBService

        db = DBService(dbName='tmalldata', tableName='need_view')
        text = db.getData(var='shopName')
        text = map(lambda x: x[0], text)
        for item in text:
            if item:
                queue_GetShopList_keyWord.put(item)


def main_GetKeyWord():
    global queue_GetShopList_keyWord
    queue_GetShopList_keyWord = Queue(0)
    GetKeyWord().run()


def jsonParse(str):
    t = str
    t = t[1:-1]
    t = t.split(',')
    t = [item.split(':') for item in t]
    d = {}
    for item in t:
        d[item[0]] = item[1]
    return d


class GetShopList(Thread):
    def __init__(self):
        Thread.__init__(self)

    def getShopInfo(self):
        while not queue_GetShopList_keyWord.empty():
            keyWord = queue_GetShopList_keyWord.get()
            getData = {'initiative_id': 'staobaoz_20120515', 'q': keyWord, 'app': 'shopsearch', 'fs': 1, 'isb': 1,
                       'goodrate': '', 's': 0}
            urlStart = 'https://s.taobao.com/search?' + urllib.urlencode(getData)
            src = myUrlOpen.requestByProxy(urlStart)
            src = src.decode('gbk', 'ignore')
            d = pq(src)
            frames = d.find('.list-item')
            for item in frames:
                d = pq(item)
                score = d.find('.descr').attr('data-dsr')
                tempForScoreGet = ['mas', 'mg', 'sas', 'sg', 'cas', 'cg', 'sgr', 'srn', 'encryptedUserId']
                # mas，描述评分；mg，描述评分avg；sas，服务态度；sg，服务态度avg；cas,物流服务;cg物流服务avg
                jsonFile = json.loads(score)
                score = [jsonFile[sc] for sc in tempForScoreGet]
                dataUid = d.find('h4>a:nth-child(1)').attr('data-uid')
                shopHref = 'http:' + d.find('h4>a:nth-child(1)').attr('href')
                shopName = d.find('h4>a:nth-child(1)').text()
                addr = d.find('.shop-address').text()
                brand = d.find('.main-cat>a').text()
                monthSale = d.find('.info-sale').text()
                monthSale = monthSale.split(' ')[1]
                productSum = d.find('.info-sum').text()
                productSum = productSum.split(' ')[1]
                productPromotFrame = d.find('.one-product')
                tempForProductPromot = ['-' for i in range(12)]
                if productPromotFrame:
                    i = 0
                    for ppf in productPromotFrame:
                        di = pq(ppf)
                        dataNid = di.find('a').attr('data-nid')
                        productHref = 'http:' + di.find('a').attr('href')
                        productPrice = di.find('.price-num').text()
                        try:
                            tempForProductPromot[i] = dataNid
                            tempForProductPromot[i + 1] = productHref
                            tempForProductPromot[i + 2] = productPrice
                        except:
                            pass
                        i += 3
                spider_time = time.strftime("%Y-%m-%d %X", time.localtime())
                Result = [shopName, shopHref, addr, brand, monthSale, productSum] + score + tempForProductPromot + [
                    dataUid] + [spider_time]

                queue_GetShopList_result.put(Result)
                print(Result)

    def run(self):
        self.getShopInfo()


def main_GetShopList(threadCount=50):
    main_GetKeyWord()

    global queue_GetShopList_url, queue_GetShopList_result
    queue_GetShopList_url = Queue(0)
    queue_GetShopList_result = Queue(0)

    GetShopList_thread = []
    for i in range(threadCount):
        GetShopList_thread.append(GetShopList())
    for item in GetShopList_thread:
        item.start()
    for item in GetShopList_thread:
        item.join()

    result = []
    for i in range(queue_GetShopList_result.qsize()):
        result.append(queue_GetShopList_result.get(timeout=20))
    title = ['name', 'href', 'addr', 'brnad', 'monthsale', 'productsum', 'dsr_desc_mark', 'dsr_desc_avg',
             'dsr_service_mark',
             'dsr_service_avg', 'dsr_sending_mark', 'dsr_sending_avg', 'sgr', 'srn', 'encryptedUserId',
             'productDataNid_1', 'product_link_1', 'price_1', 'productDataNid_2', 'product_link_2', 'price_2',
             'productDataNid_3', 'product_link_3', 'price_3', 'productDataNid_4', 'product_link_4', 'price_4',
             'shopDataUid', 'spidertime']
    # 数据写入csv文件
    writer = MyCsv.Write_Csv(path=dirCheck.dirGen('d:/spider/tmall/double_11'), name='shopInfo',
                             title=title, result=result)
    writer.add_title_data()

    indexToHandleData = [0, 1, 14, 0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 16, 17, 19, 20, 22, 23, 25, 26, -1]
    dataOk = []
    for item in result:
        temp = []
        for itemIndex in indexToHandleData:
            temp.append(item[itemIndex])
        dataOk.append(temp)
    from ms_spider_fw.DBSerivce import DBService

    db = DBService(dbName='tmalldata', tableName='tmall_baseinfo_realtime')
    db.data2DB(data=dataOk)
    print(u'文件已输出并更新至数据库，请检查数据！')


if __name__ == '__main__':
    print('Start')
    main_GetShopList(200)
