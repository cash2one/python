#coding:utf-8
__author__ = '613108'
import scrapy
from myproject.items import SecooItem

class SecooSpider(scrapy.Spider):
    name = 'secoo'
    allowed_domains = ['www.secoo.com']
    start_urls = ['http://www.secoo.com/topic/A.html']

    def parse(self, response):
        frames = response.css('.seo_cont')
        for sel in frames:
            item = SecooItem()
            item['topic'] = sel.xpath('a/text()').extract()
            item['topic_href'] = sel.xpath('a/@href').extract()
            # print(item['topic'],item['topic_href'])
