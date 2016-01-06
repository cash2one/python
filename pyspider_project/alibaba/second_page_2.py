# coding:utf8
__author__ = '613108'
# noinspection PyPep8Naming
import time

from pyquery import PyQuery as pq
from ms_spider_fw.downLoad import DownLoad_noFollow as DBN
from ms_spider_fw.DBSerivce import DBService
from ms_spider_fw.parser.PageParser import PageParser
import urllib

def gen_url_begin():
    def kw_template():
        kw = u'荷兰牛栏 德国爱他美 荷兰美素 惠氏 德国喜宝有机 德国喜宝益生菌 德国特福芬 澳洲可瑞康 新西兰A2  雅培  ' \
             u'英国惠氏 英国牛栏 英国爱他美  新西兰可瑞康 澳洲贝拉米 阿拉欧 Nannycare 日本明治 澳洲爱他美 Nutrilon ' \
             u'SIMILAC 多美滋 Guigoz 美赞臣 意大利爱他美 桂格 固力果 德国凯莉泓乐 plasmon 意大利美林 澳滋 德国牛栏 ' \
             u'美素佳儿 VIPLUS  安满 campina 卡瑞特滋   安佳 纽优乳  kinfield'
        return list(set([i.encode('GBK') for i in kw.split(' ') if i]))

    k_w = kw_template()
    url_base = "http://s.1688.com/selloffer/offer_search.htm?"
    url_par = [[('uniqfield', 'pic_tag_id'),
                ('keywords', t),
                ('earseDirect', 'false'),
                ('showStyle', 'img'),
                ('n', 'y')] for t in k_w
               ]
    # other method
    # url_par_2 = map(lambda par: '&'.join(map(lambda inner: '='.join(inner), par)), url_par)
    # urls = [url_base + item for item in url_par_2]
    return [url_base + urllib.urlencode(par) for par in url_par]

def gen_url(path=r'd:/spider/pagecount.csv'):
    def inner_gen_url(x):
        url = []
        for t in range(2, x[1] + 1):
            url_base = x[0]
            url_par = [
                ('beginPage', t),
                ('offset', 0)
            ]
            url.append(url_base + '#' + urllib.urlencode(url_par))
        return url

    with open(path) as f:
        t = f.readlines()
    t = map(lambda x: x.strip().split(','), t[1:])
    t = [item for item in t if item[1] and int(item[1]) >= 60]
    t = [(item[0], item[-1]) for item in map(lambda x: x + [int(x[1]) / 60 + 1], t)]
    t = map(lambda x: (x[0], 100) if x[1] > 100 else x, t)
    t = map(inner_gen_url, t)
    return reduce(lambda x, y: x + y, t)


# 源码下载：
class Dler(DBN.DownLoadBase):
    def __init__(self):
        DBN.DownLoadBase.__init__(self)

    def startUrlList(self):
        return gen_url()+gen_url_begin()


class PPer(PageParser):
    def __init__(self, pageSource):
        PageParser.__init__(self, pageSource=pageSource)

    def pageParser(self):
        """
        # 方法重载
        :return:
        """
        res = []
        d = self.d
        fw = d.find('#sm-offer-list>li')
        for f_w in fw:
            d = pq(f_w)
            sale = d.find('.sm-offerimg-tradeq').attr('title')
            company_name = d.find('.sm-offerimg-companyname').attr('title')
            href = d.find('.sm-offerimg-companyname').attr('href')
            member_id = d.find('.sm-offerimg-companyname').attr('memberid')
            offer_id = d.find('.sm-offerimg-companyname').attr('offerid')
            cxt_year = d.find('.sm-offerimg-cxt').text()
            credit_detail_href = d.find('.sm-offerimg-cxt').attr('href')
            goods_from = d.find('.sm-offer-flag').attr('title')
            location = d.find('.sm-offerimg-location').attr('title')
            product_title_sample=d.find('.sm-offerimg-title>a:nth-child(1)').attr('title')
            product_detail_sample=d.find('.sm-offerimg-des span').text()
            temp = [company_name,
                    sale,
                    href,
                    member_id,
                    offer_id,
                    cxt_year,
                    credit_detail_href,
                    goods_from,
                    product_title_sample,
                    product_detail_sample,
                    location]
            res.append(temp)
        return res


def spiderMain():
    """
    # main主程序
    :return:
    """
    dler = Dler()
    dler.downLoad(3)

    DB = DBService(host='localhost',
                   user='root',
                   passwd='',
                   charset='utf8',
                   dbName='spider',
                   tableName='alibaba_cow_powder_3')
    DB.createTable(tableTitle=
                   ['company_name',
                    'sale',
                    'href',
                    'member_id',
                    'offer_id',
                    'cxt_year',
                    'credit_detail_href',
                    'goods_from',
                    'product_title_sample',
                    'product_detail_sample',
                    'location',
                    'url_base'])

    while True:
        que = DBN.queueForDownLoad
        if not que.empty():
            url, src = que.get()
            pPer = PPer(src)
            temp = pPer.pageParser()
            if temp:
                temp = map(lambda x: x + [url], temp)
                DB.data2DB(data=temp)
                print(u'++成功:%s'%url)
            else:
                print(u'--失败:%s'%url)
        else:
            time.sleep(1)


if __name__ == '__main__':
    spiderMain()
