# coding:utf8
__author__ = '613108'


def savePicture():
    from screenShot import saveScreenShot
    from spiderFrame.DBSerivce import DBService
    import time
    import random

    db = DBService(dbName='elec_platform', tableName='tmall_baseinfo_everyweek')
    data = db.getData(var='href', limit=100)
    data = map(lambda x: x[0], data)
    dri = None
    for url in data:
        print(url)
        dri = saveScreenShot(url, driver=dri)
        time.sleep(abs(random.gauss(3, 2)))


savePicture()
