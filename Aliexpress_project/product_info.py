#coding:utf-8
__author__ = 'Administrator'

import sys,time,urllib,urllib2,socket,os,random,gc
socket.setdefaulttimeout(120)
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append(r'C:\Users\613108\Desktop\Project\tool_self')
import my_proxy,soup_proxy,list_split,My_Csv
from Queue import Queue
from selenium import webdriver
from bs4 import BeautifulSoup
from threading import Thread
from selenium.webdriver.common.proxy import *

# proxy_port=my_proxy.is_proxy_exists()
# queue_for_proxy=Queue(0)
# for item in proxy_port:
#     queue_for_proxy.put(item)
queue_keyword=Queue(0)
queue_kw_pc=Queue(0)
queue_for_target=Queue(0)
queue_for_result=Queue(0)
keyword=[]
keyword_fail=[]

class Get_KeyWord(object):
    def __init__(self,url='http://www.aliexpress.com'):
        self.url=url

    def get_keyword(self):
        k_w=[]
        driver=webdriver.PhantomJS()
        driver.maximize_window()
        driver.get(self.url)
        src=driver.page_source
        soup=BeautifulSoup(src)
        framess=soup.find_all(attrs={'class':'sub-cate-items'})
        for item in framess:
            temp=item.dd
            keywords=temp.find_all('a')
            for x in keywords:
                k_w.append(x.contents[0])
        driver.quit()
        k_w=set(k_w)
        for item in k_w:
            queue_keyword.put(item)
            print(item)
        return k_w

class Gen_url(object):
    # 生成待抓取网址
    def gen_url(self):
        Get_Pagecount_thread=[]
        url_list=[]
        # 开启20个线和获取页面总数
        for i in range(35):
            Get_Pagecount_thread.append(self.Get_Pagecount())
        for item in Get_Pagecount_thread:
            item.start()
        for item in Get_Pagecount_thread:
            item.join()
        print(queue_kw_pc.qsize())
        for i in range(queue_kw_pc.qsize()):
            keyword_pagecount=queue_kw_pc.get()
            keyword=keyword_pagecount[0]
            pagecount=int(keyword_pagecount[1])
            if pagecount:
                for i in range(pagecount):
                    temp={'site':'glo','shipCountry':'RU','SearchText':keyword,'needQuery':'n','page':i+1}
                    url='http://www.aliexpress.com/wholesale?'+urllib.urlencode(temp)
                    url_list.append(url)
        txt_src=','.join(url_list)
        file_name=r'd:/spider/aliexpress/url_list_'+str(time.strftime('%Y-%m-%d'))+'.txt'
        with open(file_name,'wb') as txt_file:
            txt_file.write(txt_src)
        return url_list

    # 内部类，获取各个keyword包含页面总数
    class Get_Pagecount(Thread):
        def __init__(self):
            Thread.__init__(self)

        def get_pagecount(self):
            while True:
                try:
                    keyword=queue_keyword.get(timeout=2)
                    try:
                        temp={'site':'glo','shipCountry':'RU','SearchText':keyword,'needQuery':'n','page':1}
                        url='http://www.aliexpress.com/wholesale?'+urllib.urlencode(temp)
                        res=urllib2.urlopen(url)
                        soup=BeautifulSoup(res,from_encoding='utf-8')
                        res.close()
                        page_count=soup.find(id='pagination-max').contents[0]
                    except AttributeError:
                        page_count=1
                    except:
                        keyword_fail.append(keyword)
                        page_count=0
                    queue_kw_pc.put([keyword,page_count])
                    print([keyword,page_count])
                except:
                    break

        def run(self):
            self.get_pagecount()

