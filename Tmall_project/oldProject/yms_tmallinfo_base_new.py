# coding:utf-8
__author__ = 'Mingsong_Yang'
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import pymysql
import time

# 取关键词（二级关键词）
def get_keyword():
    sql_select = 'select keyword_detail from tmall_secondkeyword where staus=0 limit 0,1'
    conn = pymysql.connect(host='10.118.187.5', user='root', passwd='root', charset='utf8', db='elec_platform')
    cursor = conn.cursor()
    cursor.execute(sql_select)
    keyword = cursor.fetchone()
    return keyword, cursor, conn


# 判断是否已爬取
def is_exist_shop():
    d = {}
    sql_select = 'select distinct href from yms_tmall_shopinfo_new'
    conn = pymysql.connect(host='10.118.187.5', user='root', passwd='root', charset='utf8', db='elec_platform')
    cursor = conn.cursor()
    cursor.execute(sql_select)
    shop_href = cursor.fetchall()
    for item in shop_href:
        d[item[0]] = 1
    return d


# 关键词状态更新
def keyword_staus_update(keyword, cursor, conn):
    sql_update = "update tmall_secondkeyword set staus=1 where keyword_detail=%s;"
    cursor.execute(sql_update, keyword)
    conn.commit()


# 搜索店铺
def shop_search(send_driver='', url='http://s.taobao.com/', keyword=u'笔记本'):
    if send_driver:
        driver = send_driver
    else:
        driver = webdriver.Firefox()
        # driver=webdriver.Chrome()
        # driver=webdriver.PhantomJS()
    driver.get(url)
    driver.find_element_by_link_text(u'店铺').click()
    driver.find_element_by_css_selector('#q').clear()
    driver.find_element_by_css_selector('#q').send_keys(keyword)
    try:
        driver.find_element_by_css_selector('.btn-search').click()
    except:
        pass
    return driver


# 页面信息设置并返回翻页总数
def page_setting(driver):
    driver = driver
    move_element = driver.find_element_by_css_selector('div.hover-menu.J_Selector:nth-child(4)')
    ActionChains(driver).move_to_element(move_element).perform()
    driver.implicitly_wait(2)
    driver.find_element_by_link_text('天猫(商城)').click()
    page_count = driver.find_element_by_css_selector('.page-info').text[2:]
    page_count = int(page_count)
    return driver, page_count


# 数据插入数据库
def data_insert(data, cursor, conn):
    sql_insert = 'insert into yms_tmall_shopinfo_new (' \
                 'name,href,judgepage_href,seller,addr,brand,monthsale,productsum,dsr_desc_mark,' \
                 'dsr_desc_avg,dsr_service_mark,dsr_service_avg,dsr_sending_mark,dsr_sending_avg,' \
                 'product_link_1,price_1,product_link_2,price_2,product_link_3,price_3,product_link_4,price_4,spider_time) ' \
                 'values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
    cursor.execute(sql_insert, data)
    conn.commit()


