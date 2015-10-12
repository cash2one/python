# coding:utf8

__author__ = '613108'
from spiderFrame.DBSerivce import DBService
from spiderFrame.CSVService import CSV
import sys

reload(sys)

sys.setdefaultencoding('utf8')


def begin():
    db = DBService(dbName='jddata', tableName='thirdPartShopInfo')
    data = db.getData()
    title = db.getTableTitle()[1:-2]
    S = set()
    for item in data:
        S.add(tuple(item[1:-2]))
    data = []
    for item in S:
        data.append(list(item))
    csv = CSV()
    csv.writeCsv(savePath='D:/spider', fileTitle=title, data=data, fileName='jdData')


def companyInfo():
    # 返回公司信息，字典形式
    db = DBService(dbName='jddata', tableName='thirdPartShopInfo')
    data = db.getData()
    data = [item for item in data if not item[2] == '-']
    comDict = {}
    for item in data:
        comDict[item[1]] = item[1:]
    return comDict


def productInfo():
    db = DBService(dbName='jddata', tableName='jdproductbaseinfo2database')
    data = db.getData(var='productHref,commentCount')
    proDict = {}
    for item in data:
        proDict[item[0]] = item[1]
    return proDict


def dataGen():
    comDict = companyInfo()
    proDict = productInfo()
    dict = {}
    for item in comDict.items():
        if item[0] in proDict.keys():
            dict[item[0]] = comDict[item[0]] + [proDict[item[0]]]
        else:
            continue
    data = [item[1] for item in dict.items()]
    db1 = DBService(dbName='jddata', tableName='thirdPartShopInfo')
    title = db1.getTableTitle()
    title = title+['commnetCount']
    print(title)
    db2 = DBService(dbName='jddata', tableName='thirdPartShopInfoAddCommentCount')
    db2.createTable(tableTitle=title)
    db2.data2DB(data=data)


dataGen()
