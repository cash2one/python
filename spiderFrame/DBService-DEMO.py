# coding:utf8
__author__ = '613108'
from spiderFrame import DBSerivce

DB = DBSerivce.DBService(dbName='tmall_info', tableName='yms_tmall_shopinfo_com',
                         host='localhost', user='root', passwd='', charset='utf8')
test = DB.getData(limit=100)

for item in test:
    print(item)