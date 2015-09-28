#coding:utf-8
__author__ = '613108'
from selenium import webdriver
import pymysql
import time
from threading import Thread
from threading import Lock
import Queue

def connection():
    conn=pymysql.connect(host='10.118.187.12',user='admin',passwd='admin',charset='utf8',db='elec_platform')
    cursor=conn.cursor()
    return conn,cursor

def get_productHref():
    conn,cursor=connection()
    # sql_select='select href from jd_thirdparty_product_href where status is null limit 0,1'
    sql_select='select href from jd_thirdparty_product_href where status is null'
    # sql_update='update jd_thirdparty_product_href set status=0.5 where href=%s'
    cursor.execute(sql_select)
    href=cursor.fetchall()
    # href=cursor.fetchone()
    # cursor.execute(sql_update,href)
    # conn.commit()
    return href

def get_dict():
    conn,cursor=connection()
    sql_select='select shop_href from jd_thirdparty_shop_href'
    cursor.execute(sql_select)
    href=cursor.fetchall()
    d={}
    for item in href:
        d[item]=1
    return d

class Jd_Shop_Dict():
    def __init__(self,d):
        self.value=d
        self.lock=Lock()

    def add(self,url):
        # self.value[url]=1
        d=self.value
        d[url]=1
        return d

# 导入字典判断是否已添加，并动态添加字元素
def get_shopHref(driver,Dict,url='http://item.jd.com/1243061305.html'):
    driver=driver
    driver.get(url)
    print(url)
    conn,cursor=connection()
    d=Dict.value
    sql_insert='insert into jd_thirdparty_shop_href (shop_name,shop_href,shop_judge_href,pop_score_total,' \
               'product_score,service_score,temporality_score,promotion,send_service,' \
               'add_service,spider_time) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    shop_href=''
    try:
        shop_href=driver.find_element_by_css_selector('.name').get_attribute('href')
        if shop_href in d.keys():
            print(shop_href+u' 已存在！')
            pass
        else:
            # d[shop_href]=1
            shop_name=driver.find_element_by_css_selector('.name').text
            shop_judge_href=driver.find_element_by_css_selector('.evaluate-grade>strong>a').get_attribute('href')
            pop_score_total=driver.find_element_by_css_selector('.evaluate-grade a').text
            pop_score_sigle=driver.find_elements_by_css_selector('.pop-score-part2 span')
            product_score=pop_score_sigle[0].text
            service_score=pop_score_sigle[1].text
            temporality_score=pop_score_sigle[2].text
            promotion_s=driver.find_elements_by_css_selector('#itemInfo #summary .J-prom em')
            temp=[]
            for item in promotion_s:
                temp.append(item.text)
            promotion='_*|*_'.join(temp)
            send_service=driver.find_element_by_css_selector('#itemInfo #summary #summary-service .dd').text
            add_service='-'
            try:
                add_service=driver.find_element_by_css_selector('#itemInfo #summary #store-prompt >a').text
            except:pass
            spider_time=time.strftime('%Y-%m-%d %X',time.localtime())
            result=[shop_name,shop_href,shop_judge_href,pop_score_total,product_score,service_score,temporality_score,
                    promotion,send_service,add_service,spider_time]
            cursor.execute(sql_insert,result)
            conn.commit()
            # d[shop_href]=1
            print(shop_name)
            print(shop_href)
            print('*'*50)
    except:pass
    return d,driver,shop_href

def update_productHref(href):
    conn,cursor=connection()
    sql_update='update jd_thirdparty_product_href set status=1 where href=%s'
    cursor.execute(sql_update,href)
    conn.commit()

# 创建共享队列
def get_queueHref():
    queue_href=Queue.Queue(0)
    url_list=get_productHref()
    for item in url_list:
        queue_href.put(item[0])
    return queue_href

class Get_ShopHref(Thread):
    def __init__(self,queue_href):
        Thread.__init__(self)
        self.queue_href=queue_href

    def run(self):
        driver=webdriver.PhantomJS()
        # driver=webdriver.Chrome()
        driver.maximize_window()
        queue=self.queue_href
        url=queue.get()
        # print(u'queue的大小为：'+str(queue._qsize()))
        d=get_dict()
        dict=Jd_Shop_Dict(d)
        while url:
            dict.lock.acquire()
            d,driver,href=get_shopHref(driver,dict,url)
            if href:
                dict.add(url=href)
                update_productHref(url)
            else:
                pass
            url=queue.get()
            dict.lock.release()
        driver.quit()

if __name__=='__main__':
    # driver=webdriver.PhantomJS()
    # url=get_productHref()
    # d=get_dict()
    # while url:
    #     d,driver=get_shopHref(driver,url,d)
    #     update_productHref(url)
    #     url=get_productHref()
    Get_ShopHref_thread=[]
    thread_count=5
    queue_href=get_queueHref()
    for i in range(thread_count):
        Get_ShopHref_thread.append(Get_ShopHref(queue_href))
    for i in range(thread_count):
        Get_ShopHref_thread[i].start()
    for i in range(thread_count):
        Get_ShopHref_thread[i].join()

# create table  JD_thirdParty_shop_href (id int,shop_name varchar(150),shop_href varchar(150),pop_score_total varchar(50) varchar(50),product_score varchar(50),service_score varchar(50),temporality_score varchar(50),promotion varchar(50),send_service varchar(50),add_service varchar(50),spider_time  varchar(100))