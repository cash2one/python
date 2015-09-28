#coding:utf-8
__author__ = '613108'
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import pymysql

#数据库链接
conn=pymysql.connect(host='localhost',
                     user='root',
                     passwd='',
                     db='tmall_info',
                     charset='utf8')
cursor=conn.cursor()

#搜索关键词
def get_firstLevel_keyword(url='http://www.tmall.com',\
                           css_setor='.j_MenuNav.menu-nav'):
    driver=webdriver.PhantomJS()
    driver.get(url)
    key_word=driver.find_elements_by_css_selector(css_setor)
    kw_1=[]
    kw_0=[]    
    for item in key_word:
        kw_1_temp=[]
        kw_0_temp=[]
        kw=item.find_elements_by_tag_name('a')
        for kw_find in kw:
            kw_1_temp.append(kw_find.text)
        kw_1.append(kw_1_temp)
        kw_0_temp="/".join(kw_1_temp)
        kw_0.append(kw_0_temp)
    driver.close()
    driver.quit()
    return kw_0,kw_1

if __name__=='__main__':
    tt=get_firstLevel_keyword()
    tt=list(tt)
    tt_1=[x for x in tt[0] if x]
    tt_2=[[tt[0][i],tt[1][i][z]] for i in range(len(tt[0])) for z in range(len(tt[1][i]))]
    for item in tt_2:
        sql="insert into yms_tmall_firstkeyword" \
        "(keyword_discribe, keyword_detail)" \
        "values('%s','%s');"%(item[0],item[1])
        cursor.execute(sql)
    conn.commit()
