from ms_spider_fw.DBSerivce import DBService

db = DBService(dbName='tmalldata', tableName='need_view')
text = db.getData(var='shopName')
text = map(lambda x: x[0], text)
for item in text:
    print(item)
####################################################################################################
# 三年规划
import pymysql

connect = pymysql.connect(host='10.118.187.12', user='admin', password='admin', charset='utf8', database='jddata')
import pandas as pd

sql_1 = "SELECT t.companyName,t.productHref FROM `thirdPartShopInfo` t HAVING t.companyName!='-'"
sql_2 = "SELECT t.companyName,t.productHref FROM `thirdPartShopInfo` t HAVING t.companyName='-'"
sql_3 = "SELECT t.productHref,t.commentCount FROM `jdproductbaseinfo2database` t"
df1 = pd.read_sql(sql=sql_1, con=connect)
df2 = pd.read_sql(sql=sql_2, con=connect)
df3 = pd.read_sql(sql=sql_3, con=connect)
df4 = df3.drop_duplicates(cols='productHref', take_last=True)
# df4['platform']=df4.pageUrl.apply(lambda x:x.split('cat=')[-1].replace('%2C',','))
df5 = pd.merge(df1, df4, how="left", left_on='productHref', right_on='productHref')
df6 = pd.merge(df2, df4, how="left", left_on='productHref', right_on='productHref')
df5['count'] = df5['commentCount'].apply(lambda x: int(x) if x.isdigit() else 0)
df5.groupby("companyName").sum()
# df5.drop('count',axis=1)
df6['count'] = df6['commentCount'].apply(lambda x: int(x) if x.isdigit() else 0)
df6.groupby("companyName").sum()
sql_7 = "SELECT t.category_ti,t.category_ti_name,t.category_se_name,t.category_fi_name FROM `jdkeyword` t"
df7 = pd.read_sql(sql=sql_7, con=connect)
df7['platform'] = df7['category_ti'].apply(lambda x: x.replace('-', ','))
df8 = pd.merge(df4, df7, how='left', left_on='platform', right_on='platform')
df8['count'] = df8['commentCount'].apply(lambda x: int(x) if x.isdigit() else 0)
df8.groupby(['category_fi_name', 'category_se_name', 'category_ti_name']).sum()
df8['ifThirdPart'] = df8['productHref'].apply(lambda x: 'YES' if len(x.split('/')[-1].split('.')[0]) >= 9 else "NO")

####################################################################################################
# 手机、运动户外两个行业每周销量数据
# 2015-12-07
import pymysql

connect = pymysql.connect(host='10.118.187.12', user='admin', password='admin', charset='utf8',
                          database='elec_platform')
import pandas as pd

sql_1 = "SELECT t.`name`,t.monthsale,t.addr,t.spider_time FROM `tmall_baseinfo_everyweek` t"
sql_2 = "SELECT t.`name`,t.major_business FROM `yms_tmall_shopinfo_com_withoutjudge` t"
df1 = pd.read_sql(sql=sql_1, con=connect)
df1['date'] = df1['spider_time'].apply(lambda x: x.split(' ')[0])
df2 = pd.read_sql(sql=sql_2, con=connect)
df3 = pd.merge(df1, df2, how='left', left_on='name', right_on='name')
df4 = df3.drop('spider_time', axis=1)
temp = [u'手机', u'运动/户外']
df5 = df4[df4['major_business'].isin(temp)]

# JD_Guangdongprovice
# create on:2015-12-25
import pymysql

connect = pymysql.connect(host='10.118.187.12', user='admin', password='admin', charset='utf8', database='jddata')
import pandas as pd

sql_1 = 'SELECT * FROM `thirdPartShopInfo`;'
df1 = pd.read_sql(sql=sql_1, con=connect)
df1 = df1.drop(['productHref', 'id'], axis=1)
df1 = df1.sort(columns=['shopName', 'gradeHref'])
df2 = df1.drop_duplicates(['shopName'])
df2.to_csv(path_or_buf='/home/appdeploy/jd_all_shop.csv', index=False)

import cookielib

print cookielib.MozillaCookieJar(r'D:\spider\tmall\cookeis\cookies.txt')

import requests

url_tes = requests.get('http://www.amazon.cn/运动-户外-休闲/dp/B00OC4V7I4')
from pyquery.pyquery import PyQuery as pq

d = pq(url_tes.text)
for item in d.my_text():
    if len(item) < 200:
        print item.decode('gbk', 'ignore')

from pyquery.pyquery import PyQuery as pq

with open('D:/temp1.html', 'r')as f:
    url_tes = f.read()
d = pq(url_tes)
f = open(u'儿童手表_brand.txt', 'w')
for x in d.find('.av-scroll>li>a').items():
    print x.attr('title').decode('gbk', 'ignore')
    f.write(x.attr('title') + ' ')
f.close()

from myTool import MyCsv

with open('d:/child_watch_brand.txt', 'r')as f:
    url_tes = f.read()
t_1 = map(lambda x: x.split('/'), url_tes.split(' '))
f_1 = []
for i_0 in t_1:
    for i_1 in i_0:
        f_1.append([i_1, i_0[0], u'儿童手表'])

with open('d:/intelligent_watch_brand.txt', 'r')as f:
    url_tes = f.read()
t_2 = map(lambda x: x.split('/'), url_tes.split(' '))
f_2 = []
for i_0 in t_2:
    for i_1 in i_0:
        f_2.append([i_1, i_0[0], u'智能手表'])

with open('d:/sweep_machine_brand.txt', 'r')as f:
    url_tes = f.read()
t_3 = map(lambda x: x.split('/'), url_tes.split(' '))
f_3 = []
for i_0 in t_3:
    for i_1 in i_0:
        f_3.append([i_1, i_0[0], u'扫地机器人'])

ff = f_1 + f_2 + f_3

f = MyCsv.Write_Csv('d:/', 'brand_list.csv', title=['brand', 'detail', u'catalogue'], result=ff)

# rebuild on 2016/01/18
# tmall shop_search page parser
import re, json

with open('D:/demo.html', 'r')as f:
    src = f.read()
pat = re.compile(r'g_page_config = {.+};')
temp = re.findall(pat, src)[0][16:-1]
res = json.loads(temp)
res = res['mods']['shoplist']['data']['shopItems']

