# coding:utf8
# __author__ = '613108'

# This script is used to unique tmall data(crawl weekly),and store date to mysql_db ;
# before using , you should modify crawled_date in cofing text .

from ms_spider_fw.DBSerivce import DBService
import datetime
import os
import pandas
import numpy as np

# config text:
# crawled_date should be modified before use
spider_time = datetime.date(2016, 2, 29)
spider_week = spider_time.strftime('%U')


# noinspection PyUnresolvedReferences
def temp_data(path):
    fileListLen = len(os.listdir(path))
    names = globals()
    count = 1
    for item in os.listdir(path):
        fileName = path + '\\' + item
        print(u'正在处理第 %s 个文件，总共 %s 个文件。' % (count, fileListLen))
        names['data' + '_' + str(count)] = pandas.read_csv(fileName)
        count += 1
    name_space = []
    for i in range(1, fileListLen + 1):
        name_space.append(names['data' + '_' + str(i)])
    data_t = pandas.concat(name_space)
    data = data_t.drop_duplicates(['href'])
    data = data.values.tolist()
    return [map(lambda x: '' if x is np.nan else x, t) for t in data], data_t.columns.tolist()


def getData(path):
    data, titleNeedToHandle = temp_data(path)
    indexToHandleData = [0, 1, 14, 0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 16, 17, 19, 20, 22, 23, 25, 26]

    def temp_f(x):
        return map(lambda i: x[i], indexToHandleData)

    data_t = [temp_f(x) for x in data]
    return map(lambda x: x + [spider_week, spider_time.__str__()], data_t)


def putDataIntoDB(path):
    data = getData(path=path)
    dbs = DBService(dbName='elec_platform', tableName='tmall_baseinfo_weekly_2016')
    dbs.data2DB(data=data)


if __name__ == '__main__':
    putDataIntoDB(path=r'D:\spider\tmall\%s' % spider_time.__str__())
