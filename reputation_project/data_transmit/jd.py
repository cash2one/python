#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import json
import re
from analysis import setiment
from ms_spider_fw.DBSerivce import DBService
import sys

reload(sys)
sys.setdefaultencoding('utf8')

db_server = DBService(dbName='platform_data', tableName='jd_comment_cellphone')
data = db_server.getData(var='comment_json', distinct=True, limit=100000)
data = reduce(lambda x, y: x + y,
              filter(lambda x: 1 if x[0][0] == '{' else 0, filter(lambda x: 1 if x[0] else 0, data)))
db_server = DBService(dbName='test', tableName="jd_setiment_cellphone")
table_title = [
    # "id",
    "content",
    "creationtime",
    "referencename",
    "referencetime",
    "referencetype",
    "replycount",
    "score",
    "status",
    "usefulvotecount",
    "uselessvotecount",
    "userlevelid",
    "userprovince",
    "userregistertime",
    "viewCount",
    "orderid",
    "isreplaygrade",
    "nickname",
    "userclient",
    "productcolor",
    "productsize",
    "integral",
    "anonymousflag",
    "userlevelname",
    "recommend",
    "userclientshow",
    "ismobile",
    "negwords",
    "negwordsnum",
    "goodwords",
    "goodwordsnum",
    "days",
    "industry"
]
if not db_server.isTableExist():
    db_server.createTable(tableTitle=table_title)

# re_sub_p = re.compile('<.+?>')
re_sub_p = re.compile(u'回复|#.+?#|@.+?[\s:：]|\[.+?\]|@.+$|\s+?')

res = list()


def extract_info(x):
    try:
        d_t = json.loads(x)
        d = d_t['comments']
    except Exception, e:
        # raise ValueError('No comments exists!')
        return None
    if isinstance(d, list):
        for it in d:
            s = it.get("content").replace('\n', '')
            st = setiment.checking_sentiment(s)
            t = [#it.get("id"),
                 it.get("content").replace('\n', ''),
                 it.get("creationTime"),
                 it.get("referenceName"),
                 it.get("referenceTime"),
                 it.get("referenceType"),
                 it.get("replyCount"),
                 it.get("score"),
                 it.get("status"),
                 it.get("usefulVoteCount"),
                 it.get("uselessVoteCount"),
                 it.get("userLevelId"),
                 it.get("userProvince"),
                 it.get("userRegisterTime"),
                 it.get("viewCount"),
                 it.get("orderId"),
                 it.get("isReplyGrade"),
                 it.get("nickname"),
                 it.get("userClient"),
                 it.get("productColor"),
                 it.get("productSize"),
                 it.get("integral"),
                 it.get("anonymousFlag"),
                 it.get("userLevelName"),
                 it.get("recommend"),
                 re.sub(re_sub_p, '', it.get("userClientShow")),
                 it.get("isMobile"),
                 st[2],
                 st[3],
                 st[0],
                 st[1],
                 it.get("days"),
                 u'手机']
            res.append(t)
            try:
                db_server.data2DB(data=t)
            except Exception,e:
                print e.message


if __name__ == "__main__":
    for item in data:
        extract_info(item)