for item in res:
    item_inner_1 = item['dsrInfo']
    more_less_t = ['mgDomClass', 'sgDomClass', 'cgDomClass']
    more_less = map(lambda x: item_inner_1[x], more_less_t)
    tempForScoreGet_t = ['mas', 'mg', 'sas', 'sg', 'cas', 'cg', 'sgr', 'srn', 'encryptedUserId']
    item_inner_2 = json.loads(item['dsrInfo']['dsrStr'])
    score = map(lambda x: item_inner_2[x], tempForScoreGet_t)
    dataUid = item['uid']
    shopHref = 'http:' + item['shopUrl']
    shopName = item['title']
    addr = item['provcity']
    brand = item['mainAuction']
    monthSale = item['totalsold']
    productSum = item['procnt']

    tempForProductPromot = reduce(lambda x, y: x + y,
                                  map(lambda x: [x['nid'], x['url'], x['price']], item['auctionsInshop']))

    Result = [shopName, shopHref, addr, brand, monthSale, productSum] + score + tempForProductPromot + [
        dataUid]
    for item in Result:
        print item

with open('D:\spider\tmall\2016-01-18\shopInfo_2016-01-18 19_11_25.csv', 'r')as f:
    url_tes = f.readlines()

url_tes = map(lambda x: x.split(','), url_tes)
for item in url_tes[:100]:
    print(item)

from ms_spider_fw.DBSerivce import DBService

dbs = DBService(dbName='b2c_base', tableName='proxy_xi_ci_dai_li')
url_tes = dbs.getData(var='proxy_port', distinct=True)

# for jiuxian website_spider to extract info
pat = re.compile('_BFD\.BFD_INFO = \{(.+?)\};', re.DOTALL)

import logging
import os

logging.basicConfig(filename=os.path.join(os.getcwd(), 'log.txt'), level=logging.DEBUG)
logging.debug('this is a message.')

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

for item in tt:
    print '*' * 50
    for item in json.loads(item).items():
        try:
            print item[1].encode('utf8')
        except:
            print item[1]

# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-02-03 17:00:44
# Project: test_02

from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
    }

    def on_message(self, project, msg):
        return filter(lambda x: 1 if x[0] == project else 0, self._messages)

    @every(minutes=24 * 60)
    def on_start(self):
        url = self.on_message('yhd_product_url', 'data:')
        print url
        self.crawl('www.baidu.com', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            url = self.on_message('yhd_product_url', 'data:')
            print url
            self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }


url_tes = requests.post(url='http://www.jiuxian.com/pro/selectProActByProId.htm?t=1455698064208',
                        data={'proId': 2790, 'resId': 6})


# dangdang relation
def extract_info(url):
    import requests as req
    from pyquery.pyquery import PyQuery as pq
    print url + '/relation.html'
    d = pq(req.get(url + '/relation.html').content)
    return d('.contact>p').text().encode('utf8', 'ignore')


import pandas
import pymysql

connect_dict = {'host': '10.118.187.12', 'user': 'admin', 'passwd': 'admin', 'charset': 'utf8'}
conn = pymysql.connect(**connect_dict)
sql = 'select seller,category,seller_href,sold from platform_data.yhd_product_info'
data_fw = pandas.read_sql(sql, con=conn)
data_fw['sold_int'] = data_fw['sold'].apply(lambda x: int(x) if x.isdigit() else 0)
data_fw = data_fw.drop(['sold'], axis=1)
data_fw = data_fw.drop(data_fw['seller'].apply(lambda x: True if x == None else False), axis=0)
# data_fw_t=data_fw.sort_values(by='sold_int',ascending=False)
df1 = data_fw.groupby(['seller', 'seller_href']).sum()

sql_data = 'select * from platform_data.dangdang_relation'
df = pandas.read_sql(sql, con=conn)
import re

pat_tel = re.compile('\d{3,4}-\d{7,8}')
pat_mob = re.compile('1\d{10}')
pat_addr = re.compile(u'地\s*?址\s*?[:：]\s*?.+?\s', re.DOTALL)
pat_email = re.compile("[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}")
pat_qq = re.compile(u'QQ[:：]\s*?\d+\s*?|qq[:：]\s*?\d+\s*?|微信[:：]\s*?\d+\s*?', re.DOTALL)


def match_tel(x):
    if x:
        try:
            t = re.findall(pat_email, x)[0]
            if t:  # and t[0]<>t[1]:
                return t
            else:
                return ''
        except:
            return ''
    else:
        return ''


df['email'] = df['relation'].apply(match_tel)

import pymongo

client = pymongo.MongoClient(host='10.118.187.4', port=27017)
db = client.swan_database

