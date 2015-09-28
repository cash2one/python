#coding:utf8
__author__ = '613108'
from selenium import webdriver
import time
import random
import pymysql

def shop_goin(url='http://youngor.tmall.com/search.htm?spm=a1z10.3-b.w4011-3212035655.83.E8OHqH&search=y&pageNo=1&tsearch=y#anchor'):
    driver=webdriver.PhantomJS()
    driver.get(url)
    text=driver.find_element_by_css_selector('.ui-page-s-len').text
    text=text.split('/')
    page_counter=text[1]
    print page_counter
    return driver,page_counter

def good_link():
    driver,page_counter=shop_goin()
    counter_good=0
    counter_turnpage=0
    good_list=[]
    while counter_turnpage<=page_counter:
        all_good=driver.find_elements_by_css_selector('.item')
        len_all_good=len(all_good)
        for seq in range(len_all_good-10):
            good_list_temp=[]
            key=all_good[seq]
            key_get=key.find_element_by_css_selector('.item-name')
            good_text=key_get.text
            good_href=key_get.get_attribute('href')
            good_price=key.find_element_by_css_selector('.c-price').text
            good_list_temp=[good_text,good_href,good_price]
            good_list.append(good_list_temp)
            counter_good+=1
            print(counter_good)
        try:
            driver.find_element_by_css_selector('.J_SearchAsync.next').click()
        except:
            break
        counter_turnpage+=1
    driver.quit()
    return good_list

def good_page_in():
    conn=pymysql.connect(host='10.118.187.3',user='root',passwd='root',charset='utf8',db='yms_tmallinfo')
    cursor=conn.cursor()
    sql_insert="insert into yageer_good_info (good_text,good_href,good_price,promo_price,original_price,month_sell,total_judge) values(%s,%s,%s,%s,%s,%s,%s)"
    driver=webdriver.PhantomJS()
    good_list=good_link()
    for key in good_list:
        url=key[1]
        driver.get(url)
        key_temp=[]
        try:
            promo_price=driver.find_element_by_css_selector('#J_PromoPrice span').text
            original_price=driver.find_element_by_css_selector('#J_StrPriceModBox span').text
            month_sell=driver.find_element_by_css_selector('ul.tm-ind-panel li:nth-child(1) span:nth-child(2)').text
            total_judge=driver.find_element_by_css_selector('ul.tm-ind-panel li:nth-child(2) span:nth-child(2)').text
            key_temp=[promo_price,original_price,month_sell,total_judge]
            key.append(key_temp)
            cursor.execute(sql_insert,key)
            conn.commit()
        except:
            continue
        print(driver.title())
        time.sleep(random.gauss(12,5))
    conn.close()
    driver.quit()
    return good_list

list=good_page_in()
for key in list:
    for item in key:
        print item