from ms_spider_fw.DBSerivce import DBService
import json
from ms_spider_fw.CSVService import CSV
import re

# connect_dict = {
#     'host': 'localhost',
#     'user': 'root',
#     'passwd': '',
#     'charset': 'utf8'
# }

db_server = DBService(dbName='platform_data', tableName='jd_comment_woman_cloth')
data = db_server.getData(var='comment_json',limit=100000)#distinct=True, limit=10000)
data = filter(lambda x: 1 if x[0][0] == '{' else 0, filter(lambda x: 1 if x[0] else 0, data))

re_sub_p = re.compile('<.+?>')


# extract_info from json string
def extract_info(x):
    try:
        d_t = json.loads(x[0])
        d = d_t['comments']
        return [
            [
                it.get("id"),
                it.get("content").replace('\n',''),
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
                it.get("days")
            ]
            for it in d
            ]
    except:
        return []


data = reduce(lambda x, y: x + y, map(extract_info, data))
title = ["id", "content", "creationtime", "referencename", "referencetime", "referencetype", "replycount", "score",
         "status", "usefulvotecount", "uselessvotecount", "userlevelid", "userprovince", "userregistertime",
         "viewCount", "orderid", "isreplaygrade", "nickname", "userclient", "productcolor", "productsize", "integral",
         "anonymousflag", "userlevelname", "recommend", "userclientshow", "ismobile", "days"]

CSV().writeCsv(savePath='d:', fileTitle=title, data=data, fileName='jd_comment_info_extract.csv')
