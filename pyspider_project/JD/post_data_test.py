#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from ms_spider_fw.DBSerivce import DBService
import json
import re
import requests
import sys

reload(sys)
sys.setdefaultencoding('utf8')

db_server = DBService(dbName='platform_data', tableName='jd_comment_woman_cloth')
data = db_server.getData(var='comment_json', distinct=True, limit=10)
data = filter(lambda x: 1 if x[0][0] == '{' else 0, filter(lambda x: 1 if x[0] else 0, data))

re_sub_p = re.compile('<.+?>')


# extract_info from json string
def extract_info(x):
    try:
        d_t = json.loads(x[0])
        d = d_t['comments']
        return [
            {
                "id": it.get("id"),
                "content": it.get("content").replace('\n', ''),
                "creationtime": it.get("creationTime"),
                "referencename": it.get("referenceName"),
                "referencetime": it.get("referenceTime"),
                "referencetype": it.get("referenceType"),
                "replycount": it.get("replyCount"),
                "score": it.get("score"),
                "status": it.get("status"),
                "usefulvotecount": it.get("usefulVoteCount"),
                "uselessvotecount": it.get("uselessVoteCount"),
                "userlevelid": it.get("userLevelId"),
                "userprovince": it.get("userProvince"),
                "userregistertime": it.get("userRegisterTime"),
                "viewCount": it.get("viewCount"),
                "orderid": it.get("orderId"),
                "isreplaygrade": it.get("isReplyGrade"),
                "nickname": it.get("nickname"),
                "userclient": it.get("userClient"),
                "productcolor": it.get("productColor"),
                "productsize": it.get("productSize"),
                "integral": it.get("integral"),
                "anonymousflag": it.get("anonymousFlag"),
                "userlevelname": it.get("userLevelName"),
                "recommend": it.get("recommend"),
                "userclientshow": re.sub(re_sub_p, '', it.get("userClientShow")),
                "ismobile": it.get("isMobile"),
                "days": it.get("days"),
                "industry":u'手机'
            }
            for it in d
            ]
    except:
        return []


def _post(data):
    url = 'http://dengta.sit.sf-express.com:6080/spider/saveJdCommentDetails'
    t = requests.post(url=url, data={'authKey': 'ddt_spider_0321', 'json': data})
    print t.status_code


if __name__ == '__main__':
    ok = reduce(lambda x, y: x + y, map(extract_info, data))
    post_data = json.dumps(ok)
    # print post_data
    _post(post_data)
