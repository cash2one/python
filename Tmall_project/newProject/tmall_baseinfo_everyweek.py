# coding:utf8
__author__ = '613108'

"""
# This script is used to unique tmall data(crawl weekly),and store date to mysql_db ;
# before using , you should modify crawled_date in cofing text .
"""

from dataAnalysis import tmallAnalysis
from ms_spider_fw.DBSerivce import DBService
import datetime

# config text:
spider_time = datetime.date(2016, 1, 11)  # crawled_date should be modified before use
spider_week = spider_time.strftime('%U')


def getData(path):
    data, titleNeedToHandle = tmallAnalysis.getDistinctShopListDir(path=path)
    indexToHandleData = [0, 1, 14, 0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 16, 17, 19, 20, 22, 23, 25, 26]
    week = spider_week
    dataOk = []
    for item in data:
        temp = []
        for itemIndex in indexToHandleData:
            temp.append(item[itemIndex])
        temp.extend([week, spider_time])
        dataOk.append(temp)

    return dataOk


def putDataIntoDB(path):
    data = getData(path=path)
    dbs = DBService(dbName='elec_platform', tableName='tmall_baseinfo_weekly_2016')
    dbs.data2DB(data=data)


if __name__ == '__main__':
    putDataIntoDB(path=r'D:\spider\tmall\%s' % spider_time.__str__())
