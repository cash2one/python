# coding:utf-8
__author__ = '613108'

import pymysql
from Keyword import get_secondLevel_keyword

# 数据库链接
conn = pymysql.connect(host='localhost', user='root', passwd='', db='tmall_info', charset='utf8')
cursor = conn.cursor()
sql_select = "select keyword_detail from yms_tmall_firstkeyword"
cursor.execute(sql_select)
firstLevel_keyword = cursor.fetchall()
firstLevel_keyword = [x[0] for x in firstLevel_keyword]
for item in firstLevel_keyword:
    print item
# print(firstLevel_keyword_1)
secondLevel_keyword = get_secondLevel_keyword(firstLevel_keyword=firstLevel_keyword)

for item in secondLevel_keyword:
    sql_insert = 'insert into yms_tmall_secondkeyword (keyword_detail,staus) values(%s,%s)'
    cursor.execute(sql_insert, (item, 0))
    conn.commit()
conn.close()