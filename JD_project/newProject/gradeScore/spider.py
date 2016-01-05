# coding:utf8
__author__ = '613108'
"""
评论页面，主要爬取详细评分，待更新
"""

import time
from ms_spider_fw.DBSerivce import DBService
from ms_spider_fw.downLoad import DownLoad_noFollow as DBN
from ms_spider_fw.parser.PageParser import PageParser


# 源码下载：
class Dler(DBN.DownLoadBase):
    def __init__(self):
        DBN.DownLoadBase.__init__(self)

    def startUrlList(self):
        db = DBService(dbName='jddata', tableName='jd_shop_gradeHref')
        data = db.getData()
        data = map(lambda x: x[0], data)
        return data


class PPer(PageParser):
    def __init__(self, pageSource):
        PageParser.__init__(self, pageSource=pageSource)

    def pageParser(self):
        from bs4 import BeautifulSoup

        src = self.pageSource
        soup = BeautifulSoup(src, from_encoding='UTF-8')
        # company_name = soup.find(attrs={'class': 'shopTolal'}).find_all('span')[2].contents[0]
        try:
            judge_total = soup.find(attrs={'class': 'jMallInfo'}).find_all('tr')[2].div['title']
        except:
            judge_total = '-'
        temp_1 = soup.find(attrs={'class': 'jMallInfo'}).find_all('tr')[3].find_all('span')[1]['class'][0]
        if temp_1 == 'jIconLow':
            judge_total_avg = '-' + \
                              soup.find(attrs={'class': 'jMallInfo'}).find_all('tr')[3].find_all('span')[1].em.contents[
                                  0]
        else:
            judge_total_avg = soup.find(attrs={'class': 'jMallInfo'}).find_all('tr')[3].find_all('span')[1].em.contents[
                0]
        temp_2 = soup.find_all(attrs={'class': 'jScore'})
        for i in range(len(temp_2)):
            name = globals()
            name['judge_title_' + str(i)] = temp_2[i].div.find(attrs={'class': 'jGrade'})['title']
            try:
                name['judge_title_' + str(i) + '_avg'] = '-' + temp_2[i].div.find(attrs={'class': 'jIconLow'}).em.string
            except AttributeError:
                try:
                    name['judge_title_' + str(i) + '_avg'] = temp_2[i].div.find(attrs={'class': 'jIconHigh'}).em.string
                except:
                    name['judge_title_' + str(i) + '_avg'] = '-'
            temp_3 = temp_2[i].find_all('li')
            for x in range(len(temp_3)):
                name = globals()
                name['judge_' + str(i) + '_' + str(x)] = temp_3[x].find(attrs={'class': 'jNum'})['title']
                try:
                    if temp_3[x].find(attrs={'class': 'jIconLow'}):
                        name['judge_' + str(i) + '_' + str(x) + '_avg'] = '-' + temp_3[x].find(
                            attrs={'class': 'jIconLow'}).em.string
                    else:
                        name['judge_' + str(i) + '_' + str(x) + '_avg'] = temp_3[x].find(
                            attrs={'class': 'jIconHigh'}).em.string
                # except:name['judge_'+str(i)+'_'+str(x)+'_avg']=temp_3[x].find_all('span')[-1].em.string
                except:
                    name['judge_' + str(i) + '_' + str(x) + '_avg'] = temp_3[x].find(
                        attrs={'class': 'jNum'}).em.string
        spider_time = time.strftime("%Y-%m-%d %X", time.localtime())
        result = [judge_total, judge_total_avg, judge_title_0, judge_title_0_avg, judge_0_0, judge_0_0_avg, judge_0_1,
                  judge_0_1_avg, judge_0_2, judge_0_2_avg, judge_title_1, judge_title_1_avg, judge_1_0, judge_1_0_avg,
                  judge_1_1, judge_1_1_avg, judge_1_2, judge_1_2_avg, judge_1_3, judge_1_3_avg, judge_title_2,
                  judge_title_2_avg, judge_2_0, judge_2_0_avg, judge_2_1, judge_2_1_avg, judge_2_2, judge_2_2_avg,
                  judge_2_3, judge_2_3_avg,spider_time]
        result=map(lambda x:x.replace(u'分',''),result)
        return result


def spiderMain():
    # 主程序
    from ms_spider_fw.CSVService import CSV

    dler = Dler()
    dler.downLoad(100)

    DB = DBService(dbName='jddata', tableName='shop_grade_score')
    DB.createTable(tableTitle=['gradeHref', 'totalScore', 'totalScore_avg', 'productScore', 'productScore_avg',
                               'productQualityScore', 'productQualityScore_avg', 'productDescribeScore',
                               'productDescribeScore_avg', 'returnExchangeRate', 'returnExchangeRate_avg',
                               'serviceScore', 'serviceScore_avg', 'sellerCSI', 'sellerCSI_avg', 'distributionCSI',
                               'distributionCSI_avg', 'onlineServiceCSI', 'onlineServiceCSI_avg', 'returnExchangeCSI',
                               'returnExchangeCSI_avg', 'temporalityScore', 'temporalityScore_avg', 'expScore',
                               'expScore_avg', 'sendPromptnessScore', 'sendPromptnessScore_avg', 'returnExchangeTime',
                               'returnExchangeTime_avg','onLineSeriveTime', 'onLineSeriveTime_avg','spider_time'])

    # while True:
    que = DBN.queueForDownLoad

    while True:
        url, src = que.get()
        try:
            pPer = PPer(src)
            result = pPer.pageParser()
            total=[url] + result
            DB.data2DB(data=total)
            print(result)
        except:
            continue

    # csvS = CSV()
    # csvS.writeCsv(savePath='d:/spider', data=total, fileName='tempJD',
    #               fileTitle=['gradeHref', 'totalScore', 'totalScore_avg', 'productScore', 'productScore_avg',
    #                          'productQualityScore', 'productQualityScore_avg', 'productDescribeScore',
    #                          'productDescribeScore_avg', 'returnExchangeRate', 'returnExchangeRate_avg',
    #                          'serviceScore', 'serviceScore_avg', 'sellerCSI', 'sellerCSI_avg', 'distributionCSI',
    #                          'distributionCSI_avg', 'onlineServiceCSI', 'onlineServiceCSI_avg', 'returnExchangeCSI',
    #                          'returnExchangeCSI_avg', 'temporalityScore', 'temporalityScore_avg', 'expScore',
    #                          'expScore_avg', 'sendPromptnessScore', 'sendPromptnessScore_avg', 'returnExchangeTime',
    #                          'returnExchangeTime_avg	onLineSeriveTime', 'onLineSeriveTime_avg'])


spiderMain()
