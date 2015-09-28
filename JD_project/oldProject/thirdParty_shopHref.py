#coding:utf-8
__author__ = '613108'
from selenium import webdriver
import pymysql
import time

def connection():
    conn=pymysql.connect(host='10.118.187.12',user='admin',passwd='admin',charset='utf8',db='elec_platform')
    cursor=conn.cursor()
    return conn,cursor

def get_productHref():
    conn,cursor=connection()
    sql_select='select href from jd_thirdparty_product_href where status is null limit 0,1'
    cursor.execute(sql_select)
    href=cursor.fetchone()
    return href[0]

def get_dict():
    conn,cursor=connection()
    sql_select='select shop_href from jd_thirdparty_shop_href'
    cursor.execute(sql_select)
    href=cursor.fetchall()
    d={}
    for item in href:
        d[item]=1
    return d

# 导入字典判断是否已添加，并动态添加字元素
def get_shopHref(driver,url='http://item.jd.com/1243061305.html',
                 d={'http://mupaidi.jd.com':1}):
    driver=driver
    driver.get(url)
    conn,cursor=connection()
    sql_insert='insert into jd_thirdparty_shop_href (shop_name,shop_href,shop_judge_href,pop_score_total,' \
               'product_score,service_score,temporality_score,promotion,send_service,' \
               'add_service,spider_time) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    try:
        shop_href=driver.find_element_by_css_selector('.name').get_attribute('href')
        if shop_href in d.keys():
            pass
        else:
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
            d[shop_href]=1
    except:pass
    return d,driver

def update_productHref(href):
    conn,cursor=connection()
    sql_update='update jd_thirdparty_product_href set status=1 where href=%s'
    cursor.execute(sql_update,href)
    conn.commit()

if __name__=='__main__':
    driver=webdriver.PhantomJS()
    url=get_productHref()
    d=get_dict()
    while url:
        d,driver=get_shopHref(driver,url,d)
        update_productHref(url)
        url=get_productHref()

# create table  JD_thirdParty_shop_href (id int,shop_name varchar(150),shop_href varchar(150),pop_score_total varchar(50) varchar(50),product_score varchar(50),service_score varchar(50),temporality_score varchar(50),promotion varchar(50),send_service varchar(50),add_service varchar(50),spider_time  varchar(100))