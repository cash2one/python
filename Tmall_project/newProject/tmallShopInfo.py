# coding:utf-8
__author__ = '613108'
import time
import urllib
import sys
import socket
import json
import re
from threading import Thread
from Queue import Queue

from myTool import dirCheck, myUrlOpen, MyCsv

reload(sys)
sys.setdefaultencoding('utf-8')
socket.setdefaulttimeout(60)


class GetKeyWord():
    def __init__(self):
        pass

    def run_getKeyWord(self):
        """
        edit 20151013
        :return:
        """
        from selenium import webdriver
        from selenium.webdriver.common.action_chains import ActionChains
        import time

        dri = webdriver.PhantomJS()
        dri.get('http://www.tmall.com')
        dri.maximize_window()
        clickElement = dri.find_elements_by_css_selector('.j_MenuNav.nav-item')[:2]
        text = []
        time.sleep(10)
        for item in clickElement:
            ActionChains(dri).move_to_element(item).perform()
            time.sleep(2)
            fra = dri.find_elements_by_css_selector('.label-list a')
            for item in fra:
                t = item.text
                if t:
                    text.append(item.text)
                    print(t)
        dri.quit()

        text = map(lambda x: x.replace(u'双11', ''), text)
        for item in text:
            print(item)
        text = set(text)
        text = list(text)
        with open('d:/spider/tmall/keyWord.txt', 'a') as f:
            f.write('++' + '++'.join(text))
        return text

    def run(self, usingLocalFile=1):
        def openLocalFile():
            with open('d:/spider/tmall/keyword.txt', 'r')as f:
                temp = f.read()
            keyword = temp.split('++')
            keyword = map(lambda x: x.replace('双11', ""), keyword)
            return list(set(keyword))

        if not usingLocalFile:
            self.run_getKeyWord()

        keyword = openLocalFile()

        for item in keyword:
            if item:
                queue_GetShopList_keyWord.put(item)


def main_GetKeyWord():
    global queue_GetShopList_keyWord
    queue_GetShopList_keyWord = Queue(0)
    GetKeyWord().run(usingLocalFile=1)


class GetShopList(Thread):
    def __init__(self):
        Thread.__init__(self)

    def getShopInfo(self):
        while not queue_GetShopList_keyWord.empty():
            keyWord = queue_GetShopList_keyWord.get()
            getData = {'initiative_id': 'staobaoz_20120515', 'q': keyWord, 'app': 'shopsearch', 'fs': 1, 'isb': 1,
                       'goodrate': '', 's': 0}
            urlStart = 'https://s.taobao.com/search?' + urllib.urlencode(getData)
            src = myUrlOpen.requestByProxy(urlStart)
            src = src.decode('gbk', 'ignore')
            # rebuild on 2016/01/18
            pageCount_t = re.findall(r'"totalPage":\d+\,?', src)
            if pageCount_t:
                pageCount = int(pageCount_t[0].split(':')[1][:-1])
            else:continue

            print(keyWord)
            print(pageCount)
            if pageCount:
                for i in range(0, pageCount * 20, 20):
                    getData = {'initiative_id': 'staobaoz_20120515', 'q': keyWord, 'app': 'shopsearch', 'fs': 1,
                               'isb': 1,
                               'goodrate': '', 's': i}
                    url = 'https://s.taobao.com/search?' + urllib.urlencode(getData)
                    queue_GetShopList_url.put(url)
                    # print(url)

        while queue_GetShopList_url.qsize() > 0:
            url = queue_GetShopList_url.get()
            src = myUrlOpen.requestByProxy(url)
            pat = re.compile(r'g_page_config = {.+};')
            temp = re.findall(pat, src)[0][16:-1]
            res = json.loads(temp)
            try:
                res = res['mods']['shoplist']['data']['shopItems']
            except KeyError:
                print('KeyError')
                continue
            for item in res:
                tempForScoreGet_t = ['mas', 'mg', 'sas', 'sg', 'cas', 'cg', 'sgr', 'srn', 'encryptedUserId']
                item_inner_2 = json.loads(item.get('dsrInfo').get('dsrStr'))
                score = map(lambda x: item_inner_2[x], tempForScoreGet_t)
                dataUid = item.get('uid')
                shopHref = 'http:' + item.get('shopUrl')
                shopName = item.get('title')
                addr = item.get('provcity')
                brand = item.get('mainAuction')
                monthSale = item.get('totalsold')
                productSum = item.get('procnt')
                if item.get('auctionsInshop'):
                    tempForProductPromot = reduce(lambda x, y: x + y,
                                                  map(lambda x: [x['nid'], x['url'], x['price']],
                                                      item['auctionsInshop']))
                else:
                    tempForProductPromot = map(lambda x: '-', range(12))
                if len(tempForProductPromot) < 12:
                    tempForProductPromot.extend(map(lambda x: '-', range(12 - len(tempForProductPromot))))
                Result = [shopName, shopHref, addr, brand, monthSale, productSum] + score + tempForProductPromot + [
                    dataUid]
                queue_GetShopList_result.put(Result)

    def run(self):
        self.getShopInfo()


