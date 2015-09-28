#coding:utf-8
__author__ = 'Administrator'
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import pymysql

conn=pymysql.connect(host='10.118.187.5',user='root',passwd='root',charset='utf8',db='elec_platform')
cursor=conn.cursor()
url='http://www.1688.com'
driver=webdriver.PhantomJS()
driver.maximize_window()
driver.get(url)
keyword_moveto=driver.find_elements_by_css_selector('#nav-sub>li')
print(len(keyword_moveto))
d={}
for item in keyword_moveto:
    ActionChains(driver).move_to_element(item).perform()
    keyword_all=driver.find_elements_by_css_selector('.text .fd-left>li>a')
    # time.sleep(1)
    temp=[key.text for key in keyword_all if key.text!='']
    for i in temp:
        d[i]=1
driver.quit()
for key in d:
    # print key
    sql_insert='insert into Alibaba_keyword (keyword) values(%s)'
    cursor.execute(sql_insert,key)
    conn.commit()
