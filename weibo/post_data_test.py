#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from ms_spider_fw.DBSerivce import DBService
import json
import re
import requests
import sys
from datetime import datetime

reload(sys)
sys.setdefaultencoding('utf8')

db_server = DBService(dbName='test', tableName='weibo_cellphone')  # , **connect_dict)
data = db_server.getData(var='detail_json', limit=20)
data = filter(lambda x: 1 if x[0][0] == '{' else 0, filter(lambda x: 1 if x[0] else 0, data))

re_sub_p = re.compile('<.+?>')
re_sub_t = re.compile('\+\d+?\s')


def time_format(ori):
    if not ori:
        return ''
    o = re.sub(re_sub_t, '', ori)
    s = datetime.strptime(o, '%a %b %d %H:%M:%S %Y')
    return s.strftime('%Y-%m-%d %H:%M:%S')


# extract_info from json string
def extract_info(x):
    try:
        d_t = json.loads(x[0])
        brand = d_t.get('sf_brand')
        industry = d_t.get('sf_industry')
        d = d_t['statuses']
        return [
            {
                "id": '1',
                "createdAt": time_format(it.get('created_at')),
                "mid": it.get('mid'),
                "text": it.get('text'),
                "source": re.sub(re_sub_p, '', it.get('source')),
                "originalPic": it.get('original_pic'),
                "repostsCount": it.get('reposts_count'),
                "commentsCount": it.get('comments_count'),
                "goodsCount": it.get('goods_count'),
                "forward": it.get('forward'),
                "userId": it.get('user').get('id'),
                "nickname": it.get('user').get('screen_name'),
                "gender": it.get('user').get('gender'),
                "verified": it.get('user').get('verified'),
                "userUrl": it.get('user').get('profile_url'),
                "followersCount": it.get('user').get('followers_count'),
                "friendsCount": it.get('user').get('friends_count'),
                "statusesCount": it.get('user').get('statuses_count'),
                "favouritesCount": it.get('user').get('favourites_count'),
                "blog": it.get('user').get('url'),
                "registerDate": time_format(it.get('user').get('created_at')),
                "url": it.get('user').get('url'),
                "province": it.get('user').get('province'),
                "city": it.get('user').get('city'),
                "description": it.get('user').get('description'),
                "weiboType": '',  # weibo_type
                "weiboType1": '',  # weibo_type1
                "isEffect": 1,  # is_effect
                "isNeg": -1,  # is_neg
                "brand": brand,
                "industry": industry
            }
            for it in d
            ]
    except:
        return []


def _post(data):
    # print (len(json.loads(data)))
    # print data
    url = 'http://dengta.sit.sf-express.com:6080/spider/saveSinaWeiboDetails'
    t = requests.post(url=url, data={'authKey': 'ddt_spider_0321', 'json': data})
    print t.content.encode('gbk', 'ignore')
    print t.status_code


if __name__ == '__main__':
    ok = reduce(lambda x, y: x + y, map(extract_info, data))
    post_data = json.dumps(ok)
    print post_data
    _post(post_data)