# data = {
#     'product_name': '爱贝多Q5B 儿童手机 移动联通 定位低辐射 迷你可爱卡通孩子男生女生 幼儿园小学生电话 太空蓝',
#     'comment_list_url': 'http://club.jd.com/productpage/p-1548519301-s-0-t-3-p-1.html',
#     'comment_detail': """{"productAttr":null,"productCommentSummary":{"beginRowNumber":0,"endRowNumber":0,"skuId":1548519301,"productId":1548519301,"score1Count":2,"score2Count":0,"score3Count":2,"score4Count":3,"score5Count":46,"showCount":12,"commentCount":53,"averageScore":5,"goodCount":49,"goodRate":0.926,"goodRateShow":92,"goodRateStyle":138,"generalCount":2,"generalRate":0.037,"generalRateShow":4,"generalRateStyle":6,"poorCount":2,"poorRate":0.037,"poorRateShow":4,"poorRateStyle":6},"hotCommentTagStatistics":[{"id":1015396,"name":"信号稳定","status":0,"rid":15236,"productId":1548519301,"count":1,"created":"2015-09-27 13:21:06","modified":"2015-09-27 13:21:06"},{"id":1015397,"name":"待机时间长","status":0,"rid":15221,"productId":1548519301,"count":1,"created":"2015-09-27 13:21:06","modified":"2016-02-29 10:50:41"},{"id":1179140,"name":"系统流畅","status":0,"rid":15226,"productId":1548519301,"count":1,"created":"2016-02-29 10:50:41","modified":"2016-02-29 10:50:41"},{"id":1179141,"name":"外观漂亮","status":0,"rid":15225,"productId":1548519301,"count":1,"created":"2016-02-29 10:50:41","modified":"2016-02-29 10:50:41"}],"jwotestProduct":"98","score":0,"soType":3,"imageListCount":34,"comments":[{"id":1334913681,"guid":"13f9c115-023f-4f2d-9190-46b91ec8e897","content":"还行吧，字好小","creationTime":"2016-02-18 22:08:37","isTop":false,"referenceId":"1548519300","referenceImage":"jfs/t1258/329/796926091/232621/2a614876/55546649N75fb7745.jpg","referenceName":"爱贝多Q5B 儿童手机 移动联通 定位低辐射 迷你可爱卡通孩子男生女生 幼儿园小学生电话 太空蓝","referenceTime":"2016-02-05 08:48:45","referenceType":"Product","referenceTypeId":0,"firstCategory":9987,"secondCategory":653,"thirdCategory":655,"replyCount":0,"score":5,"status":1,"usefulVoteCount":0,"uselessVoteCount":0,"userImage":"misc.360buyimg.com/lib/img/u/b56.gif","userImageUrl":"misc.360buyimg.com/lib/img/u/b56.gif","userLevelId":"56","userProvince":"广东","userRegisterTime":"2014-07-25 21:16:52","viewCount":0,"orderId":0,"isReplyGrade":false,"nickname":"j***o","userClient":2,"productColor":"玫瑰红","productSize":"","integral":0,"anonymousFlag":1,"userLevelName":"铜牌会员","recommend":false,"userClientShow":"<a href='http://app.jd.com/iphone.html' target='_blank'>来自京东iPhone客户端</a>","isMobile":true,"days":13},{"id":1330322625,"guid":"11b6d7ae-fce9-45cb-b7f7-40f6192bc1f4","content":"很好用的一款儿童手机，女儿很喜欢，小巧适用，功能齐全，能够在手机上就操作了。","creationTime":"2016-02-16 12:43:52","isTop":false,"referenceId":"1548519300","referenceImage":"jfs/t1258/329/796926091/232621/2a614876/55546649N75fb7745.jpg","referenceName":"爱贝多Q5B 儿童手机 移动联通 定位低辐射 迷你可爱卡通孩子男生女生 幼儿园小学生电话 太空蓝","referenceTime":"2016-02-07 14:09:43","referenceType":"Product","referenceTypeId":0,"firstCategory":9987,"secondCategory":653,"thirdCategory":655,"replyCount":0,"score":5,"status":1,"usefulVoteCount":0,"uselessVoteCount":0,"userImage":"misc.360buyimg.com/lib/img/u/b50.gif","userImageUrl":"misc.360buyimg.com/lib/img/u/b50.gif","userLevelId":"90","userProvince":"四川","userRegisterTime":"2015-04-28 15:34:37","viewCount":0,"orderId":0,"isReplyGrade":false,"nickname":"我***猪","userClient":2,"images":[{"id":121251302,"associateId":73100361,"productId":0,"imgUrl":"http://img30.360buyimg.com/shaidan/s128x96_jfs/t1987/260/2121109594/126899/d3329158/56c2a907N46d458e7.jpg","available":1,"pin":"","dealt":0,"imgTitle":"","isMain":0},{"id":121251303,"associateId":73100361,"productId":0,"imgUrl":"http://img30.360buyimg.com/shaidan/s128x96_jfs/t2128/40/2126966946/143384/f23e6586/56c2a907Nded4882c.jpg","available":1,"pin":"","dealt":0,"imgTitle":"","isMain":0}],"showOrderComment":{"id":73100361,"guid":"524ab2f8-f9bc-4ec1-860f-fa999d22b29d","content":"很好用的一款儿童手机，女儿很喜欢，小巧适用，功能齐全，能够在手机上就操作了。<div class='uploadimgdiv'><img class='uploadimg' border='0'  src='http://img30.360buyimg.com/shaidan/jfs/t1987/260/2121109594/126899/d3329158/56c2a907N46d458e7.jpg' /></div><div class='uploadimgdiv'><img class='uploadimg' border='0'  src='http://img30.360buyimg.com/shaidan/jfs/t2128/40/2126966946/143384/f23e6586/56c2a907Nded4882c.jpg' /></div>","creationTime":"2016-02-16 12:43:52","isTop":false,"referenceId":"1548519300","referenceType":"Order","referenceTypeId":0,"firstCategory":0,"secondCategory":0,"thirdCategory":0,"replyCount":0,"score":0,"status":1,"usefulVoteCount":0,"uselessVoteCount":0,"userProvince":"","viewCount":0,"orderId":0,"isReplyGrade":false,"userClient":2,"isDeal":1,"integral":-20,"recommend":false,"userLevelColor":"#999999","userClientShow":"<a href='http://app.jd.com/iphone.html' target='_blank'>来自京东iPhone客户端</a>","isMobile":true},"mergeOrderStatus":2,"discussionId":73100361,"productColor":"玫瑰红","productSize":"","imageCount":2,"integral":-20,"anonymousFlag":1,"userLevelName":"企业会员","recommend":false,"userClientShow":"<a href='http://app.jd.com/iphone.html' target='_blank'>来自京东iPhone客户端</a>","isMobile":true,"days":9},{"id":1315592315,"guid":"61542141-2d05-44fc-8867-6e9af4b3fe11","content":"商品包装完好，感觉很好。外观漂亮，适合小孩。","creationTime":"2016-02-02 21:22:49","isTop":false,"referenceId":"1548519300","referenceImage":"jfs/t1258/329/796926091/232621/2a614876/55546649N75fb7745.jpg","referenceName":"爱贝多Q5B 儿童手机 移动联通 定位低辐射 迷你可爱卡通孩子男生女生 幼儿园小学生电话 太空蓝","referenceTime":"2016-01-31 22:26:20","referenceType":"Product","referenceTypeId":0,"firstCategory":9987,"secondCategory":653,"thirdCategory":655,"replyCount":0,"score":5,"status":1,"usefulVoteCount":0,"uselessVoteCount":0,"userImage":"misc.360buyimg.com/lib/img/u/b62.gif","userImageUrl":"misc.360buyimg.com/lib/img/u/b62.gif","userLevelId":"62","userProvince":"浙江","userRegisterTime":"2014-03-18 18:13:09","viewCount":0,"orderId":0,"isReplyGrade":false,"nickname":"s***q","userClient":4,"images":[{"id":119433865,"associateId":71976319,"productId":0,"imgUrl":"http://img30.360buyimg.com/shaidan/s128x96_jfs/t2005/116/1466081264/27602/42c5a374/56b0ada7N18e62ac6.jpg","available":1,"pin":"","dealt":0,"imgTitle":"","isMain":0},{"id":119433866,"associateId":71976319,"productId":0,"imgUrl":"http://img30.360buyimg.com/shaidan/s128x96_jfs/t1909/159/1470241416/30366/32df4d41/56b0ada8N530e5261.jpg","available":1,"pin":"","dealt":0,"imgTitle":"","isMain":0},{"id":119433867,"associateId":71976319,"productId":0,"imgUrl":"http://img30.360buyimg.com/shaidan/s128x96_jfs/t2128/305/2096234247/56586/e50adc1b/56b0ada9N00e8b9c5.jpg","available":1,"pin":"","dealt":0,"imgTitle":"","isMain":0}],"showOrderComment":{"id":71976319,"guid":"8822fe4a-6ba0-4964-acce-4d0617323c65","content":"商品包装完好，感觉很好。外观漂亮，适合小孩。<div class='uploadimgdiv'><img class='uploadimg' border='0'  src='http://img30.360buyimg.com/shaidan/jfs/t2005/116/1466081264/27602/42c5a374/56b0ada7N18e62ac6.jpg' /></div><div class='uploadimgdiv'><img class='uploadimg' border='0'  src='http://img30.360buyimg.com/shaidan/jfs/t1909/159/1470241416/30366/32df4d41/56b0ada8N530e5261.jpg' /></div><div class='uploadimgdiv'><img class='uploadimg' border='0'  src='http://img30.360buyimg.com/shaidan/jfs/t2128/305/2096234247/56586/e50adc1b/56b0ada9N00e8b9c5.jpg' /></div>","creationTime":"2016-02-02 21:22:49","isTop":false,"referenceId":"1548519300","referenceType":"Order","referenceTypeId":0,"firstCategory":0,"secondCategory":0,"thirdCategory":0,"replyCount":0,"score":0,"status":1,"usefulVoteCount":0,"uselessVoteCount":0,"userProvince":"","viewCount":0,"orderId":0,"isReplyGrade":false,"userClient":4,"isDeal":1,"integral":-20,"recommend":false,"userLevelColor":"#999999","userClientShow":"<a href='http://app.jd.com/android.html' target='_blank'>来自京东Android客户端</a>","isMobile":true},"mergeOrderStatus":2,"discussionId":71976319,"productColor":"玫瑰红","productSize":"","imageCount":3,"integral":-20,"anonymousFlag":1,"userLevelName":"金牌会员","recommend":false,"userLevelColor":"#088000","userClientShow":"<a href='http://app.jd.com/android.html' target='_blank'>来自京东Android客户端</a>","isMobile":true,"days":2},{"id":1314670814,"guid":"79384378-fc2e-4052-9268-bf04cf54644d","content":"手机外型可以，不过一拿回来冲电USB线插不稳松动联系卖家也不回复，这是卖出就不管了吗？","creationTime":"2016-02-02 13:14:22","isTop":false,"referenceId":"1548519300","referenceImage":"jfs/t1258/329/796926091/232621/2a614876/55546649N75fb7745.jpg","referenceName":"爱贝多Q5B 儿童手机 移动联通 定位低辐射 迷你可爱卡通孩子男生女生 幼儿园小学生电话 太空蓝","referenceTime":"2016-01-30 14:21:30","referenceType":"Product","referenceTypeId":0,"firstCategory":9987,"secondCategory":653,"thirdCategory":655,"replyCount":0,"score":1,"status":1,"usefulVoteCount":0,"uselessVoteCount":0,"userImage":"misc.360buyimg.com/lib/img/u/b56.gif","userImageUrl":"misc.360buyimg.com/lib/img/u/b56.gif","userLevelId":"56","userProvince":"","userRegisterTime":"2014-12-03 12:48:42","viewCount":0,"orderId":0,"isReplyGrade":false,"nickname":"sLiwFFZcAiYW","userClient":21,"productColor":"玫瑰红","productSize":"","integral":-20,"anonymousFlag":0,"userLevelName":"铜牌会员","recommend":false,"userClientShow":"<a href='javascript:;'>来自微信购物</a>","isMobile":false,"days":3},{"id":1309196588,"guid":"868421b7-b6ec-4d77-bea0-61a9800c4895","content":"手机不错的，待机达到一个星期左右，女儿很喜欢","creationTime":"2016-01-30 20:25:31","isTop":false,"referenceId":"1548519300","referenceImage":"jfs/t1258/329/796926091/232621/2a614876/55546649N75fb7745.jpg","referenceName":"爱贝多Q5B 儿童手机 移动联通 定位低辐射 迷你可爱卡通孩子男生女生 幼儿园小学生电话 太空蓝","referenceTime":"2016-01-22 21:38:46","referenceType":"Product","referenceTypeId":0,"firstCategory":9987,"secondCategory":653,"thirdCategory":655,"replyCount":0,"score":5,"status":1,"usefulVoteCount":0,"uselessVoteCount":0,"userImage":"misc.360buyimg.com/lib/img/u/b105.gif","userImageUrl":"misc.360buyimg.com/lib/img/u/b105.gif","userLevelId":"105","userProvince":"江苏","userRegisterTime":"2012-09-17 15:03:59","viewCount":0,"orderId":0,"isReplyGrade":false,"nickname":"h***哥","userClient":2,"images":[{"id":118675574,"associateId":71503110,"productId":0,"imgUrl":"http://img30.360buyimg.com/shaidan/s128x96_jfs/t1915/356/1471851858/129463/473987de/56acabbbN993fb682.jpg","available":1,"pin":"","dealt":0,"imgTitle":"","isMain":0},{"id":118675575,"associateId":71503110,"productId":0,"imgUrl":"http://img30.360buyimg.com/shaidan/s128x96_jfs/t2017/187/2191543028/134324/e3b2878f/56acabbbN16f0d536.jpg","available":1,"pin":"","dealt":0,"imgTitle":"","isMain":0}],"showOrderComment":{"id":71503110,"guid":"93ea5875-ddcc-4e1f-a9bb-c29c2bc2fd50","content":"手机不错的，待机达到一个星期左右，女儿很喜欢<div class='uploadimgdiv'><img class='uploadimg' border='0'  src='http://img30.360buyimg.com/shaidan/jfs/t1915/356/1471851858/129463/473987de/56acabbbN993fb682.jpg' /></div><div class='uploadimgdiv'><img class='uploadimg' border='0'  src='http://img30.360buyimg.com/shaidan/jfs/t2017/187/2191543028/134324/e3b2878f/56acabbbN16f0d536.jpg' /></div>","creationTime":"2016-01-30 20:25:31","isTop":false,"referenceId":"1548519300","referenceType":"Order","referenceTypeId":0,"firstCategory":0,"secondCategory":0,"thirdCategory":0,"replyCount":0,"score":0,"status":1,"usefulVoteCount":0,"uselessVoteCount":0,"userProvince":"","viewCount":0,"orderId":0,"isReplyGrade":false,"userClient":2,"isDeal":1,"integral":-20,"recommend":false,"userLevelColor":"#999999","userClientShow":"<a href='http://app.jd.com/iphone.html' target='_blank'>来自京东iPhone客户端</a>","isMobile":true},"mergeOrderStatus":2,"discussionId":71503110,"productColor":"玫瑰红","productSize":"","imageCount":2,"integral":-20,"anonymousFlag":1,"userLevelName":"钻石会员","recommend":false,"userLevelColor":"#ff0000","userClientShow":"<a href='http://app.jd.com/iphone.html' target='_blank'>来自京东iPhone客户端</a>","isMobile":true,"days":8},{"id":1308437258,"guid":"ef3cbf41-b79b-4452-8742-81dcbdfeef73","content":"好看，宝宝很喜欢，萌萌哒","creationTime":"2016-01-30 14:33:57","isTop":false,"referenceId":"1548519300","referenceImage":"jfs/t1258/329/796926091/232621/2a614876/55546649N75fb7745.jpg","referenceName":"爱贝多Q5B 儿童手机 移动联通 定位低辐射 迷你可爱卡通孩子男生女生 幼儿园小学生电话 太空蓝","referenceTime":"2015-11-16 17:46:07","referenceType":"Product","referenceTypeId":0,"firstCategory":9987,"secondCategory":653,"thirdCategory":655,"replyCount":0,"score":5,"status":1,"usefulVoteCount":0,"uselessVoteCount":0,"userImage":"misc.360buyimg.com/lib/img/u/b61.gif","userImageUrl":"misc.360buyimg.com/lib/img/u/b61.gif","userLevelId":"61","userProvince":"四川","userRegisterTime":"2013-02-23 00:33:48","viewCount":0,"orderId":0,"isReplyGrade":false,"nickname":"紫***n","userClient":4,"productColor":"玫瑰红","productSize":"","integral":-20,"anonymousFlag":1,"userLevelName":"银牌会员","recommend":false,"userClientShow":"<a href='http://app.jd.com/android.html' target='_blank'>来自京东Android客户端</a>","isMobile":true,"days":76},{"id":1302491095,"guid":"4a436128-1184-43b6-b26d-3fb47b8f9d81","content":"比较满意的一次网购，客服态度真不错","creationTime":"2016-01-27 21:49:20","isTop":false,"referenceId":"1548519300","referenceImage":"jfs/t1258/329/796926091/232621/2a614876/55546649N75fb7745.jpg","referenceName":"爱贝多Q5B 儿童手机 移动联通 定位低辐射 迷你可爱卡通孩子男生女生 幼儿园小学生电话 太空蓝","referenceTime":"2015-11-24 21:15:16","referenceType":"Product","referenceTypeId":0,"firstCategory":9987,"secondCategory":653,"thirdCategory":655,"replyCount":0,"score":5,"status":1,"usefulVoteCount":0,"uselessVoteCount":0,"userImage":"misc.360buyimg.com/lib/img/u/b61.gif","userImageUrl":"misc.360buyimg.com/lib/img/u/b61.gif","userLevelId":"61","userProvince":"","userRegisterTime":"2015-01-06 23:29:53","viewCount":0,"orderId":0,"isReplyGrade":false,"nickname":"jd_幸福的味道","userClient":2,"productColor":"玫瑰红","productSize":"","integral":-20,"anonymousFlag":0,"userLevelName":"银牌会员","recommend":false,"userClientShow":"<a href='http://app.jd.com/iphone.html' target='_blank'>来自京东iPhone客户端</a>","isMobile":true,"days":65},{"id":1302004675,"guid":"8f7b1837-4406-484c-bfa8-1ab7428bf352","content":"非常满意，很适合孩子用。","creationTime":"2016-01-27 18:28:02","isTop":false,"referenceId":"1548519301","referenceImage":"jfs/t1258/329/796926091/232621/2a614876/55546649N75fb7745.jpg","referenceName":"爱贝多Q5B 儿童手机 移动联通 定位低辐射 迷你可爱卡通孩子男生女生 幼儿园小学生电话 太空蓝","referenceTime":"2016-01-21 15:53:03","referenceType":"Product","referenceTypeId":0,"firstCategory":9987,"secondCategory":653,"thirdCategory":655,"replyCount":0,"score":5,"status":1,"usefulVoteCount":0,"uselessVoteCount":0,"userImage":"storage.360buyimg.com/i.imageUpload/7a6a79313530373334303531303831333839373631333434363636_sma.jpg","userImageUrl":"storage.360buyimg.com/i.imageUpload/7a6a79313530373334303531303831333839373631333434363636_sma.jpg","userLevelId":"62","userProvince":"湖南","userRegisterTime":"2012-06-23 20:52:59","viewCount":0,"orderId":0,"isReplyGrade":false,"nickname":"z***8","userClient":4,"productColor":"太空蓝","productSize":"","integral":-20,"anonymousFlag":1,"userLevelName":"金牌会员","recommend":false,"userLevelColor":"#088000","userClientShow":"<a href='http://app.jd.com/android.html' target='_blank'>来自京东Android客户端</a>","isMobile":true,"days":6},{"id":1294753941,"guid":"35acb44b-4a70-4541-8bae-8463757ef415","content":"非常好，可以打电话、定位等。声音清楚，充电一会儿就充满了，服务太度好，物流快，总体不错！！","creationTime":"2016-01-24 19:09:05","isTop":false,"referenceId":"1548519300","referenceImage":"jfs/t1258/329/796926091/232621/2a614876/55546649N75fb7745.jpg","referenceName":"爱贝多Q5B 儿童手机 移动联通 定位低辐射 迷你可爱卡通孩子男生女生 幼儿园小学生电话 太空蓝","referenceTime":"2016-01-22 09:41:42","referenceType":"Product","referenceTypeId":0,"firstCategory":9987,"secondCategory":653,"thirdCategory":655,"replyCount":0,"score":5,"status":1,"usefulVoteCount":0,"uselessVoteCount":0,"userImage":"misc.360buyimg.com/lib/img/u/b61.gif","userImageUrl":"misc.360buyimg.com/lib/img/u/b61.gif","userLevelId":"61","userProvince":"江苏","userRegisterTime":"2013-07-29 17:15:21","viewCount":0,"orderId":0,"isReplyGrade":false,"nickname":"jd138140elz","userClient":21,"images":[{"id":117030583,"associateId":70477714,"productId":0,"imgUrl":"http://img30.360buyimg.com/shaidan/s128x96_jfs/t2371/293/2075593350/43292/317f9be2/56a4b0d1Nadc37e75.jpg","available":1,"pin":"","dealt":0,"imgTitle":"","isMain":0},{"id":117030584,"associateId":70477714,"productId":0,"imgUrl":"http://img30.360buyimg.com/shaidan/s128x96_jfs/t2464/361/2063524784/35049/d6325df3/56a4b0d1Nad95ad49.jpg","available":1,"pin":"","dealt":0,"imgTitle":"","isMain":0},{"id":117030585,"associateId":70477714,"productId":0,"imgUrl":"http://img30.360buyimg.com/shaidan/s128x96_jfs/t1846/352/2136846848/34420/41968375/56a4b0d1Nd36c2868.jpg","available":1,"pin":"","dealt":0,"imgTitle":"","isMain":0}],"showOrderComment":{"id":70477714,"guid":"42236553-f36d-4388-a690-3393f7caaea4","content":"非常好，可以打电话、定位等。声音清楚，充电一会儿就充满了，服务太度好，物流快，总体不错！！<div class='uploadimgdiv'><img class='uploadimg' border='0'  src='http://img30.360buyimg.com/shaidan/jfs/t2371/293/2075593350/43292/317f9be2/56a4b0d1Nadc37e75.jpg' /></div><div class='uploadimgdiv'><img class='uploadimg' border='0'  src='http://img30.360buyimg.com/shaidan/jfs/t2464/361/2063524784/35049/d6325df3/56a4b0d1Nad95ad49.jpg' /></div><div class='uploadimgdiv'><img class='uploadimg' border='0'  src='http://img30.360buyimg.com/shaidan/jfs/t1846/352/2136846848/34420/41968375/56a4b0d1Nd36c2868.jpg' /></div>","creationTime":"2016-01-24 19:09:05","isTop":false,"referenceId":"1548519300","referenceType":"Order","referenceTypeId":0,"firstCategory":0,"secondCategory":0,"thirdCategory":0,"replyCount":0,"score":0,"status":1,"usefulVoteCount":0,"uselessVoteCount":0,"userProvince":"","viewCount":0,"orderId":0,"isReplyGrade":false,"userClient":21,"isDeal":1,"integral":-20,"recommend":false,"userLevelColor":"#999999","userClientShow":"<a href='javascript:;'>来自微信购物</a>","isMobile":false},"mergeOrderStatus":2,"discussionId":70477714,"productColor":"玫瑰红","productSize":"","imageCount":3,"integral":-20,"anonymousFlag":0,"userLevelName":"银牌会员","recommend":false,"userClientShow":"<a href='javascript:;'>来自微信购物</a>","isMobile":false,"days":2},{"id":1280973674,"guid":"88af432e-987a-4046-9a18-d29b75be57b4","content":"价格实惠,非常好用!","creationTime":"2016-01-18 21:53:33","isTop":false,"referenceId":"1548519300","referenceImage":"jfs/t1258/329/796926091/232621/2a614876/55546649N75fb7745.jpg","referenceName":"爱贝多Q5B 儿童手机 移动联通 定位低辐射 迷你可爱卡通孩子男生女生 幼儿园小学生电话 太空蓝","referenceTime":"2016-01-06 22:56:48","referenceType":"Product","referenceTypeId":0,"firstCategory":9987,"secondCategory":653,"thirdCategory":655,"replies":[{"commentId":"1280973674","content":"感谢您的支持，使用中有任何需要 或 疑问 欢迎联系我们！客服电话：400-855-0698。","creationTime":"2016-01-21 15:56:13","creationTimeString":"2016-01-21 15:56:13","id":70035578,"guid":"a4600f4c-a9a7-42a6-8c50-841eb041a4f5","isDelete":false,"parentId":"0","pin":"爱贝多_u","userImage":"misc.360buyimg.com/lib/img/u/b50.gif","userLevelId":"50","userRegisterTime":"2015-05-05 12:01:52","userProvince":"","nickname":"爱贝多_u","userClient":98,"updateTime":"2016-01-21 15:56:20","venderShopInfo":{"id":133000,"appName":"http://aibeiduogm.jd.com","title":"爱贝多专卖店"},"userLevelName":"注册会员","userClientShow":"","isMobile":false}],"replyCount":1,"score":5,"status":1,"usefulVoteCount":0,"uselessVoteCount":0,"userImage":"misc.360buyimg.com/lib/img/u/b61.gif","userImageUrl":"misc.360buyimg.com/lib/img/u/b61.gif","userLevelId":"61","userProvince":"广东","userRegisterTime":"2012-11-18 13:46:49","viewCount":0,"orderId":0,"isReplyGrade":false,"nickname":"j***0","userClient":0,"commentTags":[{"id":889601,"name":"通话质量好","pin":"","status":0,"rid":15235,"productId":1548519300,"commentId":1280973674,"created":"2016-01-18 21:53:51","modified":"2016-01-18 21:53:51"},{"id":889602,"name":"待机时间长","pin":"","status":0,"rid":15221,"productId":1548519300,"commentId":1280973674,"created":"2016-01-18 21:53:51","modified":"2016-01-18 21:53:51"},{"id":889603,"name":"音质好","pin":"","status":0,"rid":15234,"productId":1548519300,"commentId":1280973674,"created":"2016-01-18 21:53:51","modified":"2016-01-18 21:53:51"},{"id":889604,"name":"外观漂亮","pin":"","status":0,"rid":15225,"productId":1548519300,"commentId":1280973674,"created":"2016-01-18 21:53:51","modified":"2016-01-18 21:53:51"},{"id":889605,"name":"功能齐全","pin":"","status":0,"rid":15231,"productId":1548519300,"commentId":1280973674,"created":"2016-01-18 21:53:51","modified":"2016-01-18 21:53:51"}],"productColor":"玫瑰红","productSize":"","integral":-20,"anonymousFlag":1,"userLevelName":"银牌会员","recommend":false,"userClientShow":"","isMobile":false,"days":12}],"topFiveCommentVos":[]}""",
#     'crawl_time': '2016-03-01 16:49:16'
# }

