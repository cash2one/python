#coding:utf-8
__author__ = '613108'

import scrapy
from bs4 import BeautifulSoup
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.loader import ItemLoader
from myproject.items import SecooItem

class MySpider(CrawlSpider):
    name = 'secoo.com'
    allowed_domains = ['secoo.com']
    start_urls = ['http://www.secoo.com/topic/A.html']

    rules = (Rule(LinkExtractor(allow=('/topic',),deny=('topic/detail',)),callback='parse_item'),)

    def parse_item(self,response):
        self.log('Hi,this is an item page!%s'%response.url)
        # soup = BeautifulSoup(response)
        # item=SecooItem()
        # item['topic']=response.xpath("//a[@target='_blank']/text()").extract()
        # print(item['topic'])
        # item['topic_href']=response.xpath("//a[@target='_blank']/@href").extract()
        # print(item['topic_href'])

        # item['topic'] = soup.find(attrs={'class':'seo_cont'}).a.extract()
        # print(item['topic'])
        # item['topic_href'] = soup.find(attrs={'class':'seo_cont'}).a['href'].extract()
        # print(item['topic_href'])

        item=ItemLoader(item=SecooItem(),response=response)
        item.get_css('.seo_cont>a',)
        return item