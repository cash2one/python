#coding:utf-8
__author__ = '613108'

import urllib2,cStringIO,gzip,cookielib,os,time,random,sys,csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import *
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append(r'C:\Users\613108\Desktop\Project\tool_self')
import My_Csv

def get_shoppage():
    send_headers = { 'Referer':'www.youdaili.net',
                     'User-Agent':'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
                     'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                     'Connection':'keep-alive'}
    cookie=cookielib.CookieJar()
    openner=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    url_t1='https://list.tmall.com/search_product.htm?spm=a220m.1000858.1000724.10&cat=50024400&s='
    url_t2='&sort=s&style=w&search_condition=50&from=sn_1_brand-qp&active=1&shopType=any&industryCatId=50024400&tmhkmain=0&type=pc'
    fail_num=[]
    # for i in range(30):
    for i in [8]:
        temp=url_t1+str((i-1)*20)+url_t2
        file_name=u'd:/spider/tmall_cellphone/第%s页.txt'%(i+1)
        Request=urllib2.Request(url=temp,headers=send_headers)
        try:
            result=openner.open(Request)
            result=result.read()
        except urllib2.HTTPError,e:
            print(e.code)
            fail_num.append(i+1)
            continue
        except urllib2.URLError,e:
            print(e.reason)
            fail_num.append(i+1)
            continue
        except:
            fail_num.append(i+1)
            continue
        try:
            # gzip格式处
            data=cStringIO.StringIO(result)
            gz=gzip.GzipFile(fileobj=data)
            result=gz.read()
            gz.close()
        except:pass
        with open(file_name,'wb') as txt:
            txt.writelines(result)
    print(fail_num)

def get_shop_producthref():
    path=r'd:/spider/tmall_cellphone'
    file_list=os.listdir(path)
    result=[]
    # 部分店铺没有“更多产品”之连接，直接取当前页面的产品销售数据
    result_product=[]
    for item in file_list:
        file_name=path+'/'+item
        if os.path.isdir(file_name):continue
        else:
            with open(file_name,'r') as txt_file:
                contents=txt_file.read()
                soup=BeautifulSoup(contents)
                frames=soup.find_all(attrs={'class':'shopBox'})
                # if frames:
                for item in frames:
                    shop_name=item.find(attrs={'class':'shopHeader-info'}).a.text
                    result_temp=[]
                    try:
                        href='http://list.tmall.com/'+item.find(attrs={'class':'sBr-more'}).a['href']
                    except:
                        href=''
                        products=item.find_all(attrs={'class':'product'})
                        for tt in products:
                            p_title=tt.find(attrs={'class':'productTitle'}).a.text
                            p_price=tt.find(attrs={'class':'productPrice'}).em.text[1:]
                            try:p_sale=tt.find(attrs={'class':'productStatus'}).span.em.text[:-1]
                            except:p_sale='-'
                            ttt=[shop_name,p_title,p_price,p_sale]
                            result_product.append(ttt)
                    if href:
                        result.append([shop_name,href])
    title=['shop_title','p_title','p_price','p_sale']
    writer=My_Csv.Write_Csv(path='d:/spider/tmall_cellphone',name='result_01',title=title,result=result_product)
    writer.add_title_data()
    # return result,result_product

def get_productinfo_src(url_list):
    driver=webdriver.Chrome()
    driver.maximize_window()
    i=1
    for url in url_list:
        driver.get(url)
        time.sleep(abs(random.gauss(10,3)))
        try:
            page_len=int(driver.find_element_by_css_selector('.ui-page-s-len').text.split('/')[1])
        except NoSuchElementException,e:
            time.sleep(60)
            driver.get(url)
            page_len=int(driver.find_element_by_css_selector('.ui-page-s-len').text.split('/')[1])
        except:continue
        print(page_len)
        for i in range(page_len):
            source=driver.page_source
            url=driver.current_url
            file_name='d:/spider/tmall_cellphone/src/'+url.split('?')[1]+'.txt'
            with open(file_name,'wb') as txt_file:
                txt_file.write(source)
            if i<page_len-1:
                driver.find_element_by_css_selector('.ui-page-s-next').click()
                time.sleep(abs(random.gauss(5,3)))
                print(url)
                print(u'下一页')
        i+=1
    driver.close()
    driver.quit()

# def get_pagesource():
#     proxy_list=[]
#     file_name=str(time.strftime('%Y-%m-%d'))
#     file_name='d:/spider/proxy/proxy_'+file_name+'.csv'
#     with open(file_name) as proxy_csv:
#         reader=csv.reader(proxy_csv)
#         for line in reader:
#             if line[0]=='ip':
#                 continue
#             else:
#                 proxy_list.append([line[0],line[1]])
#     cookies=cookielib.CookieJar
#     proxy=['61.184.192.42','80']
#     proxyHandler=urllib2.ProxyHandler({'http':r'http://%s:%s'%(proxy[0],proxy[1])})
#     openner=urllib2.build_opener(proxyHandler)
#     send_headers = { 'Referer':'www.youdaili.net',
#                      'User-Agent':'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
#                      'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#                      'Connection':'keep-alive'}
#     request=urllib2.Request(url='https://list.tmall.com/search_shopitem.htm?user_id=711383144&q=&sort=s&cat=50024400&from=_1_&is=p&smToken=4bcfff488f3e42dfb7b4c22c9f523791&smSign=bznm8t6fLkWnp4IzHxEONg%3D%3D',headers=send_headers)
#     result=openner.open(request)
#     result=result.read()
#     print(result)

def get_info_detail():
    path='d:/spider/tmall_cellphone/src'
    file_list=os.listdir(path)
    file_list=[path+'/'+item for item in file_list]
    result=[]
    for item in file_list:
        with open(item,'r') as src_file:
            src=src_file.read()
        soup=BeautifulSoup(src)
        frames=soup.find_all(attrs={'class':'product'})
        if len(frames):
            shop_title=soup.find(attrs={'class':'shopHeader-info'}).a.contents[0]
            print(shop_title)
            print(item)
            for temp in frames:
                p_title=temp.find(attrs={'class':'productTitle'}).a.text
                p_price=temp.find(attrs={'class':'productPrice'}).em.text[1:]
                try:p_sale=temp.find(attrs={'class':'productStatus'}).span.em.text[:-1]
                except:p_sale='-'
                result_product=[shop_title,p_title,p_price,p_sale]
                result.append(result_product)
    title=['shop_title','p_title','p_price','p_sale']
    writer=My_Csv.Write_Csv(path='d:/spider/tmall_cellphone',name='result_02',title=title,result=result)
    writer.add_title_data()

if __name__=='__main__':
    get_shop_producthref()
    # get_shoppage()
    # url_list=get_shop_producthref()[0]
    # url_list=[item[1] for item in url_list]
    # 提取已爬网址
    # url_list_temp=os.listdir('d:/spider/tmall_cellphone/src')
    # url_list_temp=[item.split('.txt')[0] for item in url_list_temp]
    # 去除已爬网址
    # url_list=[item for item in url_list if item.split('?')[1] not in url_list_temp]
    # get_productinfo_src(url_list)
    # get_pagesource()

    # get_info_detail()