####################################################################################################
import pandas
import pymysql

connect_dict = {'host': '10.118.187.12', 'user': 'admin', 'passwd': 'admin', 'charset': 'utf8'}
conn = pymysql.connect(**connect_dict)
sql_2015 = "SELECT * FROM `elec_platform`.`tmall_baseinfo_weekly_2015` WHERE `week` in ('27','31','36','40','45','49');"
df_2015 = pandas.read_sql(sql=sql_2015, con=conn)
df_2015 = df_2015.drop_duplicates(['name', 'week'])
sql_2016 = "SELECT * FROM `elec_platform`.`tmall_baseinfo_weekly_2016` WHERE `week` in ('01','04','09');"
df_2016 = pandas.read_sql(sql=sql_2016, con=conn)
sql_com = "SELECT t.`name`,t.company_name,t.major_business,t.judgepage_href from elec_platform.yms_tmall_shopinfo_com_withoutjudge t"
df_com = pandas.read_sql(sql=sql_com, con=conn)
df1 = pandas.concat([df_2015, df_2016])
df_2015, df_2016 = None, None
df2 = df1.drop(['brand', 'href', 'judgepage_href', 'seller', 'product_link_1', 'product_link_2', 'product_link_3',
                'product_link_4'], axis=1)
df1 = None
w_d = {
    '27': 'Jun',
    '31': 'Jul',
    '36': 'Aug',
    '40': 'Sep',
    '45': 'Oct',
    '49': 'Nov',
    '01': 'Dec',
    '04': 'Jan',
    '09': 'Feb'
}
df2['month'] = df2['week'].apply(lambda x: w_d[x])
df3 = pandas.merge(left=df2, right=df_com, how='left', left_on='name', right_on='name')
df4 = df3.drop(['spider_time', 'week', 'judgepage_href'], axis=1)

