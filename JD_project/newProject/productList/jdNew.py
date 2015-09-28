# coding:utf-8
__author__ = '613108'
import sys, threading
from Queue import Queue
from pyquery import PyQuery as pq
from myTool import myUrlOpen

reload(sys)
sys.setdefaultencoding('utf8')


def myInvoking(func):
    def new(*args):
        print(u'正在调用：' + func.func_name)
        return func(*args)

    return new


# 目录信息及词条对应地址（关键词，真实地址需构造）
@myInvoking
def getCategoryAndStartUrl():
    import json

    global queue_for_url_targetBase
    queue_for_url_targetBase = Queue(0)
    src = myUrlOpen.requestByProxy('http://dc.3.cn/category/get?callback=getCategoryCallback')
    srcTemp = src.split('(', 1)[1][:-1]
    srcTemp = srcTemp.decode('utf-8', 'ignore')
    srcJson = json.loads(srcTemp)['data']
    category = []
    for Fi in srcJson:
        targetFi = Fi['s']
        for Se in targetFi:
            targetSeTitle = Se['n']
            targetSe = Se['s']
            for Ti in targetSe:
                targetTiTitle = Ti['n']
                targetTi = Ti['s']
                for Fo in targetTi:
                    targetFoTitle = Fo['n']
                    categoryTemp = [targetSeTitle.split('|')[1], targetSeTitle.split('|')[0],
                                    targetTiTitle.split('|')[1], targetTiTitle.split('|')[0],
                                    targetFoTitle.split('|')[1], targetFoTitle.split('|')[0]]
                    category.append(categoryTemp)
                    queue_for_url_targetBase.put((targetFoTitle.split('|')[1], targetFoTitle.split('|')[0]))
    return category


# 页面解释类
class ProductPageParse():
    def __init__(self, src):
        self.src = src

    def returnPyqueryObject(self):
        return pq(self.src)

    @myInvoking
    def pageParseBase(self):
        d = self.returnPyqueryObject()
        result = []
        frames = d.find('.gl-i-wrap.j-sku-item')
        for item in frames:
            try:
                d = pq(item)
                productName = d.find('.p-name>a>em').text()
                commentCount = d.find('.p-commit>strong>a').text()
                sku = d.find('.J_focus').attr('data-sku')
                productHref = d.find('.p-img>a').attr('href')
                resultTemp = [productName, sku, productHref, commentCount]
                result.append(resultTemp)
            except:
                continue
        return result

    @myInvoking
    def retunPageLen(self):
        d = self.returnPyqueryObject()
        pageLen = d.find('.p-skip b').text()
        # print(pageLen)
        return pageLen


# 下载器类（多线程）
class MutiThreadForDownloadProductPage(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    @myInvoking
    def downloader(self):
        while not queue_for_url_target.empty():
            topic, url = queue_for_url_target.get()
            print(topic.decode('gbk', 'ignore'))
            print(url)
            src = myUrlOpen.requestByProxy(url)
            if src:
                queue_for_src.put((url, src))

    def run(self):
        self.downloader()


# 生成开始页地址
@myInvoking
def productStartPageUrlGen():
    global queue_for_url_targetFiUrl, queue_for_url_target, queue_for_src
    queue_for_url_targetFiUrl = Queue(0)
    queue_for_url_target = Queue(0)
    queue_for_src = Queue(0)

    # 调用获取目录函数
    getCategoryAndStartUrl()

    while not queue_for_url_targetBase.empty():
        topic, urlBase = queue_for_url_targetBase.get()
        if '-' in urlBase and '.' not in urlBase:
            url = 'http://list.jd.com/list.html?cat=' + ','.join(urlBase.split('-'))
            queue_for_url_targetFiUrl.put((topic, url))

    temp = queue_for_url_targetFiUrl.qsize()
    for i in range(temp):
        url = queue_for_url_targetFiUrl.get()
        queue_for_url_target.put(url)
        queue_for_url_targetFiUrl.put(url)


# 解释第一次返回的页面，提取页面结果
# 依据返回pageLen生成二次网址
@myInvoking
def mainProductInfoGetAndSeUrlGen():
    import urllib, time

    # 调用
    productStartPageUrlGen()

    global queueForResult
    queueForResult = Queue(0)

    # 调用下载器
    MutiThreadForDownloadProductPage_thread = []
    for i in range(10):
        MutiThreadForDownloadProductPage_thread.append(MutiThreadForDownloadProductPage())
    for item in MutiThreadForDownloadProductPage_thread:
        item.start()

    urlStart = []
    while not queue_for_url_targetFiUrl.empty():
        urlStart.append(queue_for_url_targetFiUrl.get()[1])

    while not queue_for_url_target.empty():
        if queue_for_src.empty():
            time.sleep(10)
            continue
        else:
            url, src = queue_for_src.get()
            if url in urlStart:
                try:
                    pageLen = int(ProductPageParse(src).retunPageLen())
                except:
                    print(ProductPageParse(src).retunPageLen())
                    continue
                if pageLen > 1:
                    temp = url.split('=')[1]
                    for i in range(1, pageLen):
                        urlData = {'cat': temp, 'page': i + 1, 'JL': '6_0_0'}
                        SeUrl = 'http://list.jd.com/list.html?' + urllib.urlencode(urlData)
                        # 判断是否已抓取，已抓取则不推入queue
                        if SeUrl not in pageLinkHadCrawled:
                            queue_for_url_target.put(("topic", SeUrl))
            result = ProductPageParse(src).pageParseBase()
            for item in result:
                temp = item + [url]
                queueForResult.put(temp)

            if queueForResult.qsize() > 5000:
                dataSaved()


# 结果持久化
@myInvoking
def dataSaved():
    from myTool import MyCsv,dirCheck

    result = []
    for i in range(5000):
        temp = queueForResult.get()
        result.append(temp)
    title = ['', '', '', '', 'url']
    # 数据写入csv文件
    writer = MyCsv.Write_Csv(path=dirCheck.dirGen('d:/spider/jd/productDetail'), name='jdProductInfo',
                              title=title, result=result)
    writer.add_title_data()


# 返回已抓取的地址
@myInvoking
def filterSpiderUrl():
    from dataAnalysis import jdAnalysis

    global pageLinkHadCrawled
    pageLinkHadCrawled = jdAnalysis.pageLinkHadCrawled()
    return pageLinkHadCrawled


if __name__ == '__main__':
    # getCategoryAndStartUrl()
    filterSpiderUrl()
    mainProductInfoGetAndSeUrlGen()
