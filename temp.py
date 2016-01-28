# coding:utf8
# __author__ = '613108'
# import pymysql
# connect=pymysql.connect(host='10.118.187.12',user='admin',password='admin',charset='utf8',database='elec_platform')

# import pandas as pd
# import numpy as np

# df=pd.DataFrame({'a':1,'b':1},index=[1,2])


# from sklearn import cluster,datasets
# k_means=cluster.KMeans(3)


# import jieba
# jieba.initialize()
# str='我操你妈逼的，狗日的真是日了狗了'
# str="""
# """
# seg_list=jieba.cut(str)
# print(' /'.join(seg_list))
# import jieba.analyse
# top_list=jieba.analyse.extract_tags(str)
# print(' '.join(top_list))


# with open('d:/spider/tmall/keyword.txt', 'r')as f:
#     temp = f.read()
# keyword = temp.split('++')
# keyword = map(lambda x: x.replace('双11', ""), keyword)
# keyword = list(set(keyword))
# for item in keyword:
#     print(item.decode('utf8', 'ignore'))

from ms_spider_fw.DBSerivce import DBService

db = DBService(dbName='tmalldata', tableName='need_view')
text = db.getData(var='shopName')
text = map(lambda x: x[0], text)
for item in text:
    print(item)

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

t = requests.get('http://www.amazon.cn/运动-户外-休闲/dp/B00OC4V7I4')
from pyquery.pyquery import PyQuery as pq

d = pq(t.text)
for item in d.my_text():
    if len(item) < 200:
        print item.decode('gbk', 'ignore')

from pyquery.pyquery import PyQuery as pq

with open('D:/temp1.html', 'r')as f:
    t = f.read()
d = pq(t)
f = open(u'儿童手表_brand.txt', 'w')
for x in d.find('.av-scroll>li>a').items():
    print x.attr('title').decode('gbk', 'ignore')
    f.write(x.attr('title') + ' ')
f.close()

from myTool import MyCsv

with open('d:/child_watch_brand.txt', 'r')as f:
    t = f.read()
t_1 = map(lambda x: x.split('/'), t.split(' '))
f_1 = []
for i_0 in t_1:
    for i_1 in i_0:
        f_1.append([i_1, i_0[0], u'儿童手表'])

with open('d:/intelligent_watch_brand.txt', 'r')as f:
    t = f.read()
t_2 = map(lambda x: x.split('/'), t.split(' '))
f_2 = []
for i_0 in t_2:
    for i_1 in i_0:
        f_2.append([i_1, i_0[0], u'智能手表'])

with open('d:/sweep_machine_brand.txt', 'r')as f:
    t = f.read()
t_3 = map(lambda x: x.split('/'), t.split(' '))
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


with open('D:\spider\tmall\2016-01-18\shopInfo_2016-01-18 19_11_25.csv','r')as f:
    t=f.readlines()

t=map(lambda x:x.split(','),t)
for item in t[:100]:
    print(item)

from ms_spider_fw.DBSerivce import DBService
dbs=DBService(dbName='b2c_base',tableName='proxy_xi_ci_dai_li')
t=dbs.getData(var='proxy_port',distinct=True)

# for jiuxian website_spider to extract info
pat=re.compile('_BFD\.BFD_INFO = \{(.+?)\};',re.DOTALL)