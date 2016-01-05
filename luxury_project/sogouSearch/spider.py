# coding:utf8
__author__ = '613108'
import sys
import time
import urllib

from ms_spider_fw.downLoad.DownLoad_noFollow import DownLoader
# from ms_spider_fw.parser.PageParser import PageParser
from pyquery import PyQuery as pq
from luxury_project.luxuryBrand.brandList import brandList

reload(sys)
# noinspection PyUnresolvedReferences
sys.setdefaultencoding('utf8')


# noinspection PyShadowingNames
def urlData(keyWord=None):
    """
    sogou搜索页面地址拼接
    :param keyWord:
    :return:
    """
    if not keyWord:
        return None
    else:
        t = time.time()
        t1 = int(t)
        t2 = int(t * 1000)
        urlDataTemp = {'_asf': 'null',
                       '_ast': t1,
                       'cid': '',
                       'dp': 1,
                       'ie': 'utf8',
                       'lkt': '',
                       'p': 40040100,
                       'query': keyWord,
                       'sst0': t2,
                       'sut': 5581,
                       'w': '01029901'}
        return 'https://www.sogou.com/web?' + urllib.urlencode(urlDataTemp)


def parser(src):
    d = pq(src)
    target = d.find('.rb')
    res = []
    for item in target:
        dt = pq(item)
        F = lambda x: x if x else '-'
        title = F(dt.find('.pt').text())
        content = F(dt.find('.ft').text())
        href = F(dt.find('.fb').my_text()[0])
        res.append([title, content, href])
    for item in res:
        print('=' * 30)
        for t in item:
            # noinspection PyBroadException
            try:
                print(t)
            except:
                print(t.decode('gbk', 'ignore'))


for keyWord in brandList():
    parser(DownLoader(urlData(keyWord=keyWord + ' 商城')).highOrderUrllib2())
