#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on:2016/3/25 18:06
# Project:JD_analysis
# Author:yangmingsong

import pandas
import pandas as pd
import pymysql
import sys

reload(sys)
sys.setdefaultencoding('utf8')

connect_jd = pymysql.connect(
        host='10.118.187.12',
        user='admin',
        passwd='admin',
        database='platform_data',
        charset='utf8'
)

sql_get_data = 'SELECT * FROM `jd_data_temp_0326`;'
df_ori = pandas.read_sql(sql=sql_get_data, con=connect_jd)
# delete row if cate_0 is null
df_fir = df_ori[df_ori['cate_0'] != ""]
df_fir = df_fir[df_fir['cate_0'] != u'首页']  # 闪购
# df_fir = df_fir[df_fir.shop_name.isnull().apply(lambda x: False if x else True)]
df_fir = df_fir.drop(['id'], axis=1)
# df_fir.to_csv('/home/jd_df_fir_bak.csv', index=False)  # back file
# df_fir = pd.read_csv('/home/613108/jd_df_fir_bak.csv')
# saving the number of page count for each shop
df_page_count = df_fir.groupby("shop_name").shop_name.count()
df_page_count.to_csv("/home/613108/jd_each_shop_page_count.csv")
# saving the average sku_number of each_page
df_fir['size_count_float']=df_fir.size_count.astype(float)
df_sku_number_avg = df_fir.groupby("shop_name").size_count_float.sum() / df_fir.groupby("shop_name").shop_name.count()
df_sku_number_avg.to_csv("/home/613108/jd_each_shop_page_average_skunumber.csv")
# saving distinct shop
df_each_shop_info = df_fir.drop_duplicates(subset='shop_name', keep='last')
df_each_shop_info.to_csv("/home/613108/jd_each_shop_info.csv")
