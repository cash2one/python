#coding:utf-8
__author__ = 'Administrator'

from selenium import webdriver
import urllib
# 若果需要登录，请导入登录模块
from Alibaba_logoin import login
import time
import pymysql

def dataBase_conn():
    conn=pymysql.connect(host='10.118.187.12',user='admin',passwd='admin',charset='utf8',db='elec_platform')
    cursor=conn.cursor()
    return conn,cursor

def get_keyword():
    conn,cursor=dataBase_conn()
    sql_select="select keyword from alibaba_keyword where status_3c='0' limit 0,1"
    cursor.execute(sql_select)
    keyword=cursor.fetchone()
    conn.close()
    return keyword

def keyword_status_update(keyword=''):
    conn,cursor=dataBase_conn()
    sql_update='update alibaba_keyword set status_3c=1 where keyword=%s'
    cursor.execute(sql_update,keyword)
    conn.commit()
    conn.close()

def get_urlBegin(send_driver,keyword=('外套',)):
    driver=send_driver
    keyword=keyword[0].encode('GBK')
    url_keyword={'keywords':keyword,
                 'earseDirect':'false',
                 'button_click':'top',
                 'n':'y',
                 'sortType':'pop',
                 'pageSize':'30',}
    url_begin='http://s.1688.com/company/company_search.htm?'+urllib.urlencode(url_keyword)
    driver.get(url_begin)
    # 页面滚动，发现页面总数元素
    js_scroll=['var q=document.documentElement.scrollTop=%s'%item for item in [2000,4000,6000]]
    for item in js_scroll:
        driver.execute_script(item)
    # 提取页面总数
    try:
        counterTotal=driver.find_element_by_css_selector('.total-page').text
        counterTotal=int(counterTotal[1:len(counterTotal)-1])
        if counterTotal>1:
            return url_begin,counterTotal,driver
        else:return url_begin,0,driver
    except:return url_begin,0,driver

# 返回全部页面链接
# def get_urlAfter(keyword='内衣',counterTotal=100):
#     url_after=[]
#     if counterTotal:
#         for counter in range(counterTotal-1):
#             url_keyword={'keywords':keyword,
#                          'earseDirect':'false',
#                          'button_click':'top',
#                          'n':'y',
#                          'sortType':'pop',
#                          'pageSize':'30',
#                          'beginPage':counter+2}
#             url_after.append('http://s.1688.com/company/company_search.htm?'+urllib.urlencode(url_keyword))
#     # url_total=url_begin+url_after
#     return url_after

def is_exist_shop():
    d={}
    sql_select='select distinct shop_href from alibaba_shopinfo'
    conn,cursor=dataBase_conn()
    cursor=conn.cursor()
    cursor.execute(sql_select)
    shop_href=cursor.fetchall()
    for item in shop_href:
        d[item[0]]=1
    conn.close()
    return d

