# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 15:06:18 2015

@author: 575760
"""

from selenium import webdriver
import re, time, urllib2
import MySQLdb, random
# url='https://list.tmall.com/search_product.htm?cat=50043479&brand=3716206&s=60&q=%CB%AE%D6%AE%C3%DC%D3%EF&sort=s&style=g&from=.detail.pc_1_searchbutton&active=2'
# url='https://list.tmall.com/search_product.htm?s=0&q=%CB%AE%D6%AE%C3%DC%D3%EF'
def tmall_search(keyword='水之密语', s=0):
    driver = webdriver.PhantomJS()
    # driver = webdriver.Chrome()
    KK = urllib2.quote(keyword.encode('GBK'))
    url = 'https://list.tmall.com/search_product.htm?s=' + str(s) + '&q=' + str(KK)
    print url
    driver.get(url)

    tmp1 = driver.find_elements_by_xpath('//p[@class="productPrice"]//em')
    p_price = [re.sub(u'¥|\u00a5', '', x.text) for x in tmp1]
    tmp2 = driver.find_elements_by_xpath('//p[@class="productTitle"]//a')
    p_title = [x.text for x in tmp2]
    if len(p_title) == 0:
        tmp2 = driver.find_elements_by_xpath('//div[@class="productTitle productTitle-spu"]//a')
        p_title = [x.text for x in tmp2]

    p_href = [x.get_attribute('href') for x in tmp2]
    p_href = [x.split('&')[0] for x in p_href]

    tmp3 = driver.find_elements_by_xpath('//div[@class="productShop"]//a[@class="productShop-name"]')
    p_shop = [x.text for x in tmp3]

    tmp4 = driver.find_elements_by_xpath('//p[@class="productStatus"]//em')
    p_sale = [re.sub(u'\u7b14', '', x.text) for x in tmp4]

    crawl_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    # keys=[]
    # [keys.append(keyword) for i in range(0,len(p_sale))]

    driver.close()
    driver.quit()
    # ct=[]
    # [ct.append(crawl_time) for i in range(0,len(p_sale))]
    return p_title, p_href, p_price, p_shop, p_sale, keyword, crawl_time


def app_run():
    conn = MySQLdb.connect(host="10.118.187.12", user="admin", passwd="admin", db="elec_platform", charset="utf8")

    cursor = conn.cursor()
    sql = "insert into tmall_product_apple(p_title,p_href,p_price,p_shop,p_sale,\
         keyword,crawl_time) values(%s,%s,%s,%s,%s,%s,%s)"
    # keys=['水之密语','水之印','惠润','丝蓓绮','芭比布朗','海蓝之谜','倩碧','娇兰佳人']
    # keys=['年轻水','玉兰油','倩碧','娇兰佳人']
    keys = [u'苹果手机','iphone','ipad','mac','apple']

    for pg in range(0, 10):
        for key in keys:
            try:
                tmp = tmall_search(keyword=key, s=pg * 60)
                print(tmp)
                n = len(tmp[0])
                for i in range(0, n):
                    try:
                        V = (tmp[0][i], tmp[1][i], tmp[2][i], tmp[3][i], tmp[4][i], key.encode('utf8','ignore'), tmp[6])
                        try:
                            cursor.execute(sql, V)
                            conn.commit()
                        except MySQLdb.Error, e:
                            print e
                    except:pass
            except:pass
            time.sleep(abs(random.gauss(25, 5)))
    cursor.close()
    conn.close()


if __name__ == "__main__":
    app_run()