industry_d = {
    u'手机': u'手机',
    u'服饰鞋包': u'服饰鞋包',
    u'食品/保健': u'食品保健',
    u'母婴': u'母婴护理',
    u'美容护理': u'美容日化',
    u'运动/户外': u'运动/户外',
    u'大家电': u'家电',
    u'家居用品': u'家居家纺',
    u'家装家饰': u'家居家纺',
    u'珠宝/配饰': u'珠宝/手表'
}
df4['industry'] = df4['major_business'].apply(lambda x: industry_d.get(x))

# df4.to_csv('D:/tmall_1.csv',index=False)

express_count = {
    'Jan': 144570.4,
    'Feb': 81779.5,
    'Mar': 142537.8,
    'Apr': 151483.9,
    'May': 161002.5,
    'Jun': 164486.7,
    'Jul': 163988.3,
    'Aug': 169020.3,
    'Sep': 191336.9,
    'Oct': 194064.8,
    'Nov': 260537.8,
    'Dec': 241828.0
}

####################################################################################################
import requests as req
from pyquery.pyquery import PyQuery as pq

url_base = 'http://www.stylemode.com/fashion/fashionideas/'
res = req.get(url_base).text
d = pq(res)
url_pool = set()
url_pool.add(url_base)


# page_turning
def page_turn(res):
    d = pq(res)
    for item in d('.pager.text-center.clearfix>a').items():
        url_pool.add(item.attr('href'))


