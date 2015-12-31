__author__ = '613108'

from ms_spider_fw.DBSerivce import DBService

dbs = DBService(dbName='jddata', tableName='thirdPartShopInfo')
companyCount = dbs.getData(var='companyName', distinct=True)
shopCount1 = dbs.getData(var='shopHref', distinct=True)
shopCount2 = dbs.getData(var='shopName', distinct=True)
gradeHref = dbs.getData(var='gradeHref', distinct=True)
print len(companyCount)
print len(shopCount1)
print len(shopCount2)
print len(gradeHref)
