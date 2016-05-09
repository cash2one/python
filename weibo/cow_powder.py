# -*- encoding: utf-8 -*-
import time
import urllib
import sys
import requests
import json
from ms_spider_fw.DBSerivce import DBService

reload(sys)
sys.setdefaultencoding('utf8')

connect_dict = {
    'host': 'localhost',
    'user': 'root',
    'passwd': '',
    'charset': 'utf8'
}
db_name = 'base'
table_name = 'weibo_cow_powder'
table_title = 'detail_json,crawl_time'
db_server = DBService(dbName=db_name, tableName=table_name, **connect_dict)

if not db_server.isTableExist():
    db_server.createTable(tableTitle=table_title.split(','))

headers = {
    'User-Agent': 'User-Agent:Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) '
                  'Gecko/20100101 Firefox/4.0.1'}


def weibo_api(start_time, end_time, key_word=u"奶粉", page=1):
    def time_stamp(d, t='00:00:00'):
        # d = "2016-04-01 00:00:00"
        time_array = time.strptime(d + ' ' + t, "%Y-%m-%d %H:%M:%S")
        return int(time.mktime(time_array))

    url_base = 'https://c.api.weibo.com/2/search/statuses/limited.json?1846001573'
    parameters_base = {
        'access_token': '2.005ZdVSCv1dvAC698817991ct9WF5C',
        'q': '%E4%BA%AC%E4%B8%9C',
        'starttime': '1443607200',
        'endtime': '1443614400',
        'count': '50',
        'page': '1',
        'antispam': '0'
    }

    parameters_update = {
        'q': key_word,
        'starttime': time_stamp(start_time),
        'endtime': time_stamp(end_time),
        'page': str(page)
    }

    parameters_base.update(parameters_update)
    return url_base + urllib.urlencode(parameters_base)


if __name__ == '__main__':
    start = '2016-05-01'
    end = '2016-05-02'

    api = weibo_api(start_time=start, end_time=end)
    response = requests.get(url=api, headers=headers)
    page_total = json.loads(response.content).get('total_number')

    for i in range(1, 101 if page_total / 10 > 101 else page_total / 10):
        try:
            api_t = weibo_api(start_time=start, end_time=end, page=i)
            response_t = requests.get(url=api_t, headers=headers)
            db_server.data2DB(data=[response_t.content, time.strftime('%Y-%m-%d %X', time.localtime())])
            print 'is the ' + str(i) + ' request sucessful.'
        except Exception, e:
            print e.message
            continue
