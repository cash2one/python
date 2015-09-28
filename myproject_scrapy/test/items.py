#coding:utf-8
__author__ = '613108'

import scrapy

class DmozItem(scrapy.Item):
    title=scrapy.Field()
    link=scrapy.Field()
    desc=scrapy.Field()