#coding:utf-8
__author__ = '613108'

from bs4 import BeautifulSoup
import pymysql
import re
import urllib2
from threading import Thread
from selenium import webdriver
import time
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
sys.path.append('C:/Users/613108/Desktop/Project/myTool')
import My_Csv

result=[]

send_headers = {'Referer':'http://www.vmall.com/',
                'User-Agent':'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Connection':'keep-alive'}

def get_productHref():
    url_total=[]
    url='http://www.vmall.com/'
    req=urllib2.Request(url=url,headers=send_headers)
    result=urllib2.urlopen(req)
    result=result.read()
    soup=BeautifulSoup(result,from_encoding='UTF-8')
    href_all=soup.find_all(attrs={'class':'category-info'})
    for i in range(len(href_all)-1):
        href=href_all[i].h3.a['href']
        href=url+href[1:]
        url_total.append(href)
    print(url_total)
    return url_total

class Get_ProductInfo(Thread):
    def __init__(self,url):
        Thread.__init__(self)
        self.url=url

    def get_info(self):
        driver=webdriver.PhantomJS()
        driver.maximize_window()
        driver.get(self.url)
        try:
            page_total_all=driver.find_elements_by_css_selector('.page-number.link')
            page_total=int(page_total_all[-1].text)
        except:page_total=1
        i=0
        while i<page_total:
            pro_total=driver.find_elements_by_css_selector('.pro-list.clearfix>ul>li')
            for item in pro_total:
                product_href='http://www.vmall.com'+\
                             re.split(r'#',item.find_element_by_css_selector('.p-img>a').get_attribute('href'))[0]
                product_name=item.find_element_by_css_selector('.p-name>a').text
                procudt_price=item.find_element_by_css_selector('.p-price b').text[1:]
                try:
                    if_selling=item.find_element_by_css_selector('.p-button-cart>span').text
                    if_selling=u'有货'
                except:if_selling=u'无货'
                judge_total=item.find_element_by_css_selector('.p-button-score>span').text[0:-3]
                temp=[product_name,product_href,procudt_price,if_selling,judge_total]
                result.append(temp)
                print('*'*50)
                for item in temp:
                    print(item)
            while i<page_total-1:
                driver.find_element_by_css_selector('.pgNext.link.next').click()
                break
            driver=driver
            i+=1
        driver.quit()

    def run(self):
        self.get_info()

if __name__=='__main__':
    url_list=get_productHref()
    while not url_list:
        time.sleep(5)
        url_list=get_productHref()

    Get_ProductInfo_thread=[]
    for url in url_list:
        Get_ProductInfo_thread.append(Get_ProductInfo(url))
    for i in range(len(url_list)):
        Get_ProductInfo_thread[i].start()
    for i in range(len(Get_ProductInfo_thread)):
        Get_ProductInfo_thread[i].join()

    title=['product_name','product_href','procudt_price','if_selling','judge_total']
    writer=My_Csv.Write_Csv('D:/spider/huawei','huawei_product',title,result)
    writer.add_title()
    writer.add_data()

    print(u'华为官方商城所有商品信息已经收集完毕！')