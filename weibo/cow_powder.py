# -*- encoding: utf-8 -*-
import time
import urllib
import sys
import requests
import json

reload(sys)
sys.setdefaultencoding('utf8')


def weibo_api(start_time, end_time, key_word=u"有机奶粉", page=1):
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

if __name__=='__main__':
    api=weibo_api(start_time='2016-04-01',end_time='2016-05-01')

    response = requests.get(api)


    print response.content

    page_total=json.loads(response.content).get('total_number')
    print page_total/10
