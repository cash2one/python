#coding:utf8
__author__ = '613108'
from ms_spider_fw.parser import PageParser
from ms_spider_fw.downLoad import DownLoader

DL= DownLoader.DownLoader('http://www.baidu.com')
src=DL.selenium()
PP= PageParser.PageParser(src)
print PP.pageLen()
# for item in PP.targetUrl(cssMark='.ui-page-num>a',urlHeader='https://list.tmall.com/search_product.htm'):
#     print(item)