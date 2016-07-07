#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import json
import re
from analysis import setiment
import sys
from datetime import datetime
import requests

reload(sys)
sys.setdefaultencoding('utf8')

table_title = [
    "id",
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
    res = list()
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
                    st = ('', 0, '', 0, 0)
                t = [
                    str(it.get('id')),
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
                    abs(if_ad - 1),  # is_effect
                    st[2],
                    st[3],
                    st[0],
                    st[1],
                    st[4],  # is_neg
                    brand,
                    industry
                ]
                res.append(t)
    except Exception, e:
        print e.message
    return res


def transmit(x):
    _data = map(lambda i: dict(zip(table_title, i)), extract_info(x))
    _post_data=json.dumps(_data)
    _post_url = 'http://dengta.sit.sf-express.com:6080/spider/saveSinaWeiboDetails'
    try:
        t = requests.post(url=_post_url, data={'authKey': 'ddt_spider_0321', 'json': _post_data})
        status=json.loads(t.content)
        return status.get('status')
    except ValueError,e:
        return e.message,' may be redirect to main_page.'
    except requests.ConnectionError,e:
        return e.message
