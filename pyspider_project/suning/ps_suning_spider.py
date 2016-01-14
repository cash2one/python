from pyspider.libs.base_handler import *
from ms_spider_fw.DBSerivce import DBService
import sys
import time

reload(sys)
sys.setdefaultencoding('utf8')

# config_text
db_name = 'platform_data'  # database name for store data , string
table_name = 'suning'  # table name for store data , string
table_title = ''  # table title for store data , should be string separated by ','
url_start = 'http://www.suning.com/emall/pgv_10052_10051_1_.html'  # start url for crawl,string
connect_dict = {'host': '10.118.187.12', 'user': 'admin', 'passwd': 'admin', 'charset': 'utf8'}

# script
db_server = DBService(dbName=db_name, tableName=table_name, **connect_dict)


# if not db_server.isTableExist():
#     db_server.createTable(tableTitle=table_title.split(','))


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl(url_start, callback=self.step_first)

    @config(age=2 * 24 * 60 * 60)
    def step_first(self, response):
        d = response.doc
        for t in d('.listLeft>dl>dd>span>a').items():
            self.crawl(t.attr.href, callback=self.step_second)
        for x in d('.listRight>dl>dd>span>a').items():
            self.crawl(x.attr.href, callback=self.step_second)

    @config(age=2 * 24 * 60 * 60)
    def step_second(self, response):
        d = response.doc
        for t in d('.i-name .sellPoint').items():
            self.crawl(t.attr.href, callback=self.my_result, fetch_type='js',
                       js_script="""function(){windows.scrollTo(0,document.body.scrollHeight);}""")
        for x in d('.snPages a').items():
            if x.text().decode().isnumeric():
                self.crawl(x.attr.href, callback=self.step_second)

    @config(priority=2)
    def my_result(self, response):
        d = response.doc
        #TODO:something need to be fix
        rating_score = d('.clearfix>li .rating-val').text().split(' ')
        rating_icon = [t.attr('class') for t in d('.clearfix>li .si-icon').items()]  # for judge minus or other
        return [
            d('#category1').text(),  # main category
            d('.dropdown-text a').text(),  # sub category
            d('.proinfo-title>h1').text(),  # product title
            d('.proinfo-title>h2').text(),  # promotion describe
            d('#netPrice>del').text(),  # origin price
            d('#promotionPrice').text(),  # promotion price
            d('.stars+span').text(),  # product stars
            d('.totalReview').text(),  # comment count
            d('#shopName').text(),  # sending service
            '|'.join([t('a').text() for t in d('.proinfo-serv span').items() if t.attr('style') != 'display:none;']),
            # other service
            '|'.join([t.text() for t in d('.procon-param td').items() if t.attr('class') != 'err']),
            # product parameters
            d('#curShopName>a').text(),  # shop name
            d('#curShopName>a').attr.href,  # shop href
            d('.detail-val').text(),  # company name and telephone
            time.strftime('%Y-%m-%d %X', time.localtime())
        ]

        # over ride method for result store to mysql
        # def on_result(self, result):
        #     if result:
        #         db_server.data2DB(data=result)
        #     else:
        #         print u'result-->return None'
