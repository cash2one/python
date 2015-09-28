#coding:utf-8
__author__ = '613108'

from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import urllib
import time
import pymysql
import random
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def mysql_conn():
    conn=pymysql.connect(host='10.118.187.12',user='admin',passwd='admin',charset='utf8',db='elec_platform')
    cursor=conn.cursor()
    return conn,cursor

def get_shopname():
    sql_select='select name from tmall_baseinfo_everyweek_original where staus=0 limit 0,1;'
    conn,cursor=mysql_conn()
    cursor.execute(sql_select)
    shop_name=cursor.fetchone()
    conn.close()
    return shop_name[0]

def update_status(shop_name):
    sql_update='update tmall_baseinfo_everyweek_original set staus=1 where name=%s'
    conn,cursor=mysql_conn()
    cursor.execute(sql_update,(shop_name,))
    conn.commit()
    conn.close()

def update_status_temp(shop_name):
    sql_update='update tmall_baseinfo_everyweek_original set staus=0.5 where name=%s'
    conn,cursor=mysql_conn()
    cursor.execute(sql_update,(shop_name,))
    conn.commit()
    conn.close()

def insert_everyweek(result):
    sql_insert='insert into tmall_baseinfo_everyweek (' \
               'name,href,judgepage_href,seller,addr,brand,monthsale,productsum,dsr_desc_mark,' \
               'dsr_desc_avg,dsr_service_mark,dsr_service_avg,dsr_sending_mark,dsr_sending_avg,' \
               'product_link_1,price_1,product_link_2,price_2,product_link_3,price_3,product_link_4,price_4,week,spider_time)' \
               'values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
    conn,cursor=mysql_conn()
    cursor.execute(sql_insert,result)
    conn.commit()
    conn.close()

def get_href(shop_name='松下电器旗舰店'):
    href={'initiative_id':'staobaoz_20120515','q':shop_name,'app':'shopsearch'}
    href='http://s.taobao.com/search?'+urllib.urlencode(href)
    return href

def get_shopdetail(shop_name,send_driver):
    driver=send_driver
    page_all_shop=driver.find_elements_by_css_selector('.list-item')
    shop_data_temp=[]
    if page_all_shop:
        for one_shop in page_all_shop:
            name=one_shop.find_element_by_css_selector('.shop-name.J_shop_name').text.strip()
            if name==shop_name:
                href=one_shop.find_element_by_css_selector('.list-img>a').get_attribute('href').split('?')[0]
                seller=one_shop.find_element_by_css_selector('.shop-info-list>a').text.strip()
                addr=one_shop.find_element_by_css_selector('.shop-address').text.strip()
                brand=one_shop.find_element_by_css_selector('.main-cat>a').text.strip()
                monthsale=one_shop.find_element_by_css_selector('.info-sale>em').text
                productsum=one_shop.find_element_by_css_selector('.info-sum>em').text
                move_element=one_shop.find_element_by_css_selector('.descr-icon')
                ActionChains(driver).move_to_element(move_element).perform()
                dsr_desc_mark=one_shop.find_element_by_css_selector('div.shop-mark li:nth-child(2) a').text
                judgePage_href=one_shop.find_element_by_css_selector('div.shop-mark li:nth-child(2) a').get_attribute('href')
                dsr_service_mark=one_shop.find_element_by_css_selector('div.shop-mark li:nth-child(3) a').text
                dsr_sending_mark=one_shop.find_element_by_css_selector('div.shop-mark li:nth-child(4) a').text
                if one_shop.find_element_by_css_selector('div.shop-avg li:nth-child(2) span').get_attribute('class')=='lessthan':
                    dsr_desc_avg='-'+one_shop.find_element_by_css_selector('div.shop-avg li:nth-child(2) span').text[2:]
                else:
                    dsr_desc_avg=one_shop.find_element_by_css_selector('div.shop-avg li:nth-child(2) span').text[2:]
                if one_shop.find_element_by_css_selector('div.shop-avg li:nth-child(3) span').get_attribute('class')=='lessthan':
                    dsr_service_avg='-'+one_shop.find_element_by_css_selector('div.shop-avg li:nth-child(3) span').text[2:]
                else:
                    dsr_service_avg=one_shop.find_element_by_css_selector('div.shop-avg li:nth-child(3) span').text[2:]
                if one_shop.find_element_by_css_selector('div.shop-avg li:nth-child(4) span').get_attribute('class')=='lessthan':
                    dsr_sending_avg='-'+one_shop.find_element_by_css_selector('div.shop-avg li:nth-child(4) span').text[2:]
                else:
                    dsr_sending_avg=one_shop.find_element_by_css_selector('div.shop-avg li:nth-child(4) span').text[2:]
                # 添加商品信息
                product_links=one_shop.find_elements_by_css_selector('ul li:nth-child(3) div.one-product')
                try:
                    if product_links:
                        for i in range(len(product_links)):
                            names=globals()
                            names['product_link_'+str(i+1)]=product_links[i].find_element_by_css_selector('.product-img a').get_attribute('href')
                            names['price_'+str(i+1)]=product_links[i].find_element_by_css_selector('.price-wrap span:nth-child(3)').text
                    else:
                        for i in range(4):
                            names=globals()
                            names['product_link_'+str(i+1)]='-'
                            names['price_'+str(i+1)]='-'
                except:
                    pass
                week=time.strftime('%W')
                spider_time=time.strftime("%Y-%m-%d %X",time.localtime())
                shop_data_temp=[name,href,judgePage_href,seller,addr,brand,monthsale,
                                productsum,dsr_desc_mark,dsr_desc_avg,dsr_service_mark,dsr_service_avg,dsr_sending_mark,dsr_sending_avg,
                                product_link_1,price_1,product_link_2,price_2,product_link_3,price_3,product_link_4,price_4,week,spider_time]
                break
    return shop_data_temp,driver

if __name__=='__main__':
    shop_name_temp=get_shopname()
    print(shop_name_temp)
    update_status_temp(shop_name_temp)
    driver=webdriver.PhantomJS()
    driver.maximize_window()
    while shop_name_temp:
        shop_href_temp=get_href(shop_name_temp)
        print(shop_href_temp)
        driver.get(shop_href_temp)
        print(driver.title)
        scroll_counter=abs(random.gauss(500,200))
        js_scroll='var q=document.documentElement.scrollTop=%s'%scroll_counter
        driver.execute_script(js_scroll)
        # if driver.title==u'淘宝店铺搜索':
        #     print(u'休眠中……淘宝太恶心了……')
        #     driver.quit()
        #     time.sleep(abs(random.gauss(60,30)))
        #     driver=webdriver.PhantomJS()
        #     driver.maximize_window()
        #     continue
        # else:
        try:
            if_noexsit=driver.find_element_by_css_selector('.taogongzai').get_attribute('class')

            update_status(shop_name_temp)
            continue
        except:
            pass
        try:
            result,driver=get_shopdetail(shop_name=shop_name_temp,send_driver=driver)
            print(result)
            insert_everyweek(result=result)
            print(result)
            update_status(shop_name_temp)
            print(result[0]+u' 店铺信息已更新~~~')
        except:
            pass
        finally:
            shop_name_temp=get_shopname()
            update_status_temp(shop_name_temp)
            time.sleep(abs(random.gauss(0.5,0.5)))