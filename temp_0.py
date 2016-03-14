from ms_spider_fw.DBSerivce import DBService
import time

with open('D:/proxy_2.txt', 'r')as f:
    t = f.read()
proxy_list = t.split('\n')
proxy_list = [[item, time.strftime('%Y-%m-%d %X', time.localtime())] for item in proxy_list]
print len(proxy_list)

db_name = 'b2c_base'
connect_dict = {'host': '10.118.187.12', 'user': 'admin', 'passwd': 'admin', 'charset': 'utf8'}
db_server_c = DBService(dbName=db_name, tableName='proxy_other_source', **connect_dict)
db_server_c.createTable(tableTitle=['proxy_port', 'test_time'])
db_server_c.data2DB(data=proxy_list)
