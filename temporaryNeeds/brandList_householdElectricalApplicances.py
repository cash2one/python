# coding:utf-8
__author__ = '613108'

import time, urllib2, sys, random, socket
from pyquery import PyQuery as pq
from bs4 import BeautifulSoup

sys.path.append(r'C:\Users\613108\Desktop\Project\tool_self')
import my_proxy, dirCheck, My_Csv
reload(sys)
sys.setdefaultencoding('utf-8')
socket.setdefaulttimeout(3)


def requestByProxy(url):
    i = 0
    src = ''
    proxy_port = my_proxy.is_proxy_exists()
    proxy = random.sample(proxy_port, 1)[0]
    proxy = proxy[0] + ':' + proxy[1]
    # print('=' * 5 + u'开始使用的代理：' + 'http://%s' % proxy)
    proxyHandler = urllib2.ProxyHandler({'http': r'http://%s' % proxy})
    cookies = urllib2.HTTPCookieProcessor
    opener = urllib2.build_opener(cookies, proxyHandler)
    opener.addheaders = [
        ('User-agent', 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0')]
    while i == 0:
        try:
            res_temp = opener.open(url)
            src = res_temp.read()
            res_temp.close()
            i += 1
        except:
            proxy = random.sample(proxy_port, 1)[0]
            # print(u'更换代理：%s:%s' % (proxy[0], proxy[1]))
            proxy = proxy[0] + ':' + proxy[1]
            proxyHandler = urllib2.ProxyHandler({'http': r'http://%s' % proxy})
            opener = urllib2.build_opener(cookies, proxyHandler)
            continue
    return src


# zol家电频道
def getBrandList_ZOL():
    src = requestByProxy('http://jd.zol.com.cn/manu_list.html')
    src = src.decode('gb2312', 'ignore')
    d = pq(src)
    brandList = d.find('.brandList_left a')
    brandList = [pq(item).text() for item in brandList if pq(item).text()][2:]
    for item in brandList:
        print(item)


def genBrandList_Yesky():
    src = requestByProxy('http://product.yesky.com/washingmachine/')
    d = pq(src)
    frames = d.find('.updonwlist a')
    produListEnglish = [pq(item).attr('href').split('/')[-2] for item in frames]
    produListChinese = frames.my_text()
    urlList = ['http://product.yesky.com/list/brand/' + item + '/' for item in produListEnglish]
    # productList=zip(produListChinese,produListEnglish)
    result = []
    for url in urlList:
        src = requestByProxy(url)
        d = pq(src)
        temp_1 = d.find('.rmpp>ul>li>a').my_text() if d.find('.rmpp>ul>li>a').my_text() else []
        temp_2 = d.find('.rmpp>dl>dd>a').my_text() if d.find('.rmpp>dl>dd>a').my_text() else []
        temp = temp_1 + temp_2
        nameEnglist = url.split('/')[-2]
        nameChinese = produListChinese[produListEnglish.index(nameEnglist)]
        res = []
        for item in temp:
            res.append([nameChinese, item])
        result += res

    # 数据写入csv文件
    title = ['category', 'brand']
    writer = My_Csv.Write_Csv(path=dirCheck.dirGen('d:/spider'), name='brandList_for_xiaoju', title=title,
                              result=result)
    writer.add_title_data()


if __name__ == '__main__':
    genBrandList_Yesky()
