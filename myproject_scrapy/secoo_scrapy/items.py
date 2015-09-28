#coding:utf-8
__author__ = '613108'
import scrapy

class SecooItem(scrapy.Item):
    topic=scrapy.Field()
    topic_href=scrapy.Field()