from ms_spider_fw.DBSerivce import DBService
import json
from ms_spider_fw.CSVService import CSV

connect_dict = {
    'host': 'localhost',
    'user': 'root',
    'passwd': '',
    'charset': 'utf8'
}

db_server = DBService(dbName='base', tableName='weibo_cow_powder', **connect_dict)
data = db_server.getData(var='detail_json', distinct=True)
data = filter(lambda x: 1 if x[0][0] == '{' else 0, filter(lambda x: 1 if x[0] else 0, data))


# extract_info from json string
def extract_info(x):
    try:
        d_t = json.loads(x[0])
        d = d_t['statuses']
        return [
            [
                it.get('created_at'),
                it.get('text'),
                it.get('source'),
                it.get('user').get('screen_name'),
                it.get('user').get('name'),
                it.get('user').get('province'),
                it.get('user').get('city'),
                it.get('user').get('location'),
                it.get('user').get('description'),
                it.get('user').get('followers_count'),
                it.get('user').get('friends_count'),
                it.get('user').get('pagefriends_count'),
                it.get('user').get('statuses_count'),
                it.get('user').get('favourites_count'),
                it.get('user').get('created_at'),
                it.get('user').get('star'),
                it.get('user').get('level'),
                it.get('user').get('type'),
                it.get('user').get('ulevel'),
            ]
            for it in d
            ]
    except:
        return []



data = reduce(lambda x, y: x + y, map(extract_info, data))
title = 'weibo_create_at,text,source,screen_name,name,province,city,location,description,' \
        'followers_count,friends_count,pagefriends_count,statuses_count,favourites_count,' \
        'users_created_at,star,level,type,ulevel'.split(',')

CSV().writeCsv(savePath='d:', fileTitle=title, data=data, fileName='weibo_info_extract.csv')