# 单页店铺信息获取
def get_shop_info(driver):
    driver = driver
    driver.maximize_window()
    driver.implicitly_wait(10)
    page_all_shop = driver.find_elements_by_css_selector('.list-item')
    shop_data = []
    d = is_exist_shop()
    print(u'已收集 ' + str(len(d)) + u' 家天猫店铺信息')
    scroll_counter = 0
    scroll_step = 5000 / len(page_all_shop)
    if page_all_shop:
        for one_shop in page_all_shop:
            # 页面滚动加载
            js_scroll = 'var q=document.documentElement.scrollTop=%s' % scroll_counter
            driver.execute_script(js_scroll)
            scroll_counter += scroll_step
            # 因做去重操作，查找速度太快，可能出现网页加载较慢的情况，故添加此try操作
            try:
                name = one_shop.find_element_by_css_selector('.shop-name.J_shop_name').text.strip()
            except:
                continue
            href = one_shop.find_element_by_css_selector('.list-img>a').get_attribute('href').split('?')[0]
            if href in d.keys():
                print(name + u'--已经存在，不再添加--')
                continue
            seller = one_shop.find_element_by_css_selector('.shop-info-list>a').text.strip()
            addr = one_shop.find_element_by_css_selector('.shop-address').text.strip()
            brand = one_shop.find_element_by_css_selector('.main-cat>a').text.strip()
            monthsale = one_shop.find_element_by_css_selector('.info-sale>em').text
            productsum = one_shop.find_element_by_css_selector('.info-sum>em').text
            move_element = one_shop.find_element_by_css_selector('.descr-icon')
            ActionChains(driver).move_to_element(move_element).perform()
            dsr_desc_mark = one_shop.find_element_by_css_selector('div.shop-mark li:nth-child(2) a').text
            judgePage_href = one_shop.find_element_by_css_selector('div.shop-mark li:nth-child(2) a').get_attribute(
                'href')
            dsr_service_mark = one_shop.find_element_by_css_selector('div.shop-mark li:nth-child(3) a').text
            dsr_sending_mark = one_shop.find_element_by_css_selector('div.shop-mark li:nth-child(4) a').text
            if one_shop.find_element_by_css_selector('div.shop-avg li:nth-child(2) span').get_attribute(
                    'class') == 'lessthan':
                dsr_desc_avg = '-' + one_shop.find_element_by_css_selector('div.shop-avg li:nth-child(2) span').text[2:]
            else:
                dsr_desc_avg = one_shop.find_element_by_css_selector('div.shop-avg li:nth-child(2) span').text[2:]
            if one_shop.find_element_by_css_selector('div.shop-avg li:nth-child(3) span').get_attribute(
                    'class') == 'lessthan':
                dsr_service_avg = '-' + one_shop.find_element_by_css_selector('div.shop-avg li:nth-child(3) span').text[
                                        2:]
            else:
                dsr_service_avg = one_shop.find_element_by_css_selector('div.shop-avg li:nth-child(3) span').text[2:]
            if one_shop.find_element_by_css_selector('div.shop-avg li:nth-child(4) span').get_attribute(
                    'class') == 'lessthan':
                dsr_sending_avg = '-' + one_shop.find_element_by_css_selector('div.shop-avg li:nth-child(4) span').text[
                                        2:]
            else:
                dsr_sending_avg = one_shop.find_element_by_css_selector('div.shop-avg li:nth-child(4) span').text[2:]
            # 添加商品信息
            product_links = one_shop.find_elements_by_css_selector('ul li:nth-child(3) div.one-product')
            try:
                if product_links:
                    for i in range(len(product_links)):
                        names = globals()
                        names['product_link_' + str(i + 1)] = product_links[i].find_element_by_css_selector(
                            '.product-img a').get_attribute('href')
                        names['price_' + str(i + 1)] = product_links[i].find_element_by_css_selector(
                            '.price-wrap span:nth-child(3)').text
                else:
                    for i in range(4):
                        names = globals()
                        names['product_link_' + str(i + 1)] = '-'
                        names['price_' + str(i + 1)] = '-'
            except:
                pass
            spider_time = time.strftime("%Y-%m-%d %X", time.localtime())
            shop_data_temp = [name, href, judgePage_href, seller, addr, brand, monthsale,
                              productsum, dsr_desc_mark, dsr_desc_avg, dsr_service_mark, dsr_service_avg,
                              dsr_sending_mark, dsr_sending_avg,
                              product_link_1, price_1, product_link_2, price_2, product_link_3, price_3, product_link_4,
                              price_4, spider_time]
            shop_data.append(shop_data_temp)
    return shop_data, driver


# 翻页
def page_turn(driver):
    driver.find_element_by_css_selector('.page-next').click()
    return driver

# 主调用
if __name__ == '__main__':
    get_keyword_t = get_keyword()
    execute_count = 0
    send_driver_t = ''
    while get_keyword_t[0]:
        if execute_count:
            shop_search_t = shop_search(send_driver=send_driver_t, keyword=get_keyword_t[0])
        else:
            shop_search_t = shop_search(keyword=get_keyword_t[0])
        print(u'本轮搜索关键词为：' + get_keyword_t[0][0])
        driver = shop_search_t
        if u'店铺' in driver.title:
            page_setting_t = page_setting(shop_search_t)
        else:
            continue
        counter = 0
        driver = page_setting_t[0]
        while counter < page_setting_t[1]:
            get_shop_info_t = get_shop_info(driver)
            cursor = get_keyword_t[1]
            conn = get_keyword_t[2]
            data = get_shop_info_t[0]
            for item in data:
                data_insert(item, cursor, conn)
            conn.commit()
            counter += 1
            while counter < page_setting_t[1]:
                driver = page_turn(get_shop_info_t[1])
                break
        send_driver_t = driver
        keyword_staus_update(get_keyword_t[0][0], get_keyword_t[1], get_keyword_t[2])
        get_keyword_t = get_keyword()
        execute_count += 1
