
from pyspider.libs.base_handler import *
from ms_spider_fw.DBSerivce import DBService
import re

# config_text
db_name = 'b2c_base'
table_name = 'proxy_you_dai_li'
table_title = 'proxy_port,crawl_time'
url_start = 'http://www.youdaili.net/Daili/'
connect_dict = {'host': '10.118.187.12', 'user': 'admin', 'passwd': 'admin', 'charset': 'utf8'}

# script
db_server = DBService(dbName=db_name, tableName=table_name, **connect_dict)
if not db_server.isTableExist():
    db_server.createTable(tableTitle=table_title.split(','))

patt_ip = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')

class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl(url_start, callback=self.step_first)

    @config(age=2 * 24 * 60 * 60)
    def step_first(self, response):
        d = response.doc
        for t in d('.newslist_listyle>a').items():
            self.crawl(t.attr.href, callback=self.step_second)

    @config(age=10 * 24 * 60 * 60)
    def step_second(self,response):
        d=response.doc
        # for t in d('.newslist_line>li>a').items():
        #     self.crawl(t.attr.href,callback=self.my_result)
        for t in d('.newslist_line>li>a').items():
            self.crawl(t.attr.href,callback=self.third)

    def step_third(self,response):
        d=response.doc
        txt=response.text
        proxy_port=re.findall(patt_ip,txt)
        print proxy_port



    # @config(priority=2)
    # def my_result(self, response):
    #     return []
    #
    # # over ride method for result store to mysql
    # def on_result(self, result):
    #     if result:
    #         db_server.data2DB(data=result)
    #     else:
    #         print u'result-->return None'
