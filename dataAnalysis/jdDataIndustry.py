#coding:utf8
__author__ = '613108'
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from spiderFrame.DBSerivce import DBService
import pymysql


# db=DBService('jddata','thirdPartShopInfo')
# data=db.getData(var='productHref,companyName,shopName')
# title=db.getTableTitle()
# df=pd.DataFrame(data,columns=['productHref','companyName','shopName'])
# db2=DBService('jddata','jdproductbaseinfo2database')
# data2=db2.getData(var='productHref,pageUrl')
# df2=pd.DataFrame(data2,columns=['productHref','pageUrl'])
con=pymysql.connect(host='10.118.187.12', user='admin', passwd='admin', charset='utf8', db='jddata')
sql1='select distinct productHref,companyName,shopName from thirdPartShopInfo'
df1=pd.read_sql(sql=sql1,con=con)
sql2='select distinct productHref,pageUrl from jdproductbaseinfo2database'
df2=pd.read_sql(sql=sql2,con=con)
res=df1.merge(df2,left_on='productHref',right_on='productHref')
res.to_csv(path_or_buf='d:/spider/ok.csv',encoding='UTF8')
print(res)