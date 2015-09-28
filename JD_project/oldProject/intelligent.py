# coding:utf-8
__author__ = 'Administrator'

import urllib, urllib2, sys, random, socket, os, csv, json, time
from selenium import webdriver
from threading import Thread
from Queue import Queue
from pyquery import PyQuery as pq
from tool_self import MyCsv, myProxy, dirCheck, myUrlOpen

reload(sys)
sys.setdefaultencoding('utf-8')

socket.setdefaulttimeout(5)


# 起始网址类
class StartUrls():
    def __init__(self, url='http://channel.jd.com/652-12345.html', css='.item>ul>li>a'):
        self.url = url
        self.css = css

    def startUrls(self):
        driver = webdriver.PhantomJS()
        driver.get(self.url)
        frame = driver.find_elements_by_css_selector(self.css)
        result = []
        for item in frame:
            href = item.get_attribute('href')
            topic = item.text
            result.append([topic, href])
            try:
                queue_for_genurl_0.put((topic, href))
            except:
                pass
        driver.quit()
        return result


def main_startUrls():
    global queue_for_genurl_0
    queue_for_genurl_0 = Queue(0)
    test = StartUrls()
    result = test.startUrls()
    return result


# 网址生成器
class GenUrlList(Thread):
    def __init__(self, pageCountCss='.fp-text>i'):
        Thread.__init__(self)
        self.pageCountCss = pageCountCss

    def genUrls(self):
        driver = webdriver.PhantomJS()
        driver.maximize_window()
        while queue_for_genurl_0.qsize() > 0:
            topic, url = queue_for_genurl_0.get()
            keyWord = ','.join(url.split('/')[-1].split('.')[0].split('-'))
            pageCount = 0
            try:
                driver.get(url)
                pageCount = int(driver.find_element_by_css_selector(self.pageCountCss).text)
            except:
                queue_for_genurl_0.put(url)
                continue
            if pageCount:
                for i in range(pageCount):
                    keyWordEncodeData = {'cat': keyWord, 'page': (i + 1), 'JL': '6_0_0'}
                    temp = 'http://list.jd.com/list.html?' + urllib.urlencode(keyWordEncodeData)
                    queue_for_url_target.put((topic, temp))
            # 顺带将源码保存下来，以便提取品牌列表之用
            with open(topic + '.txt', 'wb') as f:
                f.write(driver.page_source)
        driver.quit()

    def run(self):
        self.genUrls()


def main_genUrlList():
    main_startUrls()
    # 生成待抓取代理
    global queue_for_url_target
    queue_for_url_target = Queue(0)

    GenUrlList_thread = []
    for i in range(3):
        GenUrlList_thread.append(GenUrlList())
    for item in GenUrlList_thread:
        item.start()
    for item in GenUrlList_thread:
        item.join()


# 提取品牌列表
class BrandList():
    def __init__(self, filePath):
        self.filePath = filePath

    def getBrandList(self):
        fileList = os.listdir(self.filePath)
        result = []
        for item in fileList:
            with open(self.filePath + '/' + item, 'r') as f:
                res = f.read()
            d = pq(res)
            res = d.find('.J_valueList.v-fixed>li>a').my_text()
            res = [[item.split('.')[0].decode('gbk', 'ignore'), temp] for temp in res]
            result.append(res)
        result = [temp for item in result for temp in item]
        title = ['topic', 'brnad']
        # 数据写入csv文件
        writer = MyCsv.Write_Csv(path=dirCheck.dirGen('d:/spider/jd/brandList'), name='jd_intelligent_brand',
                                 title=title,
                                 result=result)
        writer.add_title_data()


def main_brandList():
    # 获取品牌列表
    BrandList(dirCheck.dirGen('D:\spider\jd\brand_pagesource')).getBrandList()
    # 测试返回的商品介绍字段，用于挑选适用字段


def productKeyWordTest():
    global queue_for_test
    queue_for_test = Queue(0)

    result = []
    for i in range(queue_for_test.qsize()):
        result.append(queue_for_test.get())
    title = ['url', 'textTest']
    # 数据写入csv文件
    writer = MyCsv.Write_Csv(path=dirCheck.dirGen('d:/spider/jd'), name='TextTest', title=title, result=result)
    writer.add_title_data()


