# -*- encoding: utf-8 -*-

from weibo_base_framework import *
from ms_spider_fw.DBSerivce import DBService
from datetime import *
# import time
from Queue import Queue
from data_transmit.weibo import transmit
import threading
import json

# config text
##################################################
# 行业配置，对应搜索关键词“文件名称”
industry = u'手机'
# 结束时间
_end = date.today().__str__()
# 需返回多长时间的数据
_before_days = 1
# 数据表名称
table_name = 'weibo_cellphone'
##################################################

queue_transmit = Queue(0)

db_name = 'test'
table_title = 'detail_json,crawl_time'
headers = {'User-Agent': 'User-Agent:Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) '
                         'Gecko/20100101 Firefox/4.0.1'}
db_server = DBService(dbName=db_name, tableName=table_name)

if not db_server.isTableExist():
    db_server.createTable(tableTitle=table_title.split(','))

end_day = datetime.strptime(_end, '%Y-%m-%d')
# start_day=end_day-timedelta(days=days)
_end_time = map(lambda x: x.strftime('%Y-%m-%d'),
                map(lambda x: end_day - timedelta(days=x), range(0, _before_days)))
_start_time = map(lambda x: x.strftime('%Y-%m-%d'),
                  map(lambda x: end_day - timedelta(days=x), range(1, _before_days + 1)))
_start_time.reverse()
_end_time.reverse()
time_step = zip(_start_time, _end_time)

t_k = target_keyword(industry)


def download_data():
    for item in time_step:
        start, end = item
        for k_w in t_k:
            try:
                api = weibo_api(start_time=start, end_time=end, key_word=k_w[0] + ' ' + industry)
                response = requests.get(url=api, headers=headers)
                page_total = json.loads(response.content).get('total_number')

                if not page_total:
                    continue

                _data = add_info(response.content, industry, k_w[1])
                queue_transmit.put(_data)
                # db_server.data2DB(data=[_data, time.strftime('%Y-%m-%d %X', time.localtime())])


                for i in range(2, 101 if page_total / 10 > 101 else page_total / 10):
                    try:
                        api_t = weibo_api(start_time=start, end_time=end, page=i, key_word=k_w[0] + ' ' + industry)
                        response_t = requests.get(url=api_t, headers=headers)
                        _data = add_info(response_t.content, industry, k_w[1])
                        queue_transmit.put(_data)
                        # db_server.data2DB(data=[_data, time.strftime('%Y-%m-%d %X', time.localtime())])
                    except Exception, e:
                        print e.message
                        continue
            except Exception, e:
                print e.message
                continue


def upload2ddt():
    while True:
        data = queue_transmit.get()
        _if_ok = transmit(data)
        print _if_ok
        if not _if_ok == 'ok':
            queue_transmit.put(data)
        if threading.activeCount() < 3:
            break


if __name__ == '__main__':
    T1 = threading.Thread(target=upload2ddt, name='Thread_upload')
    T2 = threading.Thread(target=download_data, name='Thread_download')
    T2.start()
    T1.start()
