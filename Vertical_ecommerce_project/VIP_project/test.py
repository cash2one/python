#coding:utf-8
__author__ = '613108'

from selenium import webdriver
from bs4 import BeautifulSoup
import time
print('*'*20+u'开始抓取所有在售品牌信息'+'*'*20)
# def run(self):
# driver=webdriver.Firefox()
# driver=webdriver.Chrome()
driver=webdriver.PhantomJS()
driver.maximize_window()
driver.get('http://category.vip.com/')
# frames=driver.find_elements_by_css_selector('.floor')
tips=driver.find_elements_by_css_selector('#nav_list .ani')
for item in tips:
    print(item.text)
    print(item.is_displayed())
driver.quit()