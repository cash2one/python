# coding:utf-8
__author__ = 'Mingsong_Yang'
import pymysql
from selenium import webdriver
import time
import string

# 定义数据库链接
def mysql_conn():
    conn = pymysql.connect(host='10.118.187.5', user='root', passwd='root', charset='utf8', db='elec_platform')
    cursor = conn.cursor()
    return conn, cursor


# 基本信息表提取店铺信息（店铺名称及链接）更新至公司信息表
def update_shop_company():
    # conn,cursor=mysql_conn()
    # sql_select_base='select distinct name,href,judgepage_href from yms_tmall_shopinfo_new'
    # sql_select_com='select distinct name,href,judgepage_href from yms_tmall_shopinfo_com'
    # sql_update='insert into yms_tmall_shopinfo_com (name,href,judgepage_href) values(%s,%s,%s)'
    # cursor.execute(sql_select_base)
    # base_info=cursor.fetchall()
    # cursor.execute(sql_select_com)
    # com_info=cursor.fetchall()
    # # 取基本信息表及公司信息表的差集
    # update_info=[item for item in base_info if item not in com_info]
    # for item in update_info:
    #     cursor.execute(sql_update,item)
    # conn.commit()
    # conn.close()
    pass


# 取购买评价地址
def get_link():
    conn, cursor = mysql_conn()
    sql_select_com = 'select name,judgepage_href from yms_tmall_shopinfo_com_withOutJudge where spider_time is null limit 0,1'
    cursor.execute(sql_select_com)
    shop_NameLink = cursor.fetchone()
    conn.close()
    return shop_NameLink


# 进入_购买心得评价页面，并返回浏览器
def judge_page(send_driver='', judge_link='http://rate.taobao.com/user-rate-UvFc0OmQYOFv4ONTT.htm'):
    link = judge_link
    # print(link)
    if send_driver:
        driver = send_driver
    else:
        # driver=webdriver.Firefox()
        driver = webdriver.Chrome()
        # driver=webdriver.PhantomJS()
    try:
        driver.get(link)
    except:
        driver.quit()
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get(link)
    return driver


# 页面信息提取
def get_data(send_driver):
    driver = send_driver
    try:
        major_business = driver.find_element_by_css_selector('li.company+li>a').text.strip()
        company_name = driver.find_element_by_css_selector('li.company>div:nth-child(2)').text.strip()
        seller_bond = driver.find_element_by_css_selector('.charge>span').text[1:-3].strip()
        seller_bond = string.replace(seller_bond, ',', '', 1)
        # 海外商家无执照信息
        try:
            license_href = driver.find_element_by_css_selector('#J_ShowLicence').get_attribute('href')
        except:
            license_href = '-'
        seller_commitment_all = driver.find_elements_by_css_selector('.xiaobao-box>div>a')
        text_temp = []
        counter = 0
        for item in seller_commitment_all:
            text_temp.append(item.get_attribute('title').strip())
            counter += 1
        text = '/'.join(text_temp)
        seller_commitment = text
        seller_commitment_counter = counter
        try:
            refund_time = driver.find_element_by_css_selector('div.bg30>div:nth-child(1)>span:nth-child(2)').text[:-2]
            refund_time_avg = driver.find_element_by_css_selector('div.bg30>div:nth-child(1)>span:nth-child(4)').text[
                              :-2]
            refund_self = driver.find_element_by_css_selector('div.bg30>div:nth-child(2)>span:nth-child(2)').text
            refund_self_avg = driver.find_element_by_css_selector('div.bg30>div:nth-child(2)>span:nth-child(4)').text
            refund_dispute = driver.find_element_by_css_selector('div.bg30>div:nth-child(3)>span:nth-child(2)').text
            refund_dispute_avg = driver.find_element_by_css_selector('div.bg30>div:nth-child(3)>span:nth-child(4)').text
        except:
            refund_time = '-'
            refund_time_avg = '-'
            refund_self = '-'
            refund_self_avg = '-'
            refund_dispute = '-'
            refund_dispute_avg = '-'
        judge_detail = '-'
        # judge_detail_all=driver.find_elements_by_css_selector('.tb-r-cnt')
        # judge_detail=[]
        # for item in judge_detail_all:
        #     judge_detail.append(item.text)
        # judge_detail='_*|*_'.join(judge_detail)
    except:
        company_name = '-'
        major_business = '-'
        seller_bond = '-'
        refund_time = '-'
        refund_time_avg = '-'
        refund_self = '-'
        refund_self_avg = '-'
        refund_dispute = '-'
        refund_dispute_avg = '-'
        seller_commitment = '-'
        seller_commitment_counter = '-'
        license_href = '-'
        judge_detail = '-'
    spider_time = time.strftime('%Y-%m-%d %X', time.localtime())
    data = [company_name, major_business, seller_bond, refund_time, refund_time_avg,
            refund_self, refund_self_avg, refund_dispute, refund_dispute_avg,
            seller_commitment, seller_commitment_counter, license_href, judge_detail, spider_time]
    # driver.close()
    return data, driver


# 公司信息表更新
def update_com_table(update_data):
    conn, cursor = mysql_conn()
    sql_update = 'update yms_tmall_shopinfo_com_withOutJudge set ' \
                 'company_name=%s,major_business=%s,seller_bond=%s,' \
                 'refund_time=%s,refund_time_avg=%s,refund_self=%s,' \
                 'refund_self_avg=%s,refund_dispute=%s,refund_dispute_avg=%s,' \
                 'seller_commitment=%s,seller_commitment_counter=%s,' \
                 'license_href=%s,judge_detail=%s,spider_time=%s where name=%s'
    cursor.execute(sql_update, update_data)
    conn.commit()
    conn.close()

# 主调用
if __name__ == '__main__':
    while True:
        # time.sleep(600)
        # update_shop_company()
        link_temp = get_link()
        if link_temp:
            shop_name, url = link_temp
            driver = judge_page(judge_link=url)
            driver.maximize_window()
            while url:
                update_data, driver = get_data(send_driver=driver)
                update_data.append(shop_name)
                update_com_table(update_data)
                shop_name, url = get_link()
                driver = judge_page(send_driver=driver, judge_link=url)
                print(driver.title.split('-')[0] + u'页面内容已添加！')
        else:
            continue
