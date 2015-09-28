# coding:utf8
__author__ = '613108'
import sys

from spiderFrame.downLoad import DownLoader

reload(sys)
sys.setdefaultencoding('utf8')

demo = DownLoader('http://www.Tmall.com')
test = demo.selenium()
print(test.decode('utf8', 'ignore'))
