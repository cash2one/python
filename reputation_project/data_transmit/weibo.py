#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from ms_spider_fw.DBSerivce import DBService
import json
import re
from analysis import setiment
import sys
from datetime import datetime

reload(sys)
sys.setdefaultencoding('utf8')

db_server = DBService(dbName='test', tableName='weibo_cellphone')  # , **connect_dict)
data = db_server.getData(var='detail_json', limit=20000)
data = reduce(lambda x, y: x + y,
              filter(lambda x: 1 if x[0][0] == '{' else 0, filter(lambda x: 1 if x[0] else 0, data)))

db_server = DBService(dbName='test', tableName="weibo_setiment_cellphone")
table_title = [  # "id",
    "createdAt",
    "mid",
    "text",
    "source",
    "originalPic",
    "repostsCount",
    "commentsCount",
    "goodsCount",
    "forward",
    "userId",
    "nickname",
    "gender",
    "verified",
    "userUrl",
    "followersCount",
    "friendsCount",
    "statusesCount",
    "favouritesCount",
    "blog",
    "registerDate",
    "url",
    "province",
    "city",
    "description",
    "weiboType",
    "weiboType1",
    "isEffect",
    "negWords",
    "negWordsNum",
    "goodWords",
    "goodsWordsNum",
    "isNeg",
    "brand",
    "industry"
]
if not db_server.isTableExist():
    db_server.createTable(tableTitle=table_title)

re_sub_p = re.compile('<.+?>')
re_sub_t = re.compile('\+\d+?\s')


def time_format(ori):
    """
    时间字段格式化，返回格式如 2016-06-24 12:15:10
    """
    if not ori:
        return ''
    o = re.sub(re_sub_t, '', ori)
    s = datetime.strptime(o, '%a %b %d %H:%M:%S %Y')
    return s.strftime('%Y-%m-%d %H:%M:%S')


def extract_info(x):
    try:
        d_t = json.loads(x)
        brand = d_t.get('sf_brand')
        industry = d_t.get('sf_industry')
        d = d_t['statuses']
        if d and isinstance(d, list):
            for it in d:
                text = it.get('text')
                if_ad = setiment.if_ad(text)
                st = setiment.checking_sentiment(text)
                if if_ad:
                    st = ('', '', '', '', '')
                t = [
                    # id,
                    time_format(it.get('created_at')),
                    it.get('mid'),
                    text,
                    re.sub(re_sub_p, '', it.get('source')),
                    it.get('original_pic'),
                    it.get('reposts_count'),
                    it.get('comments_count'),
                    it.get('goods_count'),
                    it.get('forward'),
                    it.get('user').get('id'),
                    it.get('user').get('screen_name'),
                    it.get('user').get('gender'),
                    it.get('user').get('verified'),
                    it.get('user').get('profile_url'),
                    it.get('user').get('followers_count'),
                    it.get('user').get('friends_count'),
                    it.get('user').get('statuses_count'),
                    it.get('user').get('favourites_count'),
                    it.get('user').get('url'),
                    time_format(it.get('user').get('created_at')),
                    it.get('user').get('url'),
                    it.get('user').get('province'),
                    it.get('user').get('city'),
                    it.get('user').get('description'),
                    '',  # weibo_type
                    '',  # weibo_type1
                    abs(if_ad-1),  # is_effect
                    st[2],
                    st[3],
                    st[0],
                    st[1],
                    st[4],  # is_neg
                    brand,
                    industry
                ]
                db_server.data2DB(data=t)
    except Exception, e:
        print e.message
    return None


if __name__ == "__main__":
    for item in data:
        extract_info(item)
