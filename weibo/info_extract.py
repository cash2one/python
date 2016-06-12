from ms_spider_fw.DBSerivce import DBService
import json
from ms_spider_fw.CSVService import CSV

db_server = DBService(dbName='test', tableName='weibo_cellphone')  # , **connect_dict)
data = db_server.getData(var='detail_json')
data = filter(lambda x: 1 if x[0][0] == '{' else 0, filter(lambda x: 1 if x[0] else 0, data))


# extract_info from json string
def extract_info(x):
    try:
        d_t = json.loads(x[0])
        brand = d_t.get('sf_brand')
        industry = d_t.get('sf_industry')
        d = d_t['statuses']
        return [
            [
                it.get('created_at'),
                it.get('mid'),
                it.get('text'),
                it.get('source'),
                it.get('original_pic'),
                it.get('reposts_count'),
                it.get('comments_count'),
                it.get('goods_count'),
                it.get('forward'),
                it.get('user').get('id'),
                it.get('user').get('screen_name'),
                # it.get('user').get('profile_image_url'),
                it.get('user').get('gender'),
                it.get('user').get('verified'),
                it.get('user').get('profile_url'),
                it.get('user').get('followers_count'),
                it.get('user').get('friends_count'),
                it.get('user').get('statuses_count'),
                it.get('user').get('favourites_count'),
                it.get('user').get('url'),
                it.get('user').get('created_at'),
                it.get('user').get('url'),
                it.get('user').get('province'),
                it.get('user').get('city'),
                it.get('user').get('description'),
                '',  # weibo_type
                '',  # weibo_type1
                1,  # is_effect
                -1,  # is_neg
                brand,
                industry
            ]
            for it in d
            ]
    except:
        return []


data = reduce(lambda x, y: x + y, map(extract_info, data))
title = 'created_at,mid,text,source,original_pic,reposts_count,comments_count,' \
        'goods_count,forward,user_id,nickname,gender,verified,user_url,' \
        'followers_count,friends_count,statuses_count,favourites_count,' \
        'blog,register_date,url,province,city,description,weibo_type,' \
        'weibo_type1,is_effect,is_neg,brand,industry'.split(',')

CSV().writeCsv(savePath='d:', fileTitle=title, data=data, fileName='weibo_info_extract.csv')
