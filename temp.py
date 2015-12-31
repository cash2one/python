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
connect = pymysql.connect(host='10.118.187.12', user='admin', password='admin', charset='utf8',database='elec_platform')
import pandas as pd
sql_1 = "SELECT t.`name`,t.monthsale,t.addr,t.spider_time FROM `tmall_baseinfo_everyweek` t"
sql_2 = "SELECT t.`name`,t.major_business FROM `yms_tmall_shopinfo_com_withoutjudge` t"
df1=pd.read_sql(sql=sql_1,con=connect)
df1['date']=df1['spider_time'].apply(lambda x:x.split(' ')[0])
df2=pd.read_sql(sql=sql_2,con=connect)
df3=pd.merge(df1,df2,how='left',left_on='name',right_on='name')
df4=df3.drop('spider_time',axis=1)
temp=[u'手机',u'运动/户外']
df5=df4[df4['major_business'].isin(temp)]

# JD_Guangdongprovice
# create on:2015-12-25
import pymysql
connect = pymysql.connect(host='10.118.187.12', user='admin', password='admin', charset='utf8',database='jddata')
import pandas as pd
sql_1='SELECT * FROM `thirdPartShopInfo`;'
df1=pd.read_sql(sql=sql_1,con=connect)
df1=df1.drop(['productHref','id'],axis=1)
df1=df1.sort(columns=['shopName','gradeHref'])
df2=df1.drop_duplicates(['shopName'])
df2.to_csv(path_or_buf='/home/appdeploy/jd_all_shop.csv',index=False)