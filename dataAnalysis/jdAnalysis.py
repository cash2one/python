# coding:utf-8
__author__ = '613108'
from threading import Thread
from pyquery import PyQuery as pq
import sys, csv, time
from tool_self import myUrlOpen, listSplit, dataToDatabase

reload(sys)
sys.setdefaultencoding('utf8')


def productBaseInfoFromLocalSrc():
    import csv

    result = []
    fileName = r'C:\Users\613108\Desktop\jd\Total_Distinct_2015-09-11 16_58_56.csv'
    with open(fileName, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            result.append(row)
    return result


def productBaseInfoFromLocalSrcDictionary(path=r'D:\spider\jd\productDetail'):
    import os, csv

    fileList = os.listdir(path)
    result = []
    for item in fileList:
        fileName = path + '/' + item
        with open(fileName, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                result.append(row)
    return result

def productBaseInfoFromDB():
    conn=dataToDatabase.connectDatabase(dbName='jddata')
    cursor=conn.cursor()
    selectForSql='select sku from jdproductbaseinfo2database'
    cursor.execute(selectForSql)
    data=cursor.fetchall()
    print(len(data))
    data=set(data)
    print(len(data))


def countOfProductBySku():
    # data = productBaseInfoFromLocalSrc()
    data = productBaseInfoFromLocalSrcDictionary()
    return len(data)


def skuIsThirdPart():
    # data = productBaseInfoFromLocalSrc()
    data = productBaseInfoFromLocalSrcDictionary()
    dataIsThirdPart = [item[1] for item in data]  # if len(item[1]) >= 10]
    dataIsThirdPart = list(set(dataIsThirdPart))
    print(len(dataIsThirdPart))
    return dataIsThirdPart


def pageLinkHadCrawled():
    data = productBaseInfoFromLocalSrc()
    dataLinks = [item[-1] for item in data]
    dataLinks = set(dataLinks)
    dataLinks = list(dataLinks)
    return dataLinks


def appleBrandProductSku():
    import urllib, csv

    data = productBaseInfoFromLocalSrcDictionary()
    dataApple = []

    jdCellphoneFlag = '9987,653,655'
    jdCellphoneFlagQuote = urllib.quote(jdCellphoneFlag)
    jdNotebookFlag = '670,671,672'
    jdNotebookFlagQuote = urllib.quote(jdNotebookFlag)
    jdPadFlag = '670,671,2694'
    jdPadFlagQuote = urllib.quote(jdPadFlag)

    for itemData in data:
        if ('IPHONE' in itemData[0].upper()
            or 'IPAD' in itemData[0].upper()
            or 'MACBOOK' in itemData[0].upper()) \
                and (jdCellphoneFlag in itemData[-1]
                     or jdCellphoneFlagQuote in itemData[-1]
                     or jdNotebookFlag in itemData[-1]
                     or jdNotebookFlagQuote in itemData[-1]
                     or jdPadFlag in itemData[-1]
                     or jdPadFlagQuote in itemData[-1]):
            dataApple.append(itemData)
    # with open('jdAppleData.csv','wb') as f:
    #     writer=csv.writer(f)
    #     writer.writerows(dataApple)
    return dataApple


class threadForJdProductShelves(Thread):
    def __init__(self, data):
        Thread.__init__(self)
        self.data = data

    def jdProductShelvesTime(self):
        for itemOut in self.data:
            href = itemOut[2]
            src = myUrlOpen.requestByProxy(href)
            d = pq(src)
            try:
                frames = d.find('#parameter2>li')
            except:
                break
            for item in frames:
                d = pq(item)
                text = d.text()
                text = text.split('：')
                textTest = text[0]
                textTarget = text[1]
                if textTest == u'上架时间':
                    shelvesTime = textTarget
                    print(shelvesTime)
                    self.data[self.data.index(itemOut)].append(shelvesTime)
                    break

        fileName = str(time.strftime('%Y-%m-%d %H_%M_%S')) + '-jdAppleData.csv'
        with open(fileName, 'wb') as f:
            writer = csv.writer(f)
            writer.writerows(self.data)

    def run(self):
        self.jdProductShelvesTime()


def threadForJdProductShelvesTime():
    threadCount = 10
    threadList = []
    data = appleBrandProductSku()
    dataList = listSplit.list_split(data, threadCount)
    for item in dataList:
        threadList.append(threadForJdProductShelves(item))
    for item in threadList:
        item.start()
    for item in threadList:
        item.join()


if __name__ == '__main__':
    # pageLinkHadCrawled()
    # skuIsThirdPart()
    # appleData=appleBrandProductSku()
    # threadForJdProductShelvesTime()
    # name = dataToDatabase.isTableExist()
    # print(name)

    productBaseInfoFromDB()
