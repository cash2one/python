"""
# pyspider script sample
# for every website spider project , copy and paste , then change config_text and script
"""

from pyspider.libs.base_handler import *
from ms_spider_fw.DBSerivce import DBService

# config_text
# when start a spider,you should modify the next config text first

db_name = ''  # database name for store data , string
table_name = ''  # table name for store data , string
table_title = ''  # table title for store data , should be string separated by ','
url_start = ''  # start url for crawl,string
# connect string , usually no need to modify
connect_dict = {'host': '10.118.187.12', 'user': 'admin', 'passwd': 'admin', 'charset': 'utf8'}

# now,the next is spider script
db_server = DBService(dbName=db_name, tableName=table_name, **connect_dict)
# if create table for store result in mysql , no need to be changed
if not db_server.isTableExist():
    db_server.createTable(tableTitle=table_title.split(','))


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl(url_start, callback=self.step_first)

    @config(age=2 * 24 * 60 * 60)
    def step_first(self, response):
        d = response.doc
        for t in d('').items():
            self.crawl(t.attr.href, callback=self.my_result)

    @config(priority=2)
    def my_result(self, response):
        return []

    # over ride method for result store to mysql
    def on_result(self, result):
        if result:
            db_server.data2DB(data=result)
        else:
            print u'result-->return None'
