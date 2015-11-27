# coding:utf8
__author__ = '613108'
"""
每周数据更新至MySql数据库
"""


def genTitle():
    title = """
    name
    href
    judgepage_href
    seller
    addr
    brand
    monthsale
    productsum
    dsr_desc_mark
    dsr_desc_avg
    dsr_service_mark
    dsr_service_avg
    dsr_sending_mark
    dsr_sending_avg
    product_link_1
    price_1
    product_link_2
    price_2
    product_link_3
    price_3
    product_link_4
    price_4
    week
    spider_time
    """
    title = [item.replace(' ', '') for item in title.split('\n') if item][:-1]
    return title


def getData(path):
    from dataAnalysis import tmallAnalysis

    data, titleNeedToHandle = tmallAnalysis.getDistinctShopListDir(path=path)

    # titleOk = genTitle()
    #
    # titleIndex = []
    # for item in titleOk:
    #     try:
    #         titleIndex.append(titleNeedToHandle.index(item.replace(" ", "")))
    #     except:
    #         titleIndex.append('NOTFOUND')
    # print('=' * 35)
    # print(titleIndex)
    # print('=' * 35)
    # titleTemp = zip(titleOk, titleIndex)
    # for item in titleTemp:
    #     print(item)
    # print('=' * 35)
    # for i in range(len(titleNeedToHandle)):
    #     print(i,titleNeedToHandle[i])
    indexToHandleData = [0, 1, 14, 0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 16, 17, 19, 20, 22, 23, 25, 26]
    # 配置项：需提供的额外数值，周数及爬取日期
    week = 47
    """每次更新数据至数据库之前请输入数据爬取日期
    """
    spiderTime = '2015-11-23'
    dataOk = []
    for item in data:
        temp = []
        for itemIndex in indexToHandleData:
            temp.append(item[itemIndex])
        temp.extend([week, spiderTime])
        dataOk.append(temp)

    return dataOk


def putDataIntoDB(path):
    title = genTitle()
    data = getData(path=path)
    from myTool import dataToDatabase

    dataToDatabase.data2database(tableTitle=title, data=data, dbName='elec_platform')


if __name__ == '__main__':
    putDataIntoDB(path=r'D:\spider\tmall\baseInfo')
