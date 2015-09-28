#coding:utf-8
__author__ = '613108'

from selenium import webdriver
import re
from threading import Thread
from bs4 import  BeautifulSoup
import urllib2
from Queue import Queue
import csv
import time
import random
import socket
socket.setdefaulttimeout(120)
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append(r'C:\Users\613108\Desktop\Project\tool_self')
import My_Csv

shop_url_list=[]
shop_url_list_fail=[]

send_headers = {'Referer':'http://www.vmall.com/',
                'User-Agent':'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Connection':'keep-alive'}
queue=Queue(0)
queue_result=Queue(0)

class Get_Shop_Href():
    print('*'*20+u'开始抓取所有在售品牌信息'+'*'*20)
    def run(self):
        driver=webdriver.PhantomJS()
        driver.maximize_window()
        # driver=webdriver.Chrome()
        driver.get('http://category.vip.com/')
        frames=driver.find_elements_by_css_selector('.floor')
        tips=driver.find_elements_by_css_selector('#nav_list a')
        print(len(tips))
        for x in range(len(frames)):
            second_frames=frames[x].find_elements_by_css_selector('.limits a')
            for item_2 in second_frames:
                tip=tips[x].text
                # print(tip)
                if tip.find(u'车')>0:
                    break
                else:
                    brand=item_2.find_element_by_class_name('fl').get_attribute('title').encode('gbk','ignore')
                    href=(item_2.get_attribute('href').split('?')[0]+'?q=0|0|0|0|0|1').encode('gbk','ignore')
                tip=tip.encode('gbk','ignore')
                result=[tip,brand,href]
                shop_url_list.append(result)
        # 持久化
        writer=My_Csv.Write_Csv('d:/spider/vip','vip_brand',shop_url_list)
        writer.add_title_data(['category','brand','link'])
        driver.quit()

class Get_Product_Info(Thread):
    def __init__(self,url):
        Thread.__init__(self)
        self.url=url

    def get_info(self):
        # print('*'*20+u'开始抓取各产品信息'+'*'*20)
        try:
            req=urllib2.Request(url=self.url,headers=send_headers)
            result=urllib2.urlopen(req)
            soup=BeautifulSoup(result.read())
            result.close()
            # print(soup.encode('gbk','ignore'))
            frames=soup.find_all(attrs={'class':'is_hidden'})
            pat_discount=re.compile(r">\((?P<find>.+?)\)<")
            print('*'*10+self.url+'*'*10)
            for item in frames:
                product_href=item.p.a['href'].encode('gbk','ignore')
                product_title=item.div.p.a.contents[0].encode('gbk','ignore')
                product_price=item.div.p.nextSibling.em.contents[0][1:].encode('gbk','ignore')
                product_price_del=item.div.p.nextSibling.find('del').contents[0][1:].encode('gbk','ignore')
                product_discount=re.search(pat_discount,str(item.div.p.nextSibling))
                product_discount=product_discount.group('find')[:-3].encode('gbk','ignore')
                result=[self.url,product_title,product_href,product_price,product_price_del,product_discount]
                queue_result.put(result)
                # print('*'*50)
                # for item in result:
                #     print(item)
        except:
            # shop_url_list_second.append(self.url)
            queue.put(self.url)
            print(u'queue已存在 '+str(queue.qsize())+u' 个待二次抓取的网址')

    def run(self):
        self.get_info()

class Get_Product_Info_driver(Thread):
    def __init__(self,driver,url):
        Thread.__init__(self)
        self.driver=driver
        self.url=url

    def get_info(self):
        driver=self.driver
        try:
            driver.get(self.url)
            while True:
                js_scroll='var q=document.documentElement.scrollTop=%s'%(8000+random.gauss(1000,1000))
                driver.execute_script(js_scroll)
                time.sleep(abs(random.gauss(3,1)))
                frames=driver.find_elements_by_class_name('J_pro_items')
                for item in frames:
                    product_title=item.find_element_by_css_selector('.pro_list_tit a').text.encode('gbk','ignore')
                    product_href=item.find_element_by_css_selector('.pro_list_pic>a').get_attribute('href').encode('gbk','ignore')
                    product_price=item.find_element_by_css_selector('.deep_red>em').text[1:].encode('gbk','ignore')
                    product_price_del=item.find_element_by_css_selector('.deep_red+del').text[1:].encode('gbk','ignore')
                    product_discount=item.find_element_by_css_selector('.deep_red').text.split('(')[1].split(')')[0][:-1].encode('gbk','ignore')
                    result=[self.url,product_title,product_href,product_price,product_price_del,product_discount]
                    queue_result.put(result)
                    print('*'*50)
                    for item in result:
                        print(item)
                try:
                    driver.find_element_by_class_name('page-next-txt').click()
                    time.sleep(2)
                except:break
        except:shop_url_list_fail.append(self.url)
        finally:driver.quit()

    def run(self):
        self.get_info()

if __name__=='__main__':
    Get_Shop_Href().run()
    # url_test=['http://list.vip.com/471168.html?shop_r=473368&q=0|0|0|0|0|1',
    #           'http://www.vip.com/show-468950.html?q=0|0|0|0|0|1']
    print('*'*20+u'开始抓取各店铺产品信息'+'*'*20)
    for url in shop_url_list:
        test=Get_Product_Info(url[2])
        test.start()

    print('*'*20+str(queue_result.qsize())+'*'*20)
    print('*'*20+u'开始抓取需二次抓取的店铺信息'+'*'*20)
    url=queue.get(timeout=1000)
    while url:
        driver=webdriver.PhantomJS()
        driver.maximize_window()
        test_t=Get_Product_Info_driver(driver,url)
        try:
            url=queue.get(timeout=120)
        except:url=''
        test_t.start()
        # test_t.join()
    filename=time.strftime('%Y-%m-%d %H_%M_%S')
    csvfile=file('d:/spider/vip/vip_product_info_'+filename+'.csv','wb')
    writer=csv.writer(csvfile)
    writer.writerow(['shop_link','product_title','link','price','price_del','discount'])
    for i in range(queue_result.qsize()):
        writer.writerow(queue_result.get())
    csvfile.close()
    print('='*5+u'失败网址共：'+str(len(shop_url_list_fail))+u' 个'+'='*5)
    for url in shop_url_list_fail:
        print(url)

    print('*'*20+u'程序运行完毕，请检查数据'+'*'*20)