# encoding: utf-8
import time
import urllib
import requests
import json
from pyquery.pyquery import PyQuery
import sys

reload(sys)
sys.setdefaultencoding('utf8')


def weibo_api(start_time, end_time, key_word=u"cellphone", page=1):
    # API请求地址构造
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


def brand_list(url):
    # 利用京东地址返回品牌列表
    # 弃用，现用本地文件返回品牌列表
    res = requests.get(url)
    d = PyQuery(res.content)
    return map(lambda a: a.text().split(u'（')[0], list(d.find('#brandsArea li a').items()))


def target_keyword(industry):
    # 返回品牌列表
    # 返回 (Key:中文品牌/英文品牌,value：唯一品牌名称）列表
    with open('d:/spider/weibo/' + industry + '.txt', 'r')as f:
        keyword_tmp = f.read()
    keyword_s = map(lambda x: x.replace(u'）', '').split(u'（'), keyword_tmp.split('\n'))
    keyword_d = dict()

    for k_w in keyword_s:
        for kw in k_w:
            keyword_d[kw] = k_w[0]

    return keyword_d.items()


def add_info(base, industry, brand):
    # 添加行业及品牌信息
    t = json.loads(base)
    t['sf_industry'] = industry
    t['sf_brand'] = brand
    return json.dumps(t)
