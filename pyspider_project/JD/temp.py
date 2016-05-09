from ms_spider_fw.DBSerivce import DBService
import json
from ms_spider_fw.CSVService import CSV

connect_dict = {
    'host': 'localhost',
    'user': 'root',
    'passwd': '',
    'charset': 'utf8'
}

db_server = DBService(dbName='base', tableName='jd_comment_cow_powder', **connect_dict)
data = db_server.getData(var='comment_json', distinct=True)
data = filter(lambda x: 1 if x[0][0] == '{' else 0, filter(lambda x: 1 if x[0] else 0, data))


def extract_info(x):
    try:
        d_t = json.loads(x[0])
        d = d_t['comments']
        return [
            [
                it.get('id'),
                it.get('referenceId'),
                it.get('guid'),
                it.get('content'),
                it.get('creationTime'),
                it.get('referenceName'),
                it.get('referenceTime'),
                it.get('referenceType'),
                it.get('replyCount'),
                it.get('score'),
                it.get('status'),
                it.get('usefulVoteCount'),
                it.get('uselessVoteCount'),
                it.get('userLevelId'),
                it.get('userProvince'),
                it.get('userRegisterTime'),
                it.get('viewCount'),
                it.get('orderId'),
                it.get('isReplyGrade'),
                it.get('nickname'),
                it.get('userClient'),
                it.get('productColor'),
                it.get('productSize'),
                it.get('integral'),
                it.get('anonymousFlag'),
                it.get('userLevelName'),
                it.get('recommend'),
                it.get('userClientShow'),
                it.get('isMobile'),
                it.get('days')
            ]
            for it in d
            ]
    except:
        return []


data = reduce(lambda x, y: x + y, map(extract_info, data))
title = ['id', 'referenceId', 'guid', 'content', 'creationTime', 'referenceName', 'referenceTime', 'referenceType',
         'replyCount', 'score', 'status', 'usefulVoteCount', 'uselessVoteCount', 'userLevelId', 'userProvince',
         'userRegisterTime', 'viewCount', 'orderId', 'isReplyGrade', 'nickname', 'userClient', 'productColor',
         'productSize', 'integral', 'anonymousFlag', 'userLevelName', 'recommend', 'userClientShow', 'isMobile', 'days']

CSV().writeCsv(savePath='d:', fileTitle=title, data=data, fileName='jd_comment_info_extract.csv')