def get_shopInfoDetail(send_driver,d):
    conn,cursor=dataBase_conn()
    sql_insert='insert into alibaba_shopinfo (shop_name,shop_href,shop_icons_identification,' \
               'shop_credit_href,shop_icons_location,shop_icons_guarantee,shop_icons_icons_goldSupplier,' \
               'shop_mainBrand,shop_addr,shop_addrPhone_pageHref,shop_employee_counter,shop_field_name) ' \
               'values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    # send_driver参数须导入get_urlBegin函数返回的浏览器
    driver=send_driver
    d=d
    frames_first=driver.find_elements_by_css_selector('.company-list-item .list-item-left')
    if frames_first:
        for item in frames_first:
            shop_href=item.find_element_by_css_selector('.list-item-title>a:nth-child(1)').get_attribute('href')
            if shop_href in d.keys():
                print(item.find_element_by_css_selector('.list-item-title>a:nth-child(1)').text + u'已存在，不再添加！')
            else:
                shop_name=item.find_element_by_css_selector('.list-item-title>a:nth-child(1)').text
                print(u'收集到 '+shop_name+u' 页面信息；现总计收集到店铺 '+str(len(d)+1)+u' 个！')
                frames_second_icons=item.find_elements_by_css_selector('.list-item-icons>a')
                # icons初始化
                shop_icons_identification='NO';shop_credit_href='-';shop_icons_location='NO'
                shop_icons_guarantee=u'NO';shop_icons_icons_goldSupplier='NO'
                for item_icons in frames_second_icons:
                    if item_icons.get_attribute('title')==u'阿里巴巴建议您优先选择诚信通会员':
                        try:
                            shop_icons_identification=item_icons.find_element_by_css_selector('em').text
                        except:
                            shop_icons_identification=0
                        shop_credit_href=item_icons.get_attribute('href')
                    elif item_icons.get_attribute('title')==u'该企业已通过阿里巴巴实地认证，100%上门实拍':
                        shop_icons_location='YES'
                    elif item_icons.get_attribute('title')==u'该卖家支持先行赔付，保障买家交易安全':
                        shop_icons_guarantee='YES'
                    elif item_icons.get_attribute('title')==u'金牌供应商':
                        shop_icons_icons_goldSupplier='YES'
                    else:pass
                frames_mainBrand=item.find_elements_by_css_selector('.list-item-detail .detail-left div:nth-child(1) a span')
                shop_mainBrand=''
                for item_mainbrand in frames_mainBrand:
                    shop_mainBrand+=item_mainbrand.text
                shop_addr=item.find_element_by_css_selector\
                    ('.list-item-detail .detail-left div:nth-child(2) a:nth-child(2)').get_attribute('title').strip()
                shop_addrPhone_pageHref=item.find_element_by_css_selector\
                    ('.list-item-detail .detail-left div:nth-child(2) a:nth-child(2)').get_attribute('href')
                shop_employee_counter=item.find_element_by_css_selector\
                    ('.list-item-detail .detail-left div:nth-child(3) a').get_attribute('title')
                shop_field_name=item.find_element_by_css_selector('.list-item-detail .detail-right div b').text
                result=[shop_name,shop_href,shop_icons_identification,shop_credit_href,shop_icons_location,
                        shop_icons_guarantee,shop_icons_icons_goldSupplier,shop_mainBrand,shop_addr,
                        shop_addrPhone_pageHref,shop_employee_counter,shop_field_name]
                cursor.execute(sql_insert,result)
                conn.commit()
                d[shop_href]=1
    conn.close()
    return driver,d

def next_page(sendriver):
    driver=sendriver
    # js='var q=document.documentElement.scrollTop=%s'%10000
    # driver.execute_script(js)
    time.sleep(2)
    try:
        driver.find_element_by_css_selector('.page-next').click()
    except:pass
    return driver

if __name__=='__main__':
    # 返回登录的浏览器，如无须登录直接生成浏览器
    driver=webdriver.Firefox()
    # driver=webdriver.PhantomJS()
    # driver=webdriver.Chrome()
    driver.maximize_window()
    # driver=login(driver)
    keyword_temp=get_keyword()
    print(keyword_temp[0])
    d=is_exist_shop()
    url_begin=get_urlBegin(keyword=keyword_temp,send_driver=driver)
    while keyword_temp:
        time.sleep(10)
        driver=url_begin[2];url=url_begin[0];page_counter=url_begin[1]
        print(page_counter,url)
        for i in range(page_counter):
            if i==page_counter-1:
                break
            else:
                driver,d=get_shopInfoDetail(send_driver=driver,d=d)
                driver=next_page(sendriver=driver)
        print(u'已收集 ' + str(len(d)) + u' 间店铺！')
        keyword_status_update(keyword_temp)
        keyword_temp=get_keyword()

        url_begin=get_urlBegin(keyword=keyword_temp,send_driver=driver)
