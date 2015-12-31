# coding:utf8
__author__ = '613108'
from pyquery import PyQuery as pq

def getKeyword():
    d = pq('https://www.taobao.com/markets/tbhome/market-list')
    wrap = d.find('.module-wrap')[6:]
    keyword = []
    for item in wrap:
        dw = pq(item)
        catogeryFi = dw.children('a').text()
        wrapSe = dw.find('.category-list-item')
        for ws in wrapSe:
            dws = pq(ws)
            catogerySe = dws.children('a').text()
            catogeryTi = dws.find('.category-items a').my_text()
            f = lambda x: [catogeryFi, catogerySe, x]
            t = map(f, catogeryTi)
            keyword += t
    return keyword

def push2DB():
    from ms_spider_fw.DBSerivce import DBService
    data=getKeyword()
    db=DBService('taobaodata','keyword')
    tableTitle=['categoryFi', 'categorySe', 'categoryTi']
    db.createTable(tableTitle=tableTitle)
    db.data2DB(data=data)

if __name__=="__main__":
    push2DB()