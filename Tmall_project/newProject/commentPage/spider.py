# coding:utf8
__author__ = '613108'
from ms_spider_fw.DBSerivce import DBService


def commentHrefList():
    db = DBService('elec_platform', 'tmall_baseinfo_everyweek')
    judgePageHref = db.getData(var='name,href,judgepage_href')
    judgePageHref = [tuple(item) for item in judgePageHref if
                     not 'http' in item[2]]
    judgePageHref = [item for item in judgePageHref if not item[2].isnumeric()]
    judgePageHref = set(judgePageHref)
    judgePageHref = list(judgePageHref)
    print(len(judgePageHref))
    return judgePageHref


def craweldhref():
    db = DBService('elec_platform', 'yms_tmall_shopinfo_com_withoutjudge')
    href = db.getData(var='href')
    href = [item[0] for item in href]
    F = lambda x: x[:-1] if x[-1] == '/' else x
    href = map(F, href)
    print(len(href))
    return href


def href():
    temp1 = commentHrefList()
    temp2 = craweldhref()
    temp2 = set(temp2)
    temp3 = []
    for item in temp1:
        if not item[1] in temp2:
            temp3.append(list(item))
        else:
            continue
    temp3=[[item[0],item[1]+'/','http://rate.taobao.com/user-rate-'+item[2]+'.htm']for item in temp3]
    return temp3


temp = href()
db=DBService('elec_platform', 'yms_tmall_shopinfo_com_withoutjudge')
db.data2DB(data=temp,tableTitle=['name','href','judgepage_href'])