url_had_crawled = set()


# page crawling
def page_crawl():
    while len(url_had_crawled) < len(url_pool):
        url = url_pool.difference(url_had_crawled).pop()
        res = req.get(url).text
        page_turn(res)
        print page_parse(res)
        url_had_crawled.add(url)


def page_parse(res):
    d = pq(res)
    fw = d('.clearfix.list-unstyled.list-content>li').items()
    return [
        {
            'title': t('img').attr('alt'),
            'src_image_href': t('img').attr('src'),
            'page_href': t('img-wrap').prev.attr('href'),
            'view_count': t('.icon:nth-child(1)').next.text(),
            'like_count': t('.icon:nth-child(2)').next.text(),
            'time': t('.option time').text()
        }
        for t in fw
        ]


page_crawl()

####################################################################################################
import requests as req
import urllib
import json
import pymysql

connect_dict = {'host': '10.118.187.12', 'user': 'admin', 'passwd': 'admin', 'charset': 'utf8'}
conn = pymysql.connect(**connect_dict)
url_t = "http://search.jd.com/shop_new.php?ids=1000001925,169299,158027,148106,133802,126538,123424,83737,80218,38059"
referer = 'http://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&wq=%E6%89%8B%E6%9C%BA&pvid=oqp82dli.ohg2b2'
res = req.get(url_t, headers={'Referer': referer})
ref_quote = urllib.unquote(referer)

