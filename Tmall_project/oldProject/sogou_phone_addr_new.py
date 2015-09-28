#coding:utf-8
__author__ = 'Administrator'

from selenium import webdriver
import pymysql
import time
import random
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# 定义数据库链接
def mysql_conn():
    conn=pymysql.connect(host='10.118.187.5',user='root',passwd='root',charset='utf8',db='elec_platform')
    cursor=conn.cursor()
    return conn,cursor

def update_database():
    conn,cursor=mysql_conn()
    sql_select_from='select distinct company_name from yms_tmall_shopinfo_com_withoutjudge ' \
                    'where company_name is not null'
    sql_select_target='select distinct company_name from yms_tmall_phone_addr_temp'
    sql_update='insert into yms_tmall_phone_addr_temp (company_name) values(%s)'
    cursor.execute(sql_select_from)
    from_info=cursor.fetchall()
    cursor.execute(sql_select_target)
    target_info=cursor.fetchall()
    update_info=[item for item in from_info if item not in target_info]
    for item in update_info:
        cursor.execute(sql_update,item)
    conn.commit()
    conn.close()

def get_record():
    conn,cursor=mysql_conn()
    sql_select='select company_name from yms_tmall_phone_addr_temp ' \
               'where spider_time is null limit 0,1'
    cursor.execute(sql_select)
    record=cursor.fetchone()
    return record

def web_site(send_driver='',url='http://www.sogou.com/zhaopin',
             css_searchbox='#query',css_submit='#stb',keyword=u'北京旺佳富鑫科技发展有限公司'):
    # 参数默认为搜狗招聘
    if send_driver:
        driver=send_driver
        # driver.get(url)
        driver.find_element_by_css_selector('#upquery').clear()
        driver.find_element_by_css_selector('#upquery').send_keys(keyword)
        driver.find_element_by_css_selector('#searchBtn').click()
    else:
        # driver=webdriver.PhantomJS()
        driver=webdriver.Chrome()
        # driver=webdriver.Firefox()
        driver.maximize_window()
        driver.get(url)
        driver.find_element_by_css_selector(css_searchbox).clear()
        driver.find_element_by_css_selector(css_searchbox).send_keys(keyword)
        driver.find_element_by_css_selector(css_submit).click()
    # 返回浏览窗口
    return driver

def get_frame(driver,css_frame='.joblist>tbody>tr'):
    frames=driver.find_elements_by_css_selector(css_frame)
    return frames

def get_result(frame,css_text='td:nth-child(2)>a>em',css_detail='td:nth-child(1)>h2>a',
             css_href='td:nth-child(1)>h2>a',css_city='td:nth-child(3)',
             css_source='td:nth-child(5)>a'):
    # css_text:公司名称，用于判断是否为待查找公司
    # css_detail:职位名称
    # css_href:职位源链接
    # css_city:城市
    # css_source:来源渠道
    spider_time=time.strftime('%Y-%m-%d %X',time.localtime())
    result=[spider_time,
            frame.find_element_by_css_selector(css_text).text,
            frame.find_element_by_css_selector(css_detail).text,
            frame.find_element_by_css_selector(css_href).get_attribute('href'),
            frame.find_element_by_css_selector(css_city).text,
            frame.find_element_by_css_selector(css_source).text]
    # print frame.find_element_by_css_selector(css_source).text
    return result

def update_result_01(result):
    conn,cursor=mysql_conn()
    sql_update="update yms_tmall_phone_addr_temp set " \
               "source_detail_1=%s,source_href_1=%s,source_city_1=%s,source_name_1=%s where company_name=%s"
    cursor.execute(sql_update,result)
    conn.commit()

def update_result_02(result):
    conn,cursor=mysql_conn()
    sql_update="update yms_tmall_phone_addr_temp set " \
               "source_detail_2=%s,source_href_2=%s,source_city_2=%s,source_name_2=%s where company_name=%s"
    cursor.execute(sql_update,result)
    conn.commit()

def update_result_03(result):
    conn,cursor=mysql_conn()
    sql_update="update yms_tmall_phone_addr_temp set " \
               "source_detail_3=%s,source_href_3=%s,source_city_3=%s,source_name_3=%s where company_name=%s"
    cursor.execute(sql_update,result)
    conn.commit()

def update_result_04(result):
    conn,cursor=mysql_conn()
    sql_update="update yms_tmall_phone_addr_temp set " \
               "source_detail_4=%s,source_href_4=%s,source_city_4=%s,source_name_4=%s where company_name=%s"
    cursor.execute(sql_update,result)
    conn.commit()

