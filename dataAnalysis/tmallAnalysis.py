# coding:utf-8
__author__ = '613108'
import csv, sys, pymysql, os
from tool_self import MyCsv


def getDistinctShopTotal(path):
    d = {}
    title = []
    with open(path + '/' + 'Total.csv', 'r') as f:
        reader = csv.reader(f)
        i = 1
        for row in reader:
            if i == 1:
                title = row
            else:
                # d[row[1]] = row
                d[row[1] + row[3]] = row
            i += 1
    print(len(d))
    result = [item[1] for item in d.items()]
    writer = MyCsv.Write_Csv(path=path, name='shopDistinct', title=title, result=result)
    writer.add_title_data()
    return result, title


def getDistinctShopListDir(path):
    d = {}
    count = 1
    title = None
    fileList = os.listdir(path)
    fileListLen = len(fileList)
    for item in os.listdir(path):
        fileName = path + '\\' + item
        print(u'正在处理第 %s 个文件，总共 %s 个文件。' % (count, fileListLen))
        with open(fileName, 'r') as f:
            reader = csv.reader(f)
            i = 1
            for row in reader:
                if i == 1:
                    title = row
                else:
                    d[row[1]] = row
                    # d['+'.join(row[:-1])] = 1
                i += 1
        count += 1
    # print(len(d))
    result = [item[1] for item in d.items()]
    # writer = My_Csv.Write_Csv(path=path, name='shopDistinct', title=title, result=result)
    # writer.add_title_data()
    return result, title


def getShopInfoFromMysql():
    conn = pymysql.connect(host='10.118.187.12', user='admin', passwd='admin', charset='utf8', db='elec_platform')
    cursor = conn.cursor()
    sqlSelect = 'select distinct t.href from yms_tmall_shopinfo_new t'
    cursor.execute(sqlSelect)
    result = cursor.fetchall()
    result = [item[0][:-1] for item in result]
    conn.close()
    return result


def getDistinctShopDiff(path=r'C:\Users\613108\Desktop\tmall'):
    allShop, title = getDistinctShopTotal(path)
    originalShop = getShopInfoFromMysql()
    result = [item for item in allShop if item[1] not in originalShop]
    print(len(result))
    writer = MyCsv.Write_Csv(path=path, name='shopDistinct(okForSaler)', title=title, result=result)
    writer.add_title_data()
    return result, title


if __name__ == '__main__':
    getDistinctShopListDir(r'D:\spider\tmall\20150915')
    # getShopInfoFromMysql()
    # getDistinctShopDiff()
