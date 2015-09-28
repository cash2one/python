#coding:utf-8
__author__ = '613108'

import urllib2
from bs4 import BeautifulSoup
from threading import Thread
from Queue import Queue
import urllib
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append(r'C:\Users\613108\Desktop\Project\tool_self')
import My_Csv,list_split

class Get_BrandHref(Thread):
    def __init__(self,url_list):
        Thread.__init__(self)
        self.url_list=url_list

    def get_href(self):
        for url in self.url_list:
            result=urllib2.urlopen(url)
            soup=BeautifulSoup(result.read(),from_encoding='utf-8')
            result.close()
            frame=soup.find(attrs={'class':'brands'})
            frames=frame.findAll('li')
            for item in frames:
                en_brand=item.a['title'].split('/')[0]
                try:ch_brand=item.a['title'].split('/')[1]
                except:ch_brand='-'
                href='http://brand.vip.com'+item.a['href']
                temp=[en_brand,ch_brand,href]
                queue_href.put(temp)

    def run(self):
        self.get_href()

class Get_BrandText(Thread):
    # def __init__(self,url_list):
    #     Thread.__init__(self)
    #     self.url_list=url_list
    def __init__(self,brand_link):
        Thread.__init__(self)
        self.brand_link=brand_link

    def get_likeNum(self,brand_id):
        data={'brand_sn':brand_id}
        data=urllib.urlencode(data)
        url='http://fav.myopen.vip.com/brand/favbrand/brand_fav_count'
        # print(url+'?'+data)
        Request=urllib2.Request(url=url+'?'+data)
        result=urllib2.urlopen(Request)
        temp=result.read()
        result.close()
        res=temp.split(':')[-1]
        res=res.split('}')[0]
        return res

    def get_desc(self):
        for url in self.brand_link:
            try:
                result=urllib2.urlopen(url)
                res=result.read()
                result.close()
                soup=BeautifulSoup(res)
                result=soup.find_all(attrs={'class':'desc'})[1]
                result=result.findAll('p')
                temp=''
                for item in result:
                    try:
                        temp+=item.contents[0]
                    except:pass
                brand_id=soup.find(attrs={'class':'like'}).span['data-mars']
                likeNum=self.get_likeNum(brand_id=brand_id)
                result_temp=[url,temp,likeNum]
                queue_brandtext.put(result_temp)
            except:print(u'失败网址：'+url)

    def run(self):
        self.get_desc()

if __name__=='__main__':
    queue_href=Queue(0)
    result_brand=[]
    # 构造品牌列表网址：
    temp=''.join(map(chr,range(97,123)))
    url_list=['http://brand.vip.com/list-'+item+'/' for item in temp]
    url_list.append('http://brand.vip.com/list-0-9/')
    # 获取品牌名称数据
    print('*'*20+u'正在抓取品牌列表'+'*'*20)
    thread_count=5
    Get_BrandHref_thread=[]
    url_list=list_split.list_split(url_list,thread_count)
    for url_s in url_list:
        Get_BrandHref_thread.append(Get_BrandHref(url_s))
    for item in Get_BrandHref_thread:
        item.start()
    for item in Get_BrandHref_thread:
        item.join()
    for i in range(queue_href.qsize()):
        result_brand.append(queue_href.get())
    writer=My_Csv.Write_Csv(path='D:/spider/vip',name='vip_allbrand_list',result=result_brand)
    writer.add_title_data(title=['en_brand','ch_brand','href'])
    # 获取品牌简介及收藏量数据
    print('*'*20+u'正在抓取品牌简介'+'*'*20)
    queue_brandtext=Queue(0)
    result_brandText=[]
    thread_count_2=30
    temp_href=[item[2] for item in result_brand]
    temp_href_list=list_split.list_split(temp_href,thread_count_2)
    Get_BrandText_thread=[]
    for url_s in temp_href_list:
        Get_BrandText_thread.append(Get_BrandText(url_s))
    for item in Get_BrandText_thread:
        item.start()
    for item in Get_BrandText_thread:
        item.join()
    for i in range(queue_brandtext.qsize()):
        result_brandText.append(queue_brandtext.get())
    writer=My_Csv.Write_Csv(path='D:/spider/vip',name='vip_allbrand_Text',result=result_brandText)
    writer.add_title_data(title=['href','temp','likeNum'])
    print('*'*20+u'程序运行完毕，请检查数据'+'*'*20)
