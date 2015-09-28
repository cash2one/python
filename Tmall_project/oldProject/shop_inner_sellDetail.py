#coding:utf-8
__author__ = 'Administrator'
import pymysql
from selenium import webdriver
import time
import urllib
import string

# 定义数据库链接
def mysql_conn():
    conn=pymysql.connect(host='10.118.187.12',user='admin',passwd='admin',charset='utf8',db='elec_platform')
    cursor=conn.cursor()
    return conn,cursor

def get_shopHref(i):
    conn,cursor=mysql_conn()
    sql_select='select href from yms_tmall_shopinfo_new limit 0,1'
    cursor.execute(sql_select)
    shopHref=cursor.fetchone()
    conn.close()
    return shopHref

def get_shopSearchPageHref(shop_href,i=1):
    searchPageHref={'search':'y',
                    'pageNo':i,
                    'tsearch':'y'}
    href=shop_href+'/search.htm?'+urllib.urlencode(searchPageHref)
    return href

def getGoodsPageHref(href='http://wenlancp.tmall.com/search.htm?spm=a1z10.3-b.w4011-8899650232.200.UJLYR3&search=y&pageNo=1&tsearch=y#anchor',senddriver=''):
    if senddriver:
        driver=senddriver
    else:
        driver=webdriver.PhantomJS()
    driver.get(href)
    # driver.maximize_window()
    pageLen=driver.find_element_by_css_selector('.ui-page-s-len').text[2:]
    pageLen=int(pageLen)
    print(pageLen)
    excute=1
    goodsHref=[]
    while 1:
        frames=driver.find_elements_by_css_selector('.J_TItems>div')
        print(len(frames))
        for i in range(len(frames)):
            if frames[i].get_attribute('class')=='pagination':
                break
            else:
                frames_inner=frames[i].find_elements_by_css_selector('dl>dt>a')
                goodsHref_temp=[item.get_attribute('href') for item in frames_inner]
            goodsHref+=goodsHref_temp
        if excute==pageLen:
            break
        else:
            driver.find_element_by_css_selector('.J_SearchAsync.next').click()
        # time.sleep(3)
        excute+=1
    return goodsHref,driver

def getGoodsSellDetail(href,senddriver):
    driver=senddriver
    driver.get(href)
    js_scroll='var q=document.documentElement.scrollTop=%s'%2000
    driver.execute_script(js_scroll)
    # driver.find_element_by_partial_link_text(u'月成交记录').click()
    find_text=u'月成交记录'
    driver.find_element_by_partial_link_text(find_text).click()
    time.sleep(1)
    frames=driver.find_elements_by_css_selector('colgroup~tbody>tr')
    result=[(frames[i].find_element_by_css_selector('td>div:nth-child(1)').text,
             # frames[i].find_element_by_css_selector('td>div:nth-child(2)>.rank').get_attribute('title'),
             frames[i].find_element_by_css_selector('td:nth-child(2)').text,
             frames[i].find_element_by_css_selector('td:nth-child(3)').text,
             frames[i].find_element_by_css_selector('td:nth-child(4)').text.replace("\n"," "))
            for i in range(1,len(frames))]
    return result,driver

def update_dataBase(result):
    conn,cursor=mysql_conn()
    sql_inset='insert into yms_tmall_shopinner_selldetail (industry,shop_name,shop_href,buyer,buy_what,buy_count,buy_time) ' \
              'values(%s,%s,%s,%s,%s,%s)'
    cursor.execute(sql_inset,result)
    conn.commit()
    conn.close()

if __name__=='__main__':
    par=(u'3C数码',u'云展数码专营店','http://shop102936285.taobao.com/')
    shopSearchHref=get_shopSearchPageHref(shop_href=par[2])
    goodsHref,driver=getGoodsPageHref(href=shopSearchHref)
    for i in goodsHref:
        result,driver=getGoodsSellDetail(href=i,senddriver=driver)
        for x in result:
            for y in x:
                print(y)
        result=par+result
        # update_dataBase(result)

# create table yms_tmall_shopinner_selldetail (id int,industry varchar(200),shop_name varchar(200),shop_href varchar(200),buyer varchar(200),buy_what varchar(200),buy_count varchar(200),buy_time varchar(200))