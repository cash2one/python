#coding:utf-8
__author__ = '613108'

import urllib2
from bs4 import BeautifulSoup
from threading import Thread
import pymysql
from Queue import Queue
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append(r'C:\Users\613108\Desktop\Project\tool_self')
import My_Csv

def connection():
    conn=pymysql.connect(host='10.118.187.12',user='admin',passwd='admin',charset='utf8',db='elec_platform')
    cursor=conn.cursor()
    return conn,cursor

def get_hrefs():
    conn,cursor=connection()
    sql_select='select distinct shop_judge_href from jd_thirdparty_shop_href where staus is null'
    cursor.execute(sql_select)
    href=cursor.fetchall()
    href=[item_2 for item_1 in href for item_2 in item_1]
    conn.close()
    print(len(href))
    return href

class getJudge(Thread):
    def __init__(self,url_list):
        Thread.__init__(self)
        self.url_list=url_list

    def getjudge(self):
        for url in self.url_list:
            try:
                addHanders={'Referer':'www.jd.com',
                            'User-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20100101 Firefox/15.0.1'}
                req=urllib2.Request(url=url,headers=addHanders)
                req_temp=urllib2.urlopen(req)
                soup=BeautifulSoup(req_temp,from_encoding='UTF-8')
                company_name=soup.find(attrs={'class':'shopTolal'}).find_all('span')[2].contents[0]
                judge_total=soup.find(attrs={'class':'jMallInfo'}).find_all('tr')[2].div['title']
                temp_1=soup.find(attrs={'class':'jMallInfo'}).find_all('tr')[3].find_all('span')[1]['class'][0]
                if temp_1=='jIconLow':
                    judge_total_avg='-'+soup.find(attrs={'class':'jMallInfo'}).find_all('tr')[3].find_all('span')[1].em.contents[0]
                else:judge_total_avg=soup.find(attrs={'class':'jMallInfo'}).find_all('tr')[3].find_all('span')[1].em.contents[0]
                temp_2=soup.find_all(attrs={'class':'jScore'})
                for i in range(len(temp_2)):
                    name=globals()
                    name['judge_title_'+str(i)]=temp_2[i].div.find(attrs={'class':'jGrade'})['title']
                    try:name['judge_title_'+str(i)+'_avg']='-'+temp_2[i].div.find(attrs={'class':'jIconLow'}).em.string
                    except AttributeError:
                        try:
                            name['judge_title_'+str(i)+'_avg']=temp_2[i].div.find(attrs={'class':'jIconHigh'}).em.string
                        except:name['judge_title_'+str(i)+'_avg']='-'
                    temp_3=temp_2[i].find_all('li')
                    for x in range(len(temp_3)):
                        name=globals()
                        name['judge_'+str(i)+'_'+str(x)]=temp_3[x].find(attrs={'class':'jNum'})['title']
                        try:
                            if temp_3[x].find(attrs={'class':'jIconLow'}):
                                name['judge_'+str(i)+'_'+str(x)+'_avg']='-'+temp_3[x].find(attrs={'class':'jIconLow'}).em.string
                            else:
                                name['judge_'+str(i)+'_'+str(x)+'_avg']=temp_3[x].find(attrs={'class':'jIconHigh'}).em.string
                        # except:name['judge_'+str(i)+'_'+str(x)+'_avg']=temp_3[x].find_all('span')[-1].em.string
                        except:name['judge_'+str(i)+'_'+str(x)+'_avg']='-'
                result=[company_name,judge_total,judge_total_avg,
                        judge_title_0,judge_title_0_avg,judge_0_0,judge_0_0_avg,judge_0_1,judge_0_1_avg,judge_0_2,judge_0_2_avg,
                        judge_title_1,judge_title_1_avg,judge_1_0,judge_1_0_avg,judge_1_1,judge_1_1_avg,judge_1_2,judge_1_2_avg,judge_1_3,judge_1_3_avg,
                        judge_title_2,judge_title_2_avg,judge_2_0,judge_2_0_avg,judge_2_1,judge_2_1_avg,judge_2_2,judge_2_2_avg,judge_2_3,judge_2_3_avg]
                queue.put(result)
            except:continue

    def run(self):
        self.getjudge()

if __name__=='__main__':
    #20个线程并发抓取
    queue=Queue(0)
    thread_count=20
    url_total=get_hrefs()
    getJudge_thread=[]
    for i in range(thread_count):
        temp=getJudge(url_total[((len(url_total)+thread_count-1)/thread_count)*i:((len(url_total)+thread_count-1)/thread_count)*(i+1)])
        getJudge_thread.append(temp)

    for i in range(len(getJudge_thread)):
        getJudge_thread[i].start()

    for i in range(len(getJudge_thread)):
        getJudge_thread[i].join()

    res=[]
    for i in range(queue.qsize()):
        res.append(queue.get())
    writer=My_Csv.Write_Csv(path='d:/spider/jd',name='jd_companyname',result=res)
    writer.add_title_data(title=['company_name','judge_total','judge_total_avg',
                        'judge_title_0','judge_title_0_avg','judge_0_0','judge_0_0_avg','judge_0_1','judge_0_1_avg','judge_0_2','judge_0_2_avg',
                        'judge_title_1','judge_title_1_avg','judge_1_0','judge_1_0_avg','judge_1_1','judge_1_1_avg','judge_1_2','judge_1_2_avg','judge_1_3','judge_1_3_avg',
                        'judge_title_2','judge_title_2_avg','judge_2_0','judge_2_0_avg','judge_2_1','judge_2_1_avg','judge_2_2','judge_2_2_avg','judge_2_3','judge_2_3_avg'])