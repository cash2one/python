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

from spiderFrame.DBSerivce import DBService
db=DBService(dbName='tmalldata',tableName='need_view')
text=db.getData(var='shopName')
text=map(lambda x:x[0],text)
for item in text:
    print(item)