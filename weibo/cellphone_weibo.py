# -*- encoding: utf-8 -*-
import time
import urllib
import sys
import requests
import json
from ms_spider_fw.DBSerivce import DBService
from pyquery.pyquery import PyQuery

reload(sys)
sys.setdefaultencoding('utf8')

db_name = 'test'
table_name = 'weibo_cellphone'
table_title = 'detail_json,crawl_time'
db_server = DBService(dbName=db_name, tableName=table_name)  # , **connect_dict)

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


def brand_list():
    res = requests.get('http://list.jd.com/list.html?cat=1319%2C1523%2C7052&go=0')
    d = PyQuery(res.content)
    return map(lambda a: a.text().split(u'（')[0], list(d.find('#brandsArea li a').items()))


def target_keyword(industry):
    with open('d:/spider/weibo/' + industry + '.txt', 'r')as f:
        keyword_tmp = f.read()
    keyword_s = map(lambda x: x.replace(u'）', '').split(u'（'), keyword_tmp.split('\n'))
    keyword_d = dict()
    for k_w in keyword_s:
        for kw in k_w:
            keyword_d[kw] = k_w[0]
    return keyword_d.items()


def add_info(base, industry, brand):
    t = json.loads(base)
    t['sf_industry'] = industry
    t['sf_brand'] = brand
    return json.dumps(t)


if __name__ == '__main__':
    start = '2016-06-10'
    end = '2016-06-11'
    industry = u'手机'

    t_k = target_keyword(industry)
    for k_w in t_k:
        try:print k_w[1]
        except:pass
        api = weibo_api(start_time=start, end_time=end, key_word=k_w[0] + ' ' + industry)
        response = requests.get(url=api, headers=headers)
        db_server.data2DB(data=[add_info(response.content, industry, k_w[1]),
                                time.strftime('%Y-%m-%d %X', time.localtime())])
        page_total = json.loads(response.content).get('total_number')

        if not page_total:
            continue

        for i in range(2, 101 if page_total / 10 > 101 else page_total / 10):
            try:
                api_t = weibo_api(start_time=start, end_time=end, page=i, key_word=k_w[0] + ' ' + industry)
                response_t = requests.get(url=api_t, headers=headers)
                db_server.data2DB(data=[add_info(response.content, industry, k_w[1]),
                                        time.strftime('%Y-%m-%d %X', time.localtime())])
                print 'is the ' + str(i) + ' request sucessful.'
            except Exception, e:
                print e.message
                continue
