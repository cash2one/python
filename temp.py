from ms_spider_fw.DBSerivce import DBService
import json
from ms_spider_fw.CSVService import CSV
import re
import jieba
# connect_dict = {
#     'host': 'localhost',
#     'user': 'root',
#     'passwd': '',
#     'charset': 'utf8'
# }

db_server = DBService(dbName='platform_data', tableName='jd_comment_cellphone')
data = db_server.getData(var='comment_json',limit=10000)  # distinct=True, limit=10000)
data = filter(lambda x: 1 if x[0][0] == '{' else 0, filter(lambda x: 1 if x[0] else 0, data))

re_sub_p = re.compile('<.+?>')


# extract_info from json string
def extract_info(x):
    try:
        d_t = json.loads(x[0])
        d = d_t['comments']
        return [
            it.get("content").replace('\n', '')
            for it in d
            ]
    except:
        return []


data = reduce(lambda x, y: x + y, map(extract_info, data))
_result='\n'.join(data)
with open('d:/spider/weibo/handle/jd_comment.txt','w')as f:
    f.write(_result)