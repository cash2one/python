#coding:utf-8
__author__ = '613108'

from bs4 import BeautifulSoup
import urllib
import urllib2
import time
import csv
import sys
sys.path.append('C:/Users/613108/Desktop/Project/myTool')
import My_Csv

result_href=[]

class Get_Info():
    def __init__(self,keyword,page_count):
        self.page_count=page_count
        self.keyword=keyword

    def get_info(self):
        temp=(self.page_count-1)*50+1
        for i in range(0,temp,50):
            # print('+'*60)
            send_headers = {'Referer':'www.baidu.com/',
                            'User-Agent':'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
                            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                            'Connection':'keep-alive'}
            url='http://tieba.baidu.com/f?'
            value={'kw':self.keyword,'ie':'utf-8','pn':i}
            url=url+urllib.urlencode(value)
            Requst=urllib2.Request(url=url,headers=send_headers)
            result=urllib2.urlopen(Requst)
            result=result.read()
            soup=BeautifulSoup(result)
            frames=soup.find_all(attrs={'class':'j_thread_list'})
            for item in frames:
                rep_num=item.find(attrs={'class':'threadlist_rep_num'}).contents[0].encode('gbk','ignore')
                title=item.find(attrs={'class':'j_th_tit'}).a.contents[0].encode('gbk','ignore')
                href='http://tieba.baidu.com'+item.find(attrs={'class':'j_th_tit'}).a['href'].encode('gbk','ignore')
                try:author=item.find(attrs={'class':'threadlist_author'}).find(attrs={'class':'j_user_card'}).contents[0].encode('gbk','ignore')
                except:author='-'
                try:text=item.find(attrs={'class':'threadlist_abs'}).contents[0].encode('gbk','ignore')
                except:text='-'
                result=[title,author,href,text,rep_num]
                result_href.append(result)
            print('='*20+u'第 '+str(1+i/50)+u' 页'+'='*20)

class Write_Csv():
    def __init__(self,path,name,result):
        self.result=result
        self.path=path
        self.name=name

    def get_filename(self):
        filename=('d:/spider/'+ self.path + '/' + self.name + '_%s.csv')%str(time.strftime('%Y-%m-%d %H_%M_%S'))
        return filename

    def add_data(self):
        filename=self.get_filename()
        with open(filename,'wb') as csvfile:
            writer=csv.writer(csvfile)
            writer.writerows(self.result)

    def add_title(self,title):
        filename=self.get_filename()
        with open(filename,'wb') as csvfile:
            writer=csv.writer(csvfile)
            writer.writerow(title)

if __name__=='__main__':
    test=Get_Info('笔记本',100)
    test.get_info()
    writer=Write_Csv('tieba','tieba_notebook',result_href)
    writer.add_title(['title','author','href','text','rep_num'])
    writer.add_data()