def update_result_05(result):
    conn,cursor=mysql_conn()
    sql_update="update yms_tmall_phone_addr_temp set " \
               "source_detail_5=%s,source_href_5=%s,source_city_5=%s,source_name_5=%s where company_name=%s"
    cursor.execute(sql_update,result)
    conn.commit()

def update_result_06(result):
    conn,cursor=mysql_conn()
    sql_update="update yms_tmall_phone_addr_temp set " \
               "source_detail_6=%s,source_href_6=%s,source_city_6=%s,source_name_6=%s where company_name=%s"
    cursor.execute(sql_update,result)
    conn.commit()

def update_result_07(result):
    conn,cursor=mysql_conn()
    sql_update="update yms_tmall_phone_addr_temp set " \
               "source_detail_7=%s,source_href_7=%s,source_city_7=%s,source_name_7=%s where company_name=%s"
    cursor.execute(sql_update,result)
    conn.commit()

def update_result_08(result):
    conn,cursor=mysql_conn()
    sql_update="update yms_tmall_phone_addr_temp set " \
               "source_detail_8=%s,source_href_8=%s,source_city_8=%s,source_name_8=%s where company_name=%s"
    cursor.execute(sql_update,result)
    conn.commit()

def update_result_09(result):
    conn,cursor=mysql_conn()
    sql_update="update yms_tmall_phone_addr_temp set " \
               "source_detail_9=%s,source_href_9=%s,source_city_9=%s,source_name_9=%s where company_name=%s"
    cursor.execute(sql_update,result)
    conn.commit()

def update_result_10(result):
    conn,cursor=mysql_conn()
    sql_update="update yms_tmall_phone_addr_temp set " \
               "source_detail_10=%s,source_href_10=%s,source_city_10=%s,source_name_10=%s where company_name=%s"
    cursor.execute(sql_update,result)
    conn.commit()

def update_result_spider_time(result):
    conn,cursor=mysql_conn()
    sql_update='update yms_tmall_phone_addr_temp set spider_time=%s where company_name=%s'
    cursor.execute(sql_update,result)
    conn.commit()

if __name__=='__main__':
    execute_counter=0
    # update_database()
    update_operator={'U_1':update_result_01,
                     'U_2':update_result_02,
                     'U_3':update_result_03,
                     'U_4':update_result_04,
                     'U_5':update_result_05,
                     'U_6':update_result_06,
                     'U_7':update_result_07,
                     'U_8':update_result_08,
                     'U_9':update_result_09,
                     'U_10':update_result_10,}
    driver_temp=''
    keyword_temp=get_record()
    while keyword_temp:
        # 每隔1000次刷新数据据
        # if execute_counter%1000==0:
        #     update_database()
        # else:
        #     pass
        try:
            if execute_counter==0:
                keyword_temp=get_record()
                driver=web_site(keyword=keyword_temp)
                frame=get_frame(driver)[1:]
            else:
                driver=web_site(send_driver=driver_temp,keyword=keyword_temp)
                frame=get_frame(driver_temp)[1:]
            result=[get_result(frame=item) for item in frame]
            if result:
                for i in range(len(result)):
                    result_temp=[result[i][2],
                                 result[i][3],
                                 result[i][4],
                                 result[i][5],
                                 keyword_temp[0]]
                    update_operator['U_'+str(i+1)](result_temp)
                result_spider_time=[time.strftime('%Y-%m-%d %X',time.localtime()),keyword_temp]
                update_result_spider_time(result_spider_time)
                print(u'成功添加 '+keyword_temp[0]+u' 公司的信息，总计有 '+str(len(result))+u' 条信息源。')
        except:
            print(u'没有找到 '+keyword_temp[0]+u' 公司的信息。')
            result=[time.strftime('%Y-%m-%d %X',time.localtime()),keyword_temp]
            update_result_spider_time(result)
        finally:
            keyword_temp=get_record()
            execute_counter+=1
            time.sleep(1)
            driver_temp=driver
            if execute_counter%103==0 or driver.title==u'搜狗——请输入验证码':
                # time.sleep(abs(random.gauss(500,100)))
                driver_temp.quit()
                driver_temp=''
            else:pass
        # time.sleep(abs(random.gauss(3,2)))

# create table yms_tmall_phone_addr_temp (id int,company_name varchar(200),spider_time varchar(100),source_detail_1 varchar(200),source_href_1 varchar(200),source_city_1 varchar(200),source_name_1 varchar(200))
