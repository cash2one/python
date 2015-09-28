#coding:utf-8
__author__ = '613108'

from selenium import webdriver
from threading import Thread
import random
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append(r'C:\Users\613108\Desktop\Project\tool_self')
import My_Csv

result=[]

class Get_ProductInfo(Thread):
    def __init__(self,url_list):
        Thread.__init__(self)
        self.url_list=url_list

    def get_info(self):
        url_list=self.url_list
        try:
            driver=webdriver.PhantomJS()
        except:
            try:driver=webdriver.Chrome()
            except:pass
        driver.maximize_window()
        # try:
        for url in url_list:
            driver.get(url)
            print(url)
            for i in range(0,400*4,400):
                rand=random.gauss(100,100)
                scroll_height=i+rand
                js_scroll='var q=document.documentElement.scrollTop=%s'%scroll_height
                driver.execute_script(js_scroll)
                time.sleep(abs(random.gauss(1,0.5)))
            goods_frames=driver.find_elements_by_css_selector('.goods-item')
            print(len(goods_frames))
            for item in goods_frames:
                product_href=item.find_element_by_css_selector('.figure>a').get_attribute('href')
                print(product_href)
                # inner_frames=item.find_elements_by_css_selector('.item-info')
                # for item_2 in inner_frames:
                product_title=item.find_element_by_css_selector('.title>a').text
                product_price=item.find_element_by_css_selector('.price').text#.split('|')[0]
                try:product_price_del=item.find_element_by_class_name('.price>del').text#.split('|')[1]
                except:product_price_del='-'
                # try:product_adapt=item_2.find_element_by_class_name('item-adapt').text
                # except:product_adapt='-'
                # judge_count=item_2.find_element_by_class_name('item-comments').text[:-2]
                try:flag=item.find_element_by_css_selector('.flag').text
                except:flag='-'
                temp=[product_title,product_href,product_price,product_price_del,flag]
                result.append(temp)
                print('*'*50)
                for item_3 in temp:
                    print(item_3)
        # except:pass
        driver.quit()

    def run(self):
        self.get_info()

if __name__=='__main__':
    url_list=['http://list.mi.com/0-0-0-0-'+str(i+1)+'-0' for i in range(60)]
    Get_ProductInfo_thread=[]
    thread_count=10
    for i in range(thread_count):
        temp=Get_ProductInfo(url_list[((len(url_list)+thread_count-1)/thread_count)*i:((len(url_list)+thread_count-1)/thread_count)*(i+1)])
        Get_ProductInfo_thread.append(temp)
    for i in range(len(Get_ProductInfo_thread)):
        Get_ProductInfo_thread[i].start()
    for i in range(len(Get_ProductInfo_thread)):
        Get_ProductInfo_thread[i].join()

    title=['product_title','product_href','product_price','product_price_del','flag']
    writer=My_Csv.Write_Csv('d:/spider/xiaomi','xiaomi_product',title,result)
    writer.add_title_data()

    print('='*20+u'程序执行完毕，请检查所抓取的数据'+'='*20)