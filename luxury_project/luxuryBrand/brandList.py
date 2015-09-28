# coding:utf8
__author__ = '613108'
import sys
from spiderFrame.downLoad.DownLoader import DownLoader
from pyquery import PyQuery as pq
reload(sys)
sys.setdefaultencoding('utf8')

def brandList():
    DL = DownLoader('http://www.xiu.com/brand.html')
    src = DL.selenium()
    d=pq(src)
    text=d.find('li>dl>dd>a').my_text()
    res=[]
    for item in text:
        res.extend(item.split('/'))
    res=map(lambda x:x.replace(' ',''),res)
    return res