sql = """SELECT t.category FROM platform_data.`jd_base` t;"""
sql_detail = """SELECT t.detail FROM platform_data.`jd_base` t;"""
fw = pandas.read_sql(sql=sql, con=conn)
fw_detail = pandas.read_sql(sql=sql_detail, con=conn)

json_file =
j_f = json.loads(json_file)
j_f['crawl_url'] = {}
shop_id = [item[1].get('shopid') for item in j_f.items()]
shop_id = set(filter(lambda x: 1 if not x == '0' else 0, filter(lambda x: 1 if x else 0, shop_id)))

####################################################################################################
url = 'http://meanwhileclothing.en.alibaba.com/contactinfo.html'
_cookie = 'ali_apache_id=220.152.150.99.1433075894474.773074.1; xman_us_f=x_l=1&x_locale=zh_CN&no_popup_today=n&' \
          'x_user=CN|ms|yang|cnfm|227830436&last_popup_time=1457712623553; xman_f=IisD7O+QtSHDaZw7Ro4eZrboy8ZoT3YH' \
          '5qBALupxuPPdhCfEPfiZuS0rL4FX7cpwIMopUXSj21PfVbpV7A9cxgY6PAnxGrJRZzb/GRClvq+p43XuioIX6eV1FtSJh+oNldA1vro' \
          'bSSRF8XHfpnoQ1psOAq0y7wfNUxjpICfbeS8pnjDtA5rBuSplRf7FPhilgrWxs/30SUnxA7PN3PPm8o/kZhzAIlZ7m3MTpPfaaCY7CN' \
          'iaRJE+45DJY6+upuaCWEAS2ED0LzlaPYRh8+2EF8RTogxUL3tJz2AHgPFFFQQdQ2ZbNHybyNL034NAKvCAzBUETWBiM6XPsCDFDHyA3' \
          'SDNpSLCkjbNMIGG6HVcG3RDbEXdb6Yyiy8RJ1sXBpjoOpMNGuUZ7qubAyTpTSHoEQ==; ali_beacon_id=220.152.150.99.14330' \
          '75894474.773074.1; cna=PDviDaz2VHICAdyYlirqiemC; ali_ab=220.152.150.99.1433075902695.2; gangesweb-bucke' \
          'ttest=14.103.20.154.1439482574780.0; cn_8915ac475b2e7q858f6f_dplus=%7B%22distinct_id%22%3A%20%2214f27d8' \
          '214c47-041b52e392137b8-4b594136-144000-14f27d8214d5d5%22%2C%22%24initial_time%22%3A%201439453719%2C%22%' \
          '24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%' \
          '22%24recent_outside_referrer%22%3A%20%22%24direct%22%7D; cn_session_id_8915ac475b2e7q858f6f=1439482519;' \
          ' l=AuvrvIr7l1sfL5ftX7thOJzpWwHVfP-C; acs_usuc_t=acs_rt=04adc570449b4500b45667b927f76911; ' \
          'xman_t=Aq2yaxoSDiVc2VFqR3p07WwMhTH3R/Xw0/QR6SMYu1hRXwb8y50kM5HZD3f8iXHjgwNKh2to/EKLlyWLtrXebwoy8P7Ygi0k' \
          '6RPnghqKnlC/JJrr80No0G59Pdc3lpV+73dXKsKIxjV72GprFDthgKiCEqZULzCYmBx+umutjlYGRChR0RfvHFRxJrmftp3UtAfI5Dy' \
          'NMMU+9Lb6fyexuo32t1veMVr0C7WRm+jXVwyavxVVaCoCWh2IAFGOcLetCqn0Tnz6A/7a873dTWbuegXUAf1ibP1C88lwGZHhgko/9H' \
          'q3jc3wWGvi44asXeiHj424PkBKZzjYEqFIAaGT0823HiwyTUkrpHk9mT7S9aKhnvA6ZuTH60t+EEMqj1MB7TnTqV+k/w37E5Z4dvmm6' \
          'mMzM70hiTJVQwjDTyVsKVoLtdLpL3mTvRyZrWy9g1ID5cLXurJqpqds++ZuaaM7x6NdfjELr3RbpXvl+B95Qc691gbdoHYgNg79jIsG' \
          'OZhUqngMimuzR4Ug7x2nBpE44clwx/fSNC8a14Kyg/v8mzEiTyWdMpgdCv9EIPes/3VJZptxox6Les/rDwYHwtzpk6GEQ0ez0AJIfD/' \
          'dTcjx3uyMZbY7+G154bUqEehqiEIfQZON6mkfVBNKxtFK2hbMXUHcclK8kMNWVtRxicOujTkMEWUYGAHyUMq9i1tZIHlK4DHZv2bKxb' \
          't91EGQK1lvVGQvsGvY4Asu; acs_rt=fb98f4ae26004875baf0f3450f12210f; ali_apache_track="mt=2|ms=|mid=cn151778' \
          '3167fxcg"; ali_apache_tracktmp="W_signed=Y";_umdata' \
       '=8D5462A7710B16F8D1DE8DF86205FD525C80C1F3E9ED159353D27A988B78E33A95124095E980AB8DBA1A2351A9C8C74E01C0BCDCAB3FBFC' \
          '411759B14F9CEB2B359DABA6FBF2624AE5AFF9C0F6889F2732095993F18FE7B52D18529826EC23E36EEA6B27956624A9D;' \
          ' xman_us_t=sign=y&x_lid=cn1517783167fxcg&x_user=snjfbkxR3NkcVQQGvr9LO/fN4xN032k/8g7FATOGjaI=&ctoken=' \
          '4ga5m1191nr7&need_popup=n; intl_locale=zh_CN; intl_common_forever=mSNCHwz4DlNY7Rx/fF379Ghsha//BhsRueoX8' \
          '0dg9FGNg4ko5BMPLQ=='
cookie = dict(map(lambda x: (x.split('=', 1)[0], x.split('=', 1)[1]), _cookie.split(';')))
from requests import Session, Request
r = Session()
url='http://brictec.en.alibaba.com/contactinfo.html'
_prep = Request(method='GET', url=url, cookies=cookie)
prep = r.prepare_request(_prep)
rsu_1 = r.send(prep)
print rsu_1.content


####################################################################################################
from ms_spider_fw.DBSerivce import DBService
connect_dict = {'host': '118.193.220.134', 'user': 'root', 'passwd': '', 'charset': 'utf8'}
dbs = DBService(dbName='aliexpress', tableName='store_name', **connect_dict)
data=dbs.getData(var='store_name',distinct=True)

import re
pat=re.compile("<dt>(.+?)</dt>.+?>(.+?)</dd>",re.DOTALL)