def main_GetShopList(threadCount=50):
    main_GetKeyWord()

    global queue_GetShopList_url, queue_GetShopList_result
    queue_GetShopList_url = Queue(0)
    queue_GetShopList_result = Queue(0)

    GetShopList_thread = []
    for i in range(threadCount):
        GetShopList_thread.append(GetShopList())
    for item in GetShopList_thread:
        item.start()

    time.sleep(100)

    title = ['name', 'href', 'addr', 'brnad', 'monthsale', 'productsum', 'dsr_desc_mark', 'dsr_desc_avg',
             'dsr_service_mark',
             'dsr_service_avg', 'dsr_sending_mark', 'dsr_sending_avg', 'sgr', 'srn', 'encryptedUserId',
             'productDataNid_1', 'product_link_1', 'price_1', 'productDataNid_2', 'product_link_2', 'price_2',
             'productDataNid_3', 'product_link_3', 'price_3', 'productDataNid_4', 'product_link_4', 'price_4',
             'shopDataUid']

    count=1

    while queue_GetShopList_url.qsize() > 0:
        if queue_GetShopList_result.qsize() > 20000:
            result = []
            for i in range(20000):
                result.append(queue_GetShopList_result.get())
            writer = MyCsv.Write_Csv(path=dirCheck.dirGen('d:/spider/tmall/baseInfo'), name='shopInfo',
                                     title=title, result=result)
            writer.add_title_data()
            print(u'第 %s 个文件已输出，请检查数据！' % count)
            count += 1

    # 输出最后一个文件
    result = []
    for i in range(queue_GetShopList_result.qsize()):
        result.append(queue_GetShopList_result.get(timeout=20))
    writer = MyCsv.Write_Csv(path=dirCheck.dirGen('d:/spider/tmall/baseInfo'), name='shopInfo',
                             title=title, result=result)
    writer.add_title_data()
    print(u'最后一个文件已输出，请检查数据！')


