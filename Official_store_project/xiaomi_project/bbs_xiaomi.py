#coding:utf-8
__author__ = '613108'

from bs4 import BeautifulSoup
import urllib2
from threading import Thread
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append(r'C:\Users\613108\Desktop\Project\tool_self')
import My_Csv

send_headers = {'Referer':'www.baidu.com/',
                'User-Agent':'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Connection':'keep-alive'}
result=[]

class Data_Get(Thread):
    def __init__(self,url_list):
        Thread.__init__(self)
        self.url_list=url_list

    def get_data(self):
        try:
            for url in self.url_list:
                req=urllib2.Request(url,headers=send_headers)
                req=urllib2.urlopen(req)
                soup=BeautifulSoup(req,from_encoding='UTF-8')
                frames=soup.find_all(attrs={'class':'theme_list_con'})
                # print(len(frames))
                for item in frames:
                    thd_topic=item.find(attrs={'class':'title'}).a.string.replace('	','')
                    thd_href='http://bbs.xiaomi.cn'+item.find(attrs={'class':'title'}).a['href']
                    second_frame=item.find(attrs={'class':'auth_msg clearfix'})
                    temp_1=second_frame.find(attrs={'class':'numb msg'})#.find_all('span')
                    pat_1=re.compile(r'''<span class="numb msg"><i></i>(?P<find>.+?)</span>''')
                    found_1=re.search(pat_1,str(temp_1))
                    thd_replies=found_1.group('find')
                    temp_2=second_frame.find(attrs={'class':'numb view'})
                    pat_2=re.compile(r'''<span class="numb view"><i></i>(?P<find>.+?)</span>''')
                    found_2=re.search(pat_2,str(temp_2))
                    thd_view=found_2.group('find')
                    thd_username=second_frame.a.contents[0]
                    thd_plate=second_frame.find_all('a')[1].contents[0].replace('\r\n','')
                    thd_publictime=second_frame.find_all('span')[1].contents[0].replace('	','')
                    temp=[thd_topic,thd_href,thd_plate,thd_username,thd_publictime,thd_view,thd_replies]
                    result.append(temp)
                    print('*'*50)
                    for item in temp:
                        print(item.encode('gbk','ignore'))
        except:pass

    def run(self):
        self.get_data()

if __name__=='__main__':
    url_list=['http://bbs.xiaomi.cn/thread/digest/pn/'+str(i+1) for i in range(1000)]
    Data_Get_thread=[]
    # 开启50个线程
    thread_count=50
    for i in range(thread_count):
        temp=Data_Get(url_list[((len(url_list)+thread_count-1)/thread_count)*i:((len(url_list)+thread_count-1)/20)*(i+1)])
        Data_Get_thread.append(temp)
    for i in range(len(Data_Get_thread)):
        Data_Get_thread[i].start()
    for i in range(len(Data_Get_thread)):
        Data_Get_thread[i].join()

    writer=My_Csv.Write_Csv('d:/spider/xiaomi','xiaomi_forum',result)
    writer.add_title_data(['thd_topic','thd_href','thd_plate','thd_username','thd_publictime','thd_view','thd_replies'])

    print('='*20+u'程序执行完毕，请检查所抓取的数据'+'='*20)