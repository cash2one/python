#coding:utf-8
__author__ = '613108'

from selenium import webdriver
import re
import pymysql
import time

def connection():
    conn=pymysql.connect(host='10.118.187.12',user='admin',passwd='admin',charset='utf8',db='elec_platform')
    cursor=conn.cursor()
    return conn,cursor

def get_href():
    conn,cursor=connection()
    sql_select='select classification,product,href from jd_get_productpagehref where status=0 limit 0,1'
    cursor.execute(sql_select)
    href=cursor.fetchone()
    return href

def get_thirdParty_product_href(driver,url):
    conn,cursor=connection()
    sql_insert='insert into jd_thirdparty_product_href (classification,product,product_name,href,spider_time) values(%s,%s,%s,%s,%s)'
    driver=driver
    driver.get(url[2])
    page_counter=int(driver.find_element_by_css_selector('.fp-text>i').text)
    for i in range(page_counter):
        frames=driver.find_elements_by_css_selector('.gl-i-wrap.j-sku-item')
        for item in frames:
            spider_time=time.strftime('%Y-%m-%d %X',time.localtime())
            href=item.find_element_by_css_selector('.p-img>a').get_attribute('href')
            parttern=re.compile(r'[0-9]{10}')
            product_sku=parttern.findall(href)
            if product_sku:
                product_name='-'
                try:
                    product_name=item.find_element_by_css_selector('.p-name>a>em').text
                except:pass
                result=[url[0],url[1],product_name,href,spider_time]
                cursor.execute(sql_insert,result)
                conn.commit()
                # print(product_name)
                # print(href)
                # print('-'*100)
        if i<page_counter-2:
            try:
                driver.find_element_by_css_selector('.pn-next').click()
            except:
                try:driver.find_element_by_css_selector('.pn-next').click()
                except:pass
        else:break
    return driver

def update_productPageHref(href):
    conn,cursor=connection()
    sql_update='update jd_get_productpagehref set status=1 where href=%s'
    cursor.execute(sql_update,href)
    conn.commit()

if __name__=='__main__':
    driver=webdriver.PhantomJS()
    # driver.maximize_window()
    url=get_href()
    while url:
        print(url)
        driver=get_thirdParty_product_href(driver=driver,url=url)
        update_productPageHref(href=url[2])
        url=get_href()

# create table JD_thirdParty_product_href (id int,classification varchar(100),product varchar(100),product_name varchar(300),href varchar(300),spider_time varchar(100))