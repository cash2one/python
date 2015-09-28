#coding:utf-8
__author__ = 'Administrator'

from selenium import webdriver
import time
import pymysql
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def dataBase_conn():
    conn=pymysql.connect(host='10.118.187.12',user='admin',passwd='admin',charset='utf8',db='elec_platform')
    cursor=conn.cursor()
    return conn,cursor
    driver=webdriver.PhantomJS

# 更新数据库
def update_dbBase_base():
    conn,cursor=dataBase_conn()
    sql_select_detail='select distinct shop_name,shop_href,shop_addrPhone_pageHref from alibaba_shopinfo'
    sql_select_phone='select distinct shop_name,shop_href,shop_addrPhone_pageHref from alibaba_shopinfo_phone'
    sql_update='insert into alibaba_shopinfo_phone (shop_name,shop_href,shop_addrPhone_pageHref) values(%s,%s,%s)'
    cursor.execute(sql_select_detail)
    base_info=cursor.fetchall()
    cursor.execute(sql_select_phone)
    phone_info=cursor.fetchall()
    # 取基本信息表及公司信息表的差集
    update_info=[item for item in base_info if item not in phone_info]
    cursor.executemany(sql_update,update_info)
    conn.commit()

# 取联系方式页面链接
def get_phoneHref():
    conn,cursor=dataBase_conn()
    sql_select='select shop_addrPhone_pageHref from alibaba_shopinfo_phone where spider_time is null limit 0,1'
    cursor.execute(sql_select)
    phone_href=cursor.fetchone()
    return phone_href

# 提取联系方式
def get_phoneAddrSoOn(send_driver,url):
    # 登录操作
    driver=send_driver
    driver.get(url)
    # 提取信息
    contacts_name='-';contacts_sex='-';contacts_job='-'
    try:
        contacts_name=driver.find_element_by_css_selector('.membername').text
        contacts_sex=driver.find_element_by_css_selector('.contact-info>dl>dd').text.split(' ')[1]
        contacts_job=driver.find_element_by_css_selector('.contact-info>dl>dd').text.split('（')[1]
        contacts_job=contacts_job.split('）')[0]
    except:
        pass
    print(contacts_job)
    phone_frames=driver.find_elements_by_css_selector('.contcat-desc dl')
    cell_phone='-';tel_phone='-';fax_phone='-';shop_addr='-'
    for i in range(len(phone_frames)):
        text=driver.find_element_by_css_selector(".contcat-desc dl:nth-child("+str(i+1)+") dt").text.strip()
        if text==u'移动电话：':
            cell_phone=driver.find_element_by_css_selector(".contcat-desc dl:nth-child("+str(i+1)+") dd").text
            continue
        elif text==u'电      话：':
            tel_phone=driver.find_element_by_css_selector(".contcat-desc dl:nth-child("+str(i+1)+") dd").text
            continue
        elif text==u'传      真：':
            fax_phone=driver.find_element_by_css_selector(".contcat-desc dl:nth-child("+str(i+1)+") dd").text
            continue
        elif text==u'地      址：':
            shop_addr=driver.find_element_by_css_selector(".contcat-desc dl:nth-child("+str(i+1)+") dd").text
            continue
    spider_time=time.strftime("%Y-%m-%d %X",time.localtime())
    result=[contacts_name,contacts_sex,contacts_job,cell_phone,tel_phone,fax_phone,shop_addr,spider_time,url]
    return result,driver

# 依据收集回来的信息更新数据库对应字段，where取值店铺链接
def update_dbBase(result):
    conn,cursor=dataBase_conn()
    sql_update='update alibaba_shopinfo_phone set contacts_name=%s,contacts_sex=%s,contacts_job=%s,cell_phone=%s,' \
               'tel_phone=%s,fax_phone=%s,shop_addr=%s,spider_time=%s where shop_addrPhone_pageHref=%s'
    print(result)
    cursor.execute(sql_update,result)
    conn.commit()

# 导入Alibaba_login登录模块
def if_login(send_driver):
    from Alibaba_logoin import login
    driver=send_driver
    driver=login(send_driver=driver)
    return driver

if __name__=='__main__':
    update_dbBase_base()
    phone_href=get_phoneHref()
    driver=webdriver.Firefox()
    driver.maximize_window()
    driver=if_login(driver)
    while phone_href:
        result,driver=get_phoneAddrSoOn(send_driver=driver,url=phone_href)
        if result[3]==u'登录后可见':
            driver=if_login(driver)
            result,driver=get_phoneAddrSoOn(send_driver=driver,url=phone_href)
        update_dbBase(result)
        # 如果取不回来值取刷新数据库，刷新数据库之后还是无法取值则程序停止运行
        if get_phoneHref():
            phone_href=get_phoneHref()
        else:
            update_dbBase_base()
            phone_href=get_phoneHref()