# 细节信息类
class ProductDetail(Thread):
    def __init__(self):
        Thread.__init__(self)

    def getProductDetail(self):
        proxy_port = myProxy.is_proxy_exists()
        proxy = random.sample(proxy_port, 1)[0]
        proxy = proxy[0] + ':' + proxy[1]
        print('=' * 5 + u'开始使用的代理：' + 'http://%s' % proxy)
        proxyHandler = urllib2.ProxyHandler({'http': r'http://%s' % proxy})
        cookies = urllib2.HTTPCookieProcessor
        opener = urllib2.build_opener(cookies, proxyHandler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0')]

        while queue_for_url_target.qsize() > 0:
            print('=' * 15 + u'还剩下%s个待抓网址！' % queue_for_url_target.qsize())
            temp = ''
            try:
                temp = queue_for_url_target.get()
                topic, url = temp
            except:
                print(temp)
                continue
            try:
                res_temp = opener.open(url)
                src = res_temp.read()
            except:
                queue_for_url_target.put(url)
                proxy = random.sample(proxy_port, 1)[0]
                print(u'更换代理：%s:%s' % (proxy[0], proxy[1]))
                proxy = proxy[0] + ':' + proxy[1]
                proxyHandler = urllib2.ProxyHandler({'http': r'http://%s' % proxy})
                opener = urllib2.build_opener(cookies, proxyHandler)
                continue

            res_temp.close()
            d = pq(src)
            frames = d.find('.gl-i-wrap.j-sku-item')
            for item in frames:
                d = pq(item)
                productName = d.find('.p-name>a>em').text()
                # productFunction = d.find('.p-name>a>em').text()
                price = d.find('.J_price>i').text()
                commentCount = d.find('.p-commit>strong>a').text()
                sku = d.find('.gl-item').attr('data-sku')
                productHref = d.find('.p-img>a').attr('href')
                # print [productName,sku,productHref,price,commentCount,topic,url]
                queue_for_result.put([productName, sku, productHref, price, commentCount, topic, url])
                print([productName, sku, productHref, price, commentCount, topic, url])

    def run(self):
        self.getProductDetail()


def main_productDetail(threadCount=50):
    main_genUrlList()
    # 商品链接等详情抓取main
    global queue_for_result
    queue_for_result = Queue(0)

    ProductDetail_thread = []
    for i in range(threadCount):
        ProductDetail_thread.append(ProductDetail())
    for item in ProductDetail_thread:
        item.start()
    for item in ProductDetail_thread:
        item.join()

    result = []
    for i in range(queue_for_result.qsize()):
        result.append(queue_for_result.get())
    title = ['productName', 'sku', 'productHref', 'price', 'commentCount', 'topic', 'pageUrl']
    # 数据写入csv文件
    writer = MyCsv.Write_Csv(path=dirCheck.dirGen('d:/spider/jd/productDetail'),
                             name='jd_intelligent_productInfoDetail', title=title,
                             result=result)
    writer.add_title_data()


# 商品页面信息抓取类，主要为抓取评价数据及商品信息数据
class InnerPageProductDetail(Thread):
    def __init__(self):
        Thread.__init__(self)

    def getDetail(self):
        proxy_port = myProxy.is_proxy_exists()
        proxy = random.sample(proxy_port, 1)[0]
        proxy = proxy[0] + ':' + proxy[1]
        print('=' * 5 + u'开始使用的代理：' + 'http://%s' % proxy)
        proxyHandler = urllib2.ProxyHandler({'http': r'http://%s' % proxy})
        cookies = urllib2.HTTPCookieProcessor
        opener = urllib2.build_opener(cookies, proxyHandler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0')]

        while queue_for_InnerPageProdctDetail.qsize() > 0:
            print('=' * 15 + u'还剩下%s个待抓网址！' % queue_for_InnerPageProdctDetail.qsize())
            url = queue_for_InnerPageProdctDetail.get()
            try:
                res_temp = opener.open(url)
                src = res_temp.read()
                res_temp.close()
                d = pq(src)
            except:
                queue_for_url_target.put(url)
                proxy = random.sample(proxy_port, 1)[0]
                print(u'更换代理：%s:%s' % (proxy[0], proxy[1]))
                proxy = proxy[0] + ':' + proxy[1]
                proxyHandler = urllib2.ProxyHandler({'http': r'http://%s' % proxy})
                opener = urllib2.build_opener(cookies, proxyHandler)
                continue
            # 第三方卖家则获取公司名称
            companyName = d.find('.text.J-shop-name').text()
            companyName = companyName if companyName else '-'
            # 第三方卖家则获取评分信息
            scoreSum = '-'
            scoreProduct = '-'
            scoreProductAvg = '-'
            scoreService = '-'
            scoreServiceAvg = '-'
            scoreExpress = '-'
            scoreExpressAvg = '-'
            scoreFrame = d.find('.score-infor>div').my_text()
            if scoreFrame:
                upDownFrame = d.find('.score-infor>div span i')  # .attr('class')
                upDownFrame = [pq(item).attr('class') for item in upDownFrame]
                # 总分
                scoreSum = scoreFrame[0]
                scoreProduct = scoreFrame[3]
                scoreService = scoreFrame[6]
                scoreExpress = scoreFrame[9]
                scoreProductAvg = scoreFrame[4] if upDownFrame[0] == 'up' else '-' + scoreFrame[4]
                scoreServiceAvg = scoreFrame[7] if upDownFrame[1] == 'up' else '-' + scoreFrame[7]
                scoreExpressAvg = scoreFrame[10] if upDownFrame[2] == 'up' else '-' + scoreFrame[10]
            # 获取商品简介信息
            frames = d.find('#parameter2>li')
            commondityName = '-'
            commondityCode = '-'
            shelvesTime = '-'
            goodsWeight = '-'
            shopName = '-'
            function = '-'
            type = '-'
            originOfGoods = '-'
            usage = '-'
            system = '-'
            productNo = '-'
            compatibility = '-'
            applicableCrowd = '-'
            brand = '-'
            theoreticalEndurance = '-'
            rateOfWork = '-'
            for item in frames:
                d = pq(item)
                text = d.text()
                text = text.split('：')
                textTest = text[0]
                textTarget = text[1]
                # 用于字段测试
                # queue_for_test.put([url,textTest])
                if textTest == u'商品名称':
                    commondityName = textTarget
                elif textTest == u'商品编号':
                    commondityCode = textTarget
                elif textTest == u'上架时间':
                    shelvesTime = textTarget
                elif textTest == u'商品毛重':
                    goodsWeight = textTarget
                elif textTest == u'店铺':
                    shopName = textTarget
                elif textTest == u'功能':
                    function = textTarget
                elif textTest == u'类型':
                    type = textTarget
                elif textTest == u'商品产地':
                    originOfGoods = textTarget
                elif textTest == u'使用方式':
                    usage = textTarget
                elif textTest == u'系统':
                    system = textTarget
                elif textTest == u'货号':
                    productNo = textTarget
                elif textTest == u'兼容性':
                    compatibility = textTarget
                elif textTest == u'适用人群' or textTest == u'适用对象':
                    applicableCrowd = textTarget
                elif textTest == u'品牌':
                    brand = textTarget
                elif textTest == u'理论续航':
                    theoreticalEndurance = textTarget
                elif textTest == u'功率':
                    rateOfWork = textTarget
                else:
                    pass
            res_temp = [url, commondityName, commondityCode, shelvesTime, goodsWeight, shopName, function, type,
                        originOfGoods, usage, system, productNo, compatibility, applicableCrowd, brand,
                        theoreticalEndurance, rateOfWork,
                        scoreSum, scoreProduct, scoreProductAvg, scoreService, scoreServiceAvg, scoreExpress,
                        scoreExpressAvg, companyName]
            queue_for_InnerPageProdctDetail_result.put(res_temp)

    def run(self):
        self.getDetail()


def main_innerProductDetail(threadCount=50):
    # 抓取商品页面商品介绍（商品参数类）

    main_productDetail()

    global queue_for_InnerPageProdctDetail, queue_for_InnerPageProdctDetail_result
    queue_for_InnerPageProdctDetail = Queue(0)
    queue_for_InnerPageProdctDetail_result = Queue(0)

    for i in range(queue_for_result.qsize()):
        item = queue_for_result.get()[-1]
        queue_for_InnerPageProdctDetail.put(item)

    # 若单独执行InnerPageProductDetail类，则需为queue_for_InnerPageProductDetail赋值
    # fileName='D:/spider/jd/jd_intelligent_productInfoDetail_2015-08-25 09_48_22.csv'
    # dict = {}
    # with open(fileName,'r') as f:
    # reader = csv.reader(f)
    #     i = 0
    #     for row in reader:
    #         if i>0:
    #             dict[row[2]]=1
    #         i+=1
    # for item in dict.items():
    #     queue_for_InnerPageProdctDetail.put(item[0])

    # 抓取商品页面商品介绍（商品参数类）
    InnerPageProductDetail_thread = []
    for i in range(threadCount):
        InnerPageProductDetail_thread.append(InnerPageProductDetail())
    for item in InnerPageProductDetail_thread:
        item.start()
    for item in InnerPageProductDetail_thread:
        item.join()

    # 商品页面信息持久化
    resultForInnerPageProductDetail = []
    for i in range(queue_for_InnerPageProdctDetail_result.qsize()):
        resultForInnerPageProductDetail.append(queue_for_InnerPageProdctDetail_result.get())
    title = ['productUrl', 'commondityName', 'commondityCode', 'shelvesTime', 'goodsWeight', 'shopName', 'function',
             'type', 'originOfGoods', 'usage', 'system', 'productNo', 'compatibility', 'applicableCrowd',
             'brand', 'theoreticalEndurance', 'rateOfWork', 'scoreSum', 'scoreProduct', 'scoreProductAvg',
             'scoreService', 'scoreServiceAvg', 'scoreExpress', 'scoreExpressAvg', 'companyName']
    # 数据写入csv文件
    writer = MyCsv.Write_Csv(path=dirCheck.dirGen('d:/spider/jd'), name='InnerPageProductDetail',
                             title=title, result=resultForInnerPageProductDetail)
    writer.add_title_data()


class ProductPrice(Thread):
    def __init__(self):
        Thread.__init__(self)

    def produPrice(self):
        while queue_for_ProductPrice.qsize() > 0:
            sku = queue_for_ProductPrice.get()
            url = 'http://p.3.cn/prices/get?skuid=J_' + sku
            src = myUrlOpen.requestByProxy(url)
            jsonFile = src[1:-2]
            d = json.loads(jsonFile)
            res = [sku, d['p'], d['m']]
            print(res)
            queue_for_ProductPrice_result.put(res)

    def run(self):
        self.produPrice()


def main_ProductPrice(threadCound=50):
    # 注，本段代码未引用其他类
    global queue_for_ProductPrice, queue_for_ProductPrice_result
    queue_for_ProductPrice = Queue(0)
    queue_for_ProductPrice_result = Queue(0)
    # 若单独执行ProductPrice类，则需为queue_for_ProductPrice赋值
    fileName = 'D:/spider/jd/jd_intelligent_productInfoDetail_2015-08-25 09_48_22.csv'
    # fileName = 'D:/spider/jd/jd_intelligent_productInfoDetail_2015-08-25 01_41_33.csv'
    dict = {}
    with open(fileName, 'r') as f:
        reader = csv.reader(f)
        i = 0
        for row in reader:
            if i > 0:
                dict[row[2]] = 1
            i += 1
    for item in dict.items():
        queue_for_ProductPrice.put(item[0].split('/')[-1].split('.')[0])

    ProductPrice_thread = []
    for i in range(threadCound):
        ProductPrice_thread.append(ProductPrice())
    for item in ProductPrice_thread:
        item.start()
    for item in ProductPrice_thread:
        item.join()

    result = []
    for i in range(queue_for_ProductPrice_result.qsize()):
        result.append(queue_for_ProductPrice_result.get())
    title = ['productSku', 'price', 'M']
    # 数据写入csv文件
    writer = MyCsv.Write_Csv(path=dirCheck.dirGen('d:/spider/jd/productDetail'), name='ProductPrice',
                             title=title, result=result)
    writer.add_title_data()


# 商品评论抓取类
class CommentDetail(Thread):
    def __init__(self):
        Thread.__init__(self)

    def getCommentDetail_FirstPage(self):
        # 抓取策略：因评论信息都是动态的，为尽量避免因动态添加的评论而引起的重复抓取问题，以每个产品对应内容为单个抓取单元
        proxy_port = myProxy.is_proxy_exists()
        proxy = random.sample(proxy_port, 1)[0]
        proxy = proxy[0] + ':' + proxy[1]
        proxyHandler = urllib2.ProxyHandler({'http': r'http://%s' % proxy})
        cookies = urllib2.HTTPCookieProcessor
        opener = urllib2.build_opener(cookies, proxyHandler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0')]

        while queue_sku_commentDetail.qsize() > 0:
            print('=' * 15 + u'还剩下%s个待抓SKU！' % queue_sku_commentDetail.qsize())
            sku = queue_sku_commentDetail.get()
            # 第一个评论页面地址;;参数p-0
            url = 'http://s.club.jd.com/productpage/p-' + str(sku) + '-s-0-t-0-p-0.html?callback=fetchJSON_comment'
            # 返回第一页评论数据及评论总量
            try:
                res_temp = opener.open(url)
                src = res_temp.read()
                res_temp.close()
                jsonFile = src.split('(', 1)[1][:-2]
            except:
                queue_sku_commentDetail.put(sku)
                proxy = random.sample(proxy_port, 1)[0]
                print(u'更换代理：%s:%s' % (proxy[0], proxy[1]))
                proxy = proxy[0] + ':' + proxy[1]
                proxyHandler = urllib2.ProxyHandler({'http': r'http://%s' % proxy})
                opener = urllib2.build_opener(cookies, proxyHandler)
                continue
            try:
                jsonFile = jsonFile.decode('GBK', 'ignore')
                jsonFile = json.loads(jsonFile)
            except:
                continue
            # 评论总量提取并依据此数生成url,并put至queue备用
            commentCount = jsonFile['productCommentSummary']['commentCount']
            pageCount = commentCount / 10 if commentCount % 10 == 0 else 1 + commentCount / 10
            if pageCount > 1:
                for i in range(1, pageCount):
                    url = 'http://s.club.jd.com/productpage/p-' + str(sku) + '-s-0-t-0-p-' + str(
                        i) + '.html?callback=fetchJSON_comment'
                    queue_skuPageUrl_commentDetail.put((sku, url))

            # 评论信息提取
            commentList = jsonFile['comments']
            for item in commentList:
                userId = item['id']
                userGuid = item['guid']
                content = item['content']
                createTime = item['creationTime']
                referenceId = item['referenceId']
                referenceTime = item['referenceTime']
                replyCount = item['replyCount']
                score = item['score']
                userLevelId = item['userLevelId']
                userProvince = item['userProvince']
                try:
                    productColor = item['productColor']
                except:
                    productColor = '-'
                userLevelName = item['userLevelName']
                userClientShow = item['userClientShow']
                userClientShow = userClientShow.split('>', 1)[1].split('<', 1)[0] if userClientShow else '-'
                isMobile = item['isMobile']
                resultTemp = [sku, userId, userGuid, content, createTime, referenceId,
                              referenceTime, replyCount, score, userLevelId, userProvince, productColor,
                              userLevelName, userClientShow, isMobile, url
                              ]
                queue_commentDetail_result.put(resultTemp)

    # 除第一个页面外其余页面评论信息抓取
    def getCommentDetail_OtherPage(self):
        proxy_port = myProxy.is_proxy_exists()
        proxy = random.sample(proxy_port, 1)[0]
        proxy = proxy[0] + ':' + proxy[1]
        proxyHandler = urllib2.ProxyHandler({'http': r'http://%s' % proxy})
        cookies = urllib2.HTTPCookieProcessor
        opener = urllib2.build_opener(cookies, proxyHandler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0')]

        while queue_skuPageUrl_commentDetail.qsize() > 0:
            if queue_skuPageUrl_commentDetail.qsize() % 1000 == 0:
                print('=' * 15 + u'还剩下%s个待抓评论页面！' % queue_skuPageUrl_commentDetail.qsize())
                print('+' * 15 + u'已抓取评论数量总计%s条！' % queue_commentDetail_result.qsize())
            # 评论信息持久化，动态清除内存

            sku, url = queue_skuPageUrl_commentDetail.get()
            try:
                res_temp = opener.open(url)
                src = res_temp.read()
                res_temp.close()
                jsonFile = src.split('(', 1)[1][:-2]
            except:
                queue_skuPageUrl_commentDetail.put((sku, url))
                proxy = random.sample(proxy_port, 1)[0]
                # print(u'更换代理：%s:%s'%(proxy[0],proxy[1]))
                proxy = proxy[0] + ':' + proxy[1]
                proxyHandler = urllib2.ProxyHandler({'http': r'http://%s' % proxy})
                opener = urllib2.build_opener(cookies, proxyHandler)
                continue
            try:
                jsonFile = jsonFile.decode('GBK', 'ignore')
                jsonFile = json.loads(jsonFile)
            except:
                continue
            commentList = jsonFile['comments']
            for item in commentList:
                userId = item['id']
                userGuid = item['guid']
                content = item['content']
                createTime = item['creationTime']
                referenceId = item['referenceId']
                referenceTime = item['referenceTime']
                replyCount = item['replyCount']
                score = item['score']
                userLevelId = item['userLevelId']
                userProvince = item['userProvince']
                try:
                    productColor = item['productColor']
                except:
                    productColor = '-'
                userLevelName = item['userLevelName']
                userClientShow = item['userClientShow']
                userClientShow = userClientShow.split('>', 1)[1].split('<', 1)[0] if userClientShow else '-'
                isMobile = item['isMobile']
                resultTemp = [sku, userId, userGuid, content, createTime, referenceId,
                              referenceTime, replyCount, score, userLevelId, userProvince, productColor,
                              userLevelName, userClientShow, isMobile, url
                              ]
                queue_commentDetail_result.put(resultTemp)

    def run(self):
        self.getCommentDetail_FirstPage()
        self.getCommentDetail_OtherPage()


def main_CommentDetail(fileName=dirCheck.dirGen('D:\spider\jd\InnerPageProductDetail_2015-08-26 10_53_41.csv'),
                       columnNo=2, threadCount=50):
    global queue_sku_commentDetail, queue_skuPageUrl_commentDetail, queue_commentDetail_result
    queue_sku_commentDetail = Queue(0)
    queue_skuPageUrl_commentDetail = Queue(0)
    queue_commentDetail_result = Queue(0)

    # 参数说明;fileName为需打开的文件绝对路径加文件名；columnNo为特定字段在第几列（第一列为0）；threadCount为开启线程数，默认开启50个线程
    # sku信息put至queue备用
    with open(fileName, 'r') as f:
        reader = csv.reader(f)
        i = 1
        for row in reader:
            if i > 1:
                queue_sku_commentDetail.put(row[columnNo])
            i += 1

    # 评论信息抓取
    CommentDetail_thread = []
    for i in range(threadCount):
        CommentDetail_thread.append(CommentDetail())
    for item in CommentDetail_thread:
        item.start()
        time.sleep(0.01)

    while True:
        if queue_commentDetail_result.qsize() > 200000:
            resultForCommentDetail = []
            for i in range(200000):
                resultForCommentDetail.append(queue_commentDetail_result.get())
            title = ['productSku', 'userId', 'userGuid', 'content', 'createTime', 'referenceId',
                     'referenceTime', 'replyCount', 'score', 'userLevelId', 'userProvince',
                     'productColor', 'userLevelName', 'userClientShow', 'isMobile', 'urlFrom'
                     ]
            # 数据写入csv文件
            writer = MyCsv.Write_Csv(path=dirCheck.dirGen('d:/spider/jd/commentDetail'), name='commentDetail',
                                     title=title, result=resultForCommentDetail)
            writer.add_title_data()
        if queue_skuPageUrl_commentDetail.qsize() == 0:
            break

    # for item in CommentDetail_thread:
    # item.join()

    # 评论信息持久化
    resultForCommentDetail = []
    for i in range(queue_commentDetail_result.qsize()):
        resultForCommentDetail.append(queue_commentDetail_result.get())
    title = ['productSku', 'userId', 'userGuid', 'content', 'createTime', 'referenceId',
             'referenceTime', 'replyCount', 'score', 'userLevelId', 'userProvince',
             'productColor', 'userLevelName', 'userClientShow', 'isMobile'
             ]
    # 数据写入csv文件
    writer = MyCsv.Write_Csv(path=dirCheck.dirGen('d:/spider/jd/commentDetail'), name='commentDetail',
                             title=title, result=resultForCommentDetail)
    writer.add_title_data()


def my_dirCheck():
    dirCheck.ifDirOrCreate(root='d:', directory_1st='spider')
    dirCheck.ifDirOrCreate(root='d:/spider', directory_1st='jd',
                           directory_2nd=['brandList', 'productDetail', 'InnerPageProductDetail', 'commentDetail',
                                          'brand_pagesource'])


if __name__ == '__main__':
    my_dirCheck()
    # 产品名称、链接等抓取
    # main_productDetail(threadCount=100)
    # 产品页面信息（产品简介等）抓取
    # main_innerProductDetail(threadCount=100)
    # 评论信息抓取
    # main_CommentDetail(threadCount=200)
    # 价格抓取
    main_ProductPrice(200)
