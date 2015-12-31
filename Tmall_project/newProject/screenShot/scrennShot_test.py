# coding:utf8
__author__ = '613108'


def savePicture():
    from screenShot import saveScreenShot
    from ms_spider_fw.DBSerivce import DBService
    import time
    import random

    db = DBService(dbName='tmalldata', tableName='tmall_baseinfo_realtime')
    data = db.getData(var='name,href', distinct=True)
    nameD = map(lambda x: x[0], data)
    data = map(lambda x: x[1], data)
    print(len(data))
    dri = None
    for url in data:
        name=nameD[data.index(url)]
        print(name)
        dri = saveScreenShot(url, driver=dri,title=name)
        time.sleep(abs(random.gauss(3, 2)))


savePicture()
