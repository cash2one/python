#coding:utf-8
__author__ = '613108'
from bs4 import BeautifulSoup
import os

# with open(r'd:/spider/aliexpress/url_list_2015-08-05.txt','r') as txtfile:
#     result_for_soup=txtfile.read()
#     result_for_soup=result_for_soup.split(',')
#     for item in result_for_soup:
#         print(item)
# soup=BeautifulSoup(result_for_soup)
# frames=soup.find_all(attrs={'class':'list-item'})
# print(len(frames))
#
# os.remove(r'd:/spider/2015-08-050.txt')
#
# url='http://www.aliexpress.com/wholesale?SearchText=PlayStation&needQuery=n&shipCountry=RU&site=glo&page=6'
# result='1'
# file_name='D:/spider/aliexpress/src/'+url.split('?')[-1]+'.txt'
# with open(file_name,'wb') as txt_file:
#     txt_file.writelines(result)

path='d:/spider/aliexpress/src'
filelist=os.listdir(path)
for item in filelist:
    file_name='d:/spider/aliexpress/src/'+item
    with open(file_name,'r') as txt_file:
        temp=txt_file.read()
    soup=BeautifulSoup(temp)
    frames=soup.find_all(attrs={'class':'list-item'})
    for item in frames:
        sec_frame=item.find(attrs={'class':'detail'})
        title=sec_frame.h3.a['title']
        href=sec_frame.h3.a['href']
        try:judge_href=sec_frame.find(attrs={'class':'score-dot'})['href']
        except:judge_href='-'
        store_title=sec_frame.find(attrs={'class':'store'})['title']
        store_href=sec_frame.find(attrs={'class':'store'})['href']
        try:is_top_rate_seller=sec_frame.find(attrs={'class':'top-rated-seller'}).contents[0]
        except:is_top_rate_seller='NO'
        thr_frame=item.find(attrs={'class':'info infoprice'})
        price=thr_frame.span.span.contents[0]
        price_unit=thr_frame.span.find_all('span')[-1].text
        try:del_price=thr_frame.find(attrs={'class':'original-price'}).contents[0]
        except:del_price='-'
        try:shipping_service=thr_frame.strong.contents[0]
        except:shipping_service='-'
        try:
            product_rate=thr_frame.find(itemprop="ratingValue").contents[0]
            feedback=thr_frame.find(attrs={'class':'rate-num'}).contents[0]
        except:product_rate='-';feedback='-'
        orders=thr_frame.find(title="Total Orders").contents[0]
        result=[title,href,judge_href,store_title,is_top_rate_seller,store_href,price,price_unit,
                del_price,shipping_service,product_rate,feedback,orders]
        print('='*80)
        for item in result:
            print(item)
    os.curdir(file_name)