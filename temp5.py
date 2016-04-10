# from ms_spider_fw.DBSerivce import DBService
# from myTool.listSplit import listSplit
# import time
# import ms_proxy.proxy_test as pt
#
# connect_dict_proxy = {
#     'host': 'localhost',
#     'user': 'root',
#     'passwd': '',
#     'charset': 'utf8'
# }
# db_name_proxy = 'base'
# table_name_proxy = 'proxy_black_hat'
# dbs = DBService(dbName=db_name_proxy, tableName=table_name_proxy, **connect_dict_proxy)
# dbs.createTable(tableTitle=['proxy_port', 'crawld_time'], x='Y')
#
# with open('D:/proxy_black_hat.txt', 'r')as f:
#     t = f.read()
# proxy_list_t_0 = list(set(t.split('\n')))
# proxy_list_t_1 = filter(lambda x: 1 if x else 0, map(lambda x: x[1:-1], proxy_list_t_0))
# # proxy_list = map(lambda x: [x, time.strftime('%Y-%m-%d %X', time.localtime())], proxy_list_t_1)
#
# # dbs.data2DB(data=proxy_list)
# target_list = listSplit(proxy_list_t_1, 10)
# ok = list()
# for proxy_list in target_list:
#     ok += pt.test_from_list(proxy_list)
#     print ok
#
# for item in ok:
#     print item
#
# with open('D:/black_proxy.txt', 'wb')as f:
#     for proxy_port in ok:
#         f.write(proxy_port + '\n')

with open('d:/black_proxy.txt','r')as f:
    t=f.read()
print len(t.split('\n'))

with open('c:\aliexpress\contact_info_aliexpress_com.txt','r')as f:
    data_base=f.read()
data_fir_step = filter(lambda x: 1 if x else 0, data_base.split('\n'))
print 'Total record is %s' % len(data_fir_step)
data_sec_step = filter(lambda x: 1 if x.split('\t')[0] == '"888888"' else 0, data_fir_step)
print 'Total "888888" record is %s' % len(data_sec_step)
print data_sec_step[-1]