# class ShopItem(Thread):
#     def __init__(self):
#         Thread.__init__(self)
#
#     def getShopItem(self):
#         while not queue_for_ShopDataUid.empty():
#             shopDataUid = queue_for_ShopDataUid.get()
#             urlData = {'from': 1, 'sort': 's', 'style': 'sg', 'user_id': shopDataUid, 's': 0}
#             urlHeader = 'http://list.tmall.com/search_shopitem.htm?'
#             url = urlHeader + urllib.urlencode(urlData)
#             # print(url)
#             # src = myUrlOpen.requestByProxy('http://1111.ip138.com/ic.asp')
#             # print(src)
#             src = myUrlOpen.requestByProxy(url)
#             # print(src)
#             d = pq(src)
#             frames = d.find('.product-iWrap')
#             print(len(frames))
#
#     def run(self):
#         self.getShopItem()
#
#
# def getShopDataUid(fileName):
#     d = {}
#     with open(fileName, 'r') as f:
#         reader = csv.reader(f)
#         i = 1
#         for row in reader:
#             if i == 1:
#                 pass
#             else:
#                 d[row[-1]] = 1
#             i += 1
#     for item in d.items():
#         queue_for_ShopDataUid.put(item[0])
#
#
# def main_ShopItem(threadCount):
#     global queue_for_ShopDataUid
#     queue_for_ShopDataUid = Queue(0)
#     getShopDataUid(r'C:\Users\613108\Desktop\tmall\shopDistinct_2015-08-28 15_54_23.csv')
#
#     ShopItem_thread = []
#     for i in range(threadCount):
#         ShopItem_thread.append(ShopItem())
#     for item in ShopItem_thread:
#         item.start()
#     for item in ShopItem_thread:
#         item.join()
#
#
# class ProductInfoFromListUrl(Thread):
#     def __init__(self):
#         Thread.__init__(self)
#
#     def getInfo(self):
#         while not queue_for_ProductInfoFromListUrl_url.empty():
#             url, referer = queue_for_ProductInfoFromListUrl_url.get()
#             print(url)
#             # url='http://www.tmall.com'
#             src = myUrlOpen.requestByProxyAddReferer(url, referer)
#             with open('text%s.html' % url.split('//')[1], 'wb') as f:
#                 f.write(src)
#             d = pq(src)
#             print(d.find('title').text())
#             frames = d.find('.product-iWrap')
#             print(len(frames))
#             for item in frames:
#                 d = pq(item)
#                 href = 'https:' + d.find('.productImg').attr('href')
#                 price = d.find('.productPrice>em').attr('title')
#                 tmallIdentification = d.find('.productPrice>a>img').attr('title')
#                 title = d.find('.productTitle').text()
#                 shop = d.find('.productShop>a').text()
#                 saleCount = d.find('.productStatus>span:nth-child(1)>em').text()[:-1]
#                 commentCount = d.find('.productStatus>span:nth-child(2)>a').text()
#                 result = [title, href, price, tmallIdentification, shop, saleCount, commentCount, url]
#                 print(result)
#                 queue_for_ProductInfoFromListUrl_result.put(result)
#
#     def run(self):
#         self.getInfo()
#
#
# def main_ProductInfoFromListUrl(threadCount=1):
#     global queue_for_ProductInfoFromListUrl_url, queue_for_ProductInfoFromListUrl_result
#     queue_for_ProductInfoFromListUrl_url = Queue(0)
#     queue_for_ProductInfoFromListUrl_result = Queue(0)
#
#     url_base = 'https://list.tmall.com/search_product.htm?spm=a220m.1000858.0.0.2Km9BG&cat=56148012&s='
#     url_after = '&sort=s&style=g&search_condition=7&from=sn_1_rightnav&active=1&industryCatId=55852013&theme=551&tmhkmain=0&type=pc'
#
#     for i in range(0, 100 * 60, 60):
#         if i == 0:
#             queue_for_ProductInfoFromListUrl_url.put((url_base + str(i) + url_after, 'www.tmall.com'))
#             print((url_base + str(i) + url_after, 'www.tmall.com'))
#         else:
#             queue_for_ProductInfoFromListUrl_url.put(
#                     (url_base + str(i) + url_after, url_base + str(i - 60) + url_after))
#
#     ProductInfoFromListUrl_thread = []
#     for i in range(threadCount):
#         ProductInfoFromListUrl_thread.append(ProductInfoFromListUrl())
#     for item in ProductInfoFromListUrl_thread:
#         item.start()
#     for item in ProductInfoFromListUrl_thread:
#         item.join()
#
#     result = []
#     for i in range(queue_for_ProductInfoFromListUrl_result.qsize()):
#         result.append(queue_for_ProductInfoFromListUrl_result.get())
#     title = ['title', 'href', 'price', 'tmallIdentification', 'shop', 'saleCount', 'commentCount', 'urlFrom']
#     # 数据写入csv文件
#     writer = MyCsv.Write_Csv(path=dirCheck.dirGen('d:/spider/tmall'), name=u'智能设备Info',
#                              title=title, result=result)
#     writer.add_title_data()
#     print(u'文件已输出，请检查数据！')
#
#
# # 天猫高科技商品信息页面分析
# def productInfoFromLocalSrc(path):
#     fileList = os.listdir(path)
#     result = []
#     for item in fileList:
#         with open(path + '/' + item, 'r') as f:
#             temp = f.read()
#         temp = temp.decode('utf-8', 'ignore')
#         d = pq(temp)
#         frames = d.find('.product-iWrap')
#         print(len(frames))
#         for itemIneer in frames:
#             d = pq(itemIneer)
#             href = 'https:' + d.find('.productImg').attr('href')
#             price = d.find('.productPrice>em').attr('title')
#             tmallIdentification = d.find('.productPrice>a>img').attr('title')
#             title = d.find('.productTitle').text()
#             shop = d.find('.productShop>a').text()
#             saleCount = d.find('.productStatus>span:nth-child(1)>em').text()[:-1]
#             commentCount = d.find('.productStatus>span:nth-child(2)>a').text()
#             res = [title, href, price, tmallIdentification, shop, saleCount, commentCount]
#             result.append(res)
#     title = ['title', 'href', 'price', 'tmallIdentification', 'shop', 'saleCount', 'commentCount']
#     # 数据写入csv文件
#     writer = MyCsv.Write_Csv(path=dirCheck.dirGen('d:/spider/tmall'), name=u'智能设备Info',
#                              title=title, result=result)
#     writer.add_title_data()
#     print(u'文件已输出，请检查数据！')
#
#
# def test(fileName):
#     temp = myUrlOpen.requestByProxy('https://rate.taobao.com/user-rate-UvGkuvGQYvGNy.htm')
#     # with open(fileName, 'r') as f:
#     #     temp = f.read()
#     temp = temp.decode('GBK', 'ignore')
#     d = pq(temp)
#     framesDetail = d.find('.count')
#     textDetail = framesDetail.my_text()[3:]  # 所有细项评分比例
#     framesCount = d.find('.total>span')
#     textCount = [framesCount.my_text()[0]]  # 参与评分人数
#     framesOther = d.find('.title+ul>li')
#     textOther = framesOther.my_text()  # 公司名称所在地等
#     tempForTextOther = ['公 司 名：', '当前主营：', '开店时长：']
#     textOther = [textOther[i + 1] for item in tempForTextOther for i in range(len(textOther)) if textOther[i] == item]
#     result = textCount + textDetail + textOther
#     for item in result:
#         print(item)
#
#
# class CommentDetailCount(Thread):
#     def __init__(self):
#         Thread.__init__(self)
#
#     def getINfo(self):
#         while not queue_for_CommentDetailCount.empty():
#             # time.sleep(abs(random.gauss(5, 2)))
#             urlKeyWord = queue_for_CommentDetailCount.get()
#             urlBase = 'https://rate.taobao.com/user-rate-'
#             url = urlBase + urlKeyWord + '.htm?spm=a1z10.3-b.d4918101.' + spmKeywordRandom()
#             temp = myUrlOpen.requestByProxy(url)
#             temp = temp.decode('GBK', 'ignore')
#             d = pq(temp)
#             framesDetail = d.find('.count')
#             textDetail = framesDetail.my_text()[3:]  # 所有细项评分比例
#             if not textDetail:
#                 textDetail = []
#             framesCount = d.find('.total>span')
#             try:
#                 textCount = [framesCount.my_text()[0]]  # 参与评分人数
#             except:
#                 textCount = ['-']
#             framesOther = d.find('.title+ul>li')
#             textOther = framesOther.my_text()  # 公司名称所在地等
#             tempForTextOther = ['公 司 名：', '当前主营：', '开店时长：']
#             textOther = [textOther[i + 1] for item in tempForTextOther for i in range(len(textOther)) if
#                          textOther[i] == item]
#             print(textCount, textDetail, textOther)
#             result = textCount + textDetail + textOther
#             result.append(urlKeyWord)
#             # for item in result:
#             #     print(item)
#
#     def run(self):
#         self.getINfo()
#
#
# def spmKeywordRandom():
#     res = []
#     for i in range(0, 6):
#         tempFi = random.randint(65, 90)
#         tempSe = random.randint(97, 122)
#         tempForSelect = random.randint(1, 2)
#         if len(res) < 1:
#             res.append(str(tempForSelect) + '.')
#         if tempForSelect == 1:
#             temp = chr(tempFi)
#             res.append(temp)
#         else:
#             temp = chr(tempSe)
#             res.append(temp)
#     res = ''.join(res)
#     return res
#
#
# def main_CommentDetailCount(path, threadCount=50):
#     global queue_for_CommentDetailCount
#     queue_for_CommentDetailCount = Queue(0)
#     fileList = os.listdir(path)
#     for item in fileList:
#         with open(path + '/' + item, 'r') as f:
#             reader = csv.reader(f)
#             i = 1
#             for row in reader:
#                 if i == 1:
#                     pass
#                 else:
#                     queue_for_CommentDetailCount.put(row[14])
#                 i += 1
#
#     CommentDetailCount_thread = []
#     for i in range(threadCount):
#         CommentDetailCount_thread.append(CommentDetailCount())
#     for item in CommentDetailCount_thread:
#         item.start()
#     for item in CommentDetailCount_thread:
#         item.join()


if __name__ == '__main__':
    print('Start')
    main_GetShopList(100)