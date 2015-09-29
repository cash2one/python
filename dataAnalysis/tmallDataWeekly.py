#coding:utf8
__author__ = '613108'
from spiderFrame.DBSerivce import DBService
dbs=DBService(dbName='elec_platform',tableName='tmall_baseinfo_everyweek')
data=dbs.getData()
data=[item for item in data if int(item[-2])>=35]
print(len(data))