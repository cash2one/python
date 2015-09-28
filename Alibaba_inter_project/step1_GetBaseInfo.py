#coding:utf-8
__author__ = '613108'

import urllib2,os,sys
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
from threading import Thread
from Queue import Queue
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append(r'C:\Users\613108\Desktop\Project\tool_self')
import My_Csv

# 网址生成类
class Gen_url():
    def __init__(self,keyword_list):
        self.keyword_list=keyword_list

    def get_pagecount(self):
        d={}
        for keyword in self.keyword_list:
            url='http://www.alibaba.com/corporations/'+keyword+'/--------------------50.html'
            send_headers = {'Referer':'www.alibaba.com',
                            'User-Agent':'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
                            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                            'Connection':'keep-alive'}
            req=urllib2.Request(url=url,headers=send_headers)
            res=urllib2.urlopen(req)
            result=res.read()
            res.close()
            soup=BeautifulSoup(result)
            try:page_count=int(soup.find_all('span',attrs={'class':'disable'})[1].contents[0])
            except IndexError,e:
                print(e.message)
                page_count=''
            except:page_count=''
            if page_count:
                d[keyword]=page_count
            print(page_count)
        return d

    def gen_url(self):
        url_list=[]
        d=self.get_pagecount()
        for item in d.items():
            keyword=item[0]
            page_count=item[1]
            for i in range(page_count):
                url_temp='http://www.alibaba.com/corporations/'+keyword+'/--------------------50/'+str(i+1)+'.html'
                url_list.append(url_temp)
        return url_list

# 获取源码类
class Get_Src(Thread):
    def __init__(self,url_list):
        Thread.__init__(self)
        self.url_list=url_list

    def get_src(self):
        for url in self.url_list:
            send_headers = {'Referer':'www.alibaba.com',
                            'User-Agent':'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
                            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                            'Connection':'keep-alive'}
            req=urllib2.Request(url=url,headers=send_headers)
            try:
                res=urllib2.urlopen(req)
                result=res.read()
                res.close()
                # 测试请求返回源码
                # soup=BeautifulSoup(result)
                # frames=soup.find_all('div',attrs={'class':'f-icon','data-spm':'35'})
                temp=url.split('/')
                file_name=temp[-3]+'_'+temp[-2]+'_'+temp[-1].split('.')[0]+'.txt'
                # 配置文件保存地址
                path='d:/spider/alibaba_inter/src'
                with open(path+'/'+file_name,'wb') as txt_file:
                    txt_file.write(result)
            except urllib2.HTTPError,e:print(e.code)
            except urllib2.URLError,e:print(e.reason)
            except:continue

    def run(self):
        self.get_src()

# 解释源码类,传入文件路径
# 使用beautifulsoup
class Analysis_src(Thread):
    def __init__(self,file_list):
        Thread.__init__(self)
        self.file_list=file_list

    def analysis(self):
        for item in self.file_list:
            with open(item,'r') as txt_file:
                res=txt_file.read()
            soup=BeautifulSoup(res)
            frames=soup.find_all('div',attrs={'class':'f-icon','data-spm':'35'})
            for temp in frames:
                com_name=temp.find('h2',attrs={'class':'title ellipsis'}).a.contents[0]
                com_href=temp.find('h2',attrs={'class':'title ellipsis'}).a['href']
                com_sid=temp.find('h2',attrs={'class':'title ellipsis'}).a['data-hislog']
                try:ico_year=temp.find('a',attrs={'class':'ico-year'}).span['class'][0][2:]
                except:ico_year='-'
                # 品质保证
                try:ico_ta=temp.find('a',attrs={'class':'ico-ta'})['title']
                except:ico_ta='-'
                contact_href=temp.find('a',attrs={'class':'cd'})['href']
                temp_s=temp.find_all('div',attrs={'class':'attr'})
                try:response_rate=temp_s[-1].div.a.contents[0]
                except:response_rate='-'
                main_products='-';country_region='-';total_revenue='-';top3_markets='-'
                for temp_t in temp_s:
                    t=temp_t.span.contents[0]
                    if t=='Main Products:':
                        main_products=temp_t.div.text
                    elif t=='Country/Region:':
                        country_region=temp_t.div.span.contents[0]
                    elif t=='Total Revenue:':
                        total_revenue=temp_t.div.span.contents[0]
                    elif t=='Top 3 Markets:':
                        tt=temp_t.div.find_all('span')
                        top3_markets='+'.join([item.contents[0] for item in tt])
                    else:continue
                temp_res=[com_name,com_href,com_sid,ico_year,ico_ta,contact_href,
                          main_products,country_region,total_revenue,top3_markets,response_rate]
                queue_res.put(temp_res)

    def run(self):
        self.analysis()

# 解释源码类,传入文件路径
# 使用pyquery
# 未完成，如需使用本类解释页面请先行调用Analysis_src类
class Analysis_src_pyquery(Thread):
    def __init__(self,file_list):
        Thread.__init__(self)
        self.file_list=file_list

    def analysis(self):
        for item in self.file_list:
            with open(item,'r') as txt_file:
                res=txt_file.read()
            content=pq(res)
            frames=content.find('div.f-icon.m-item')
            for temp in frames:
                d=pq(temp)
                com_name=d('h2').children('a').text()
                com_href=d('h2').find('a').attr('href')
                com_sid=d('h2').children('a').attr('data-hislog')
                print(com_name,com_sid)
                print('*'*60)
                # com_name=temp('h2')
                # print(com_name)

            # soup=BeautifulSoup(res)
            # frames=soup.find_all('div',attrs={'class':'f-icon','data-spm':'35'})
            # for temp in frames:
            #     com_name=temp.find('h2',attrs={'class':'title ellipsis'}).a.contents[0]
            #     com_href=temp.find('h2',attrs={'class':'title ellipsis'}).a['href']
            #     com_sid=temp.find('h2',attrs={'class':'title ellipsis'}).a['data-hislog']
            #     try:ico_year=temp.find('a',attrs={'class':'ico-year'}).span['class'][0][2:]
            #     except:ico_year='-'
            #     # 品质保证
            #     try:ico_ta=temp.find('a',attrs={'class':'ico-ta'})['title']
            #     except:ico_ta='-'
            #     contact_href=temp.find('a',attrs={'class':'cd'})['href']
            #     temp_s=temp.find_all('div',attrs={'class':'attr'})
            #     try:response_rate=temp_s[-1].div.a.contents[0]
            #     except:response_rate='-'
            #     main_products='-';country_region='-';total_revenue='-';top3_markets='-'
            #     for temp_t in temp_s:
            #         t=temp_t.span.contents[0]
            #         if t=='Main Products:':
            #             main_products=temp_t.div.text
            #         elif t=='Country/Region:':
            #             country_region=temp_t.div.span.contents[0]
            #         elif t=='Total Revenue:':
            #             total_revenue=temp_t.div.span.contents[0]
            #         elif t=='Top 3 Markets:':
            #             tt=temp_t.div.find_all('span')
            #             top3_markets='+'.join([item.contents[0] for item in tt])
            #         else:continue
            #     temp_res=[com_name,com_href,com_sid,ico_year,ico_ta,contact_href,
            #               main_products,country_region,total_revenue,top3_markets,response_rate]
            #     queue_res.put(temp_res)

    def run(self):
        self.analysis()

# 获取待解释文档列表
def get_filelist(path):
    file_list=os.listdir(path)
    file_list=[path+'/'+item for item in file_list]
    return file_list

if __name__=='__main__':
    # 关键词列表
    keyword_list=['polo','t-shirt','dress']

    # 依据关键词列表生成网址
    gen_url_d=Gen_url(keyword_list=keyword_list)
    urls=gen_url_d.gen_url()

    # 根据所生成的网址下载并保存见面源码
    # 测试阶段仅开启一个线程，线程可增加，将网址list分块后传入url_list参数
    get_src_d=Get_Src(urls)
    get_src_d.run()

    # 获取待解释文档列表
    file_list=get_filelist('d:/spider/alibaba_inter/src')

    # 解释文档
    queue_res=Queue(0)
    test_analysis=Analysis_src(file_list)
    test_analysis.start()
    test_analysis.join()

    # 获得结果
    result=[]
    for i in range(queue_res.qsize()):
        result.append(queue_res.get())
    title=['com_name','com_href','com_sid','ico_year','ico_ta','contact_href',
           'main_products','country_region','total_revenue','top3_markets','response_rate']
    #结果持久化
    writer=My_Csv.Write_Csv(path='d:/spider/alibaba_inter',name='alibaba_inter_com',title=title,result=result)
    writer.add_title_data()

    # 测试pyquery
    # test_pq=Analysis_src_pyquery(file_list)
    # test_pq.start()