#coding:utf8
__author__ = '613108'
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
from urllib import urlencode
import pymysql
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def get_productPageHref():
    conn,cursor=connection()
    sql_insert='insert into JD_get_productPageHref (classification,product,href) values(%s,%s,%s)'
    driver=webdriver.PhantomJS()
    driver.get('http://www.jd.com')
    driver.maximize_window()
    d={}
    time.sleep(5)
    move_elements=driver.find_elements_by_css_selector('#categorys-2014 .dd-inner div')
    for item_0 in move_elements:
        ActionChains(driver).move_to_element(item_0).perform()
        time.sleep(1)
        frames=driver.find_elements_by_css_selector('.subitems')
        for item_1 in frames:
            first_product_list=item_1.find_elements_by_css_selector('dl')
            for item_2 in first_product_list:
                classification=item_2.find_element_by_css_selector('dt').text.replace('>','').strip("\r\n")
                if classification=='':
                    break
                else:
                    second_product_list=item_2.find_elements_by_css_selector('dd>a')
                    for item_3 in second_product_list:
                        if item_3.get_attribute('class')=='img-link':
                            continue
                        else:
                            d[classification+'_'+item_3.text.strip()]=item_3.get_attribute('href')
                            result=[classification,item_3.text.strip(),item_3.get_attribute('href')]
                            cursor.execute(sql_insert,result)
                            conn.commit()
                            # print classification+'_'+item_3.text.strip()
                            # print d[classification+'_'+item_3.text]
                            # print len(d)
    driver.quit()
    return d

def connection():
    conn=pymysql.connect(host='10.118.187.5',user='root',passwd='root',charset='utf8',db='elec_platform')
    cursor=conn.cursor()
    return conn,cursor

def update_data(result):
    sql_update='insert into '

if __name__=='__main__':
    d=get_productPageHref()
    print(len(d))
    for k,v in d.items():
        print(k)
        print(v)
        print '-'*88

# 建表语句
# create table JD_get_productPageHref (id int,classification varchar(100),product varchar(150),href varchar(300))