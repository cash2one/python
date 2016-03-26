#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on:2016/3/25 13:40
# Project:JD_parse
# Author:yangmingsong

import pandas
import pymysql
import json
from ms_spider_fw.DBSerivce import DBService
import threading
import Queue

json_file_queue = Queue.Queue(0)

connect_jd = pymysql.connect(
        host='10.118.187.12',
        user='admin',
        passwd='admin',
        database='platform_data'
)
connect_dict = {'host': '10.118.187.12', 'user': 'admin', 'passwd': 'admin', 'charset': 'utf8'}
dbs = DBService(dbName='platform_data', tableName='jd_data_temp_0326', **connect_dict)
dbs.createTable(
        tableTitle=
        map(lambda x: x.strip(),
            'shop_name, addr, com_name, shop_href, cate_0, score_summary, '
            'express_score, product_score, service_score,product_href, vender_id, '
            'sku_id, size_count'.split(','))
)


def get_min_max_id():
    sql_min = 'SELECT MIN(id) FROM jd_product_detail'
    sql_max = 'SELECT MAX(id) FROM jd_product_detail'
    cur = connect_jd.cursor()
    cur.execute(sql_min)
    min_id = cur.fetchall()
    cur.execute(sql_max)
    max_id = cur.fetchall()
    cur.close()
    return min_id[0][0], max_id[0][0]


def get_data_from_database(min_id, max_id):
    print min_id, max_id
    sql_data = "SELECT product_detail FROM `jd_product_detail` " \
               "where id BETWEEN %s AND %s;" % (min_id, max_id)
    print sql_data
    fw_data = pandas.read_sql(sql=sql_data, con=connect_jd)
    array_data = fw_data.values
    list_data = array_data.tolist()
    return map(lambda x: x[0], list_data)


def parse_json(json_file):
    shop_name, addr, com_name, shop_href, cate_0, score_summary, \
    express_score, product_score, service_score, product_href, vender_id, \
    sku_id, size_count = '', '', '', '', '', '', '', '', '', '', '', '', ''
    try:
        d = json.loads(json_file)
        d_shop = d.get('shop_com_information')
        d_cate = d.get('catagory')
        d_sore = d.get('score_detail')
        d_product = d.get('base_info').get('product')
        if d_shop:
            shop_name = d_shop.get('shop_name')
            addr = d_shop.get('addr')
            com_name = d_shop.get('com_name')
            shop_href = d_shop.get('shop_href')
        if d_cate:
            cate_0 = d_cate.get('category_0')
        if d_product:
            product_href = d_product.get('href')
            vender_id = d_product.get('venderId')
            sku_id = d_product.get('skuid')
            size_count = len(d_product.get('colorSize')) \
                if d_product.get('colorSize') else 1
        if d_sore:
            score_summary = d_sore.get('score_sum')
            express_score = d_sore.get(u'物流').get(
                'score')  # get("score") maybe wrong because Nonytype doesn't having "get" method
            product_score = d_sore.get(u'商品').get('score')
            service_score = d_sore.get(u'服务').get('score')
    except:
        pass
    return [
        shop_name, addr, com_name, shop_href, cate_0, score_summary,
        express_score, product_score, service_score, product_href, vender_id,
        sku_id, size_count
    ]


def json_decode(*args):
    min_id, max_id = args
    step = 100000
    small_id = min_id
    while small_id < max_id:
        big_id = max_id if small_id + step > max_id else small_id + step
        data = get_data_from_database(small_id, big_id - 1)
        json_file_queue.put(data)
        # decode_json = map(parse_json, data)
        # print decode_json[0]
        # dbs.data2DB(data=decode_json)
        small_id += step


def decode_json_file():
    while True:
        data = json_file_queue.get(timeout=500)
        decode_json = map(parse_json, data)
        print decode_json[0]
        dbs.data2DB(data=decode_json)


def main():
    min_id, max_id = get_min_max_id()
    thread_step = 10000000
    # thread_count, t = divmod(max_id, thread_step)[0]
    # thread_count = thread_count if t == 0 else thread_count + 1
    id_list = map(lambda x: (x, x + thread_step), range(min_id, max_id, thread_step))
    thread_pool = list()
    thread_pool.append(threading.Thread(target=decode_json_file))
    for id_tuple in id_list:
        # using pandas to read data from database can not using mutiple thread
        thread_pool.append(threading.Thread(target=json_decode, args=(id_tuple[0], id_tuple[1]), name='get_data'))
    for thread_son in thread_pool:
        thread_son.start()
        print thread_son.name
    for thread_son in thread_pool:
        thread_son.join()


if __name__ == '__main__':
    main()