class Get_src(Thread):
    def __init__(self,url_list):
        Thread.__init__(self)
        self.url_list=url_list

    def use_proxy(self):
        proxy_port=my_proxy.is_proxy_exists()
        return proxy_port

    def put_urllist_2_queue(self):
        for url in self.url_list:
            queue_for_target.put(url)

    def get_info(self,use_proxy=0):
        self.put_urllist_2_queue()
        if use_proxy:
            proxy_port=self.use_proxy()
            proxy=random.sample(proxy_port,1)[0]
            proxy=proxy[0]+':'+proxy[1]
            print(proxy)
            proxy=Proxy({'proxyType':ProxyType.MANUAL,'httpProxy':proxy,'ftpProxy':proxy,'sslProxy':proxy,'noProxy':''})
            driver=webdriver.Firefox(proxy=proxy)
            driver.maximize_window()
            while True:
                url=queue_for_target.get(timeout=1)
                driver.get(url)
                result=driver.page_source
                file_name=r'd:/spider/aliexpress/src/'+url.split('?')[-1]+'.txt'
                with open(file_name,'wb') as txt_file:
                    txt_file.writelines(result)
        else:
            driver=webdriver.PhantomJS()
            # driver=webdriver.Chrome()
            driver.maximize_window()
            while True:
                for i in range(100):
                    url=queue_for_target.get(timeout=1)
                    print(url)
                    try:
                        driver.get(url)
                        result=driver.page_source
                        # print(result.encode('gbk','ignore'))
                        file_name=r'd:/spider/aliexpress/src/'+url.split('?')[-1]+'.txt'
                        with open(file_name,'wb') as txt_file:
                            txt_file.writelines(result)
                        print('Okay!')
                    except:
                        print('Failed!')
                        queue_for_target.put(url)
                driver.close()
                driver.quit()
                print('*'*15+u'关闭PhantomJS,释放内存'+'*'*15)
                driver=webdriver.PhantomJS()
                time.sleep(abs(random.gauss(5,3)))

    def run(self):
        self.get_info()

class Get_info(Thread):
    def __init__(self,file_list):
        Thread.__init__(self)
        self.file_list=file_list

    def get_info(self):
        # path='d:/spider/aliexpress/src'
        # filelist=os.listdir(path)
        for item in self.file_list:
            try:
                file_name='d:/spider/aliexpress/src/'+item
                print(item)
                with open(file_name,'r') as txt_file:
                    temp=txt_file.read()
                soup=BeautifulSoup(temp)
                frames=soup.find_all(attrs={'class':'list-item'})
                soup=''
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
                    # for item in result:
                    #     print(item)
                    queue_for_result.put(result)
                print('='*80)
            except:
                print('*'*20+u'程序出错，已经跳过'+'*'*20)
                continue
            # os.remove(file_name)

    def run(self):
        self.get_info()

# 代码组织
def url_for_spider():
    file_name=r'd:/spider/aliexpress/url_list_'+str(time.strftime('%Y-%m-%d'))+'.txt'
    if os.path.exists(file_name):
        with open(file_name,'r') as txt_file:
            url_list=txt_file.read()
            url_list=url_list.split(',')
    else:
        Get_KeyWord().get_keyword()
        url_list=Gen_url().gen_url()
    return url_list

def save_data():
    data_result=[]
    title_temp=['title','href','judge_href','store_title','is_top_rate_seller','store_href','price','price_unit',
                'del_price','shipping_service','product_rate','feedback','orders']
    for i in range(queue_for_result.qsize()):
        data_result.append(queue_for_result.get())
    writer=My_Csv.Write_Csv(path='d:/spider/aliexpress',name='aliexpress_shopinfo',title=title_temp,result=data_result)
    writer.add_title_data()

if __name__=='__main__':
    # url_list=url_for_spider()
    # had_get_url_list=os.listdir('d:/spider/aliexpress/src')
    # had_get_url_list=['http://www.aliexpress.com/wholesale?'+item.split('.txt')[0] for item in had_get_url_list]
    # url_list=[item for item in url_list if item not in had_get_url_list]
    #
    # Get_src_thread=[]
    # url_list=list_split.list_split(url_list,25)
    # for item in url_list:
    #     Get_src_thread.append(Get_src(item))
    # for item in Get_src_thread:
    #     item.start()
    # for item in Get_src_thread:
    #     item.join()

    original_file_list=os.listdir('d:/spider/aliexpress/src')
    file_list_1=list_split.list_split(original_file_list,600)
    i=0
    for temp in file_list_1:
        i+=1
        print('*'*15+'ROUND '+str(i)+'*'*15)
        file_list=list_split.list_split(temp,30)
        Get_info_thread=[]
        for item in file_list:
            Get_info_thread.append(Get_info(item))
        for item in Get_info_thread:
            item.start()
        for item in Get_info_thread:
            item.join()
        save_data()

        print('+'*15+u'文件'+str(i)+u'已保存！'+'*'*15)

        for item in Get_info_thread:
            print(item.is_alive)

    # data_result=[]
    # title_temp=['title','href','judge_href','store_title','is_top_rate_seller','store_href','price','price_unit',
    #             'del_price','shipping_service','product_rate','feedback','orders']
    # for i in range(queue_for_result.qsize()):
    #     data_result.append(queue_for_result.get())
    # writer=My_Csv.Write_Csv(path='d:/spider/aliexpress',name='aliexpress_shopinfo',title=title_temp,result=data_result)
    # writer.add_title_data()

    print('*'*15+u'程序运行完毕，请检查数据'+'*'*15)