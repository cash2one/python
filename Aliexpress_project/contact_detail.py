#coding:utf-8
__author__ = '613108'

import sys,csv,urllib2,re
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append(r'C:\Users\613108\Desktop\Project\Vertical_ecommerce_project\VIP_project')
sys.path.append(r'C:\Users\613108\Desktop\Project\tool_self\Tool_self')
import get_phone_search,My_Csv,list_split
from Queue import Queue
from threading import Thread
from bs4 import BeautifulSoup

class Get_contact_detail(Thread):
    def __init__(self,href_list):
        Thread.__init__(self)
        self.href_list=href_list

    def get_info(self):
        send_headers = {
         'Referer':'www.alibaba.com',
         'User-Agent':'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
         'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
         'Connection':'keep-alive'
        }
        pat=re.compile(r'\n')
        for url in self.href_list:
            try:
                r=urllib2.Request(url=url[1],headers=send_headers)
                res=urllib2.urlopen(r)
                result=res.read()
                res.close()
                soup=BeautifulSoup(result,from_encoding='utf-8')
                frame=soup.find(attrs={'class':'m-content'})
                name=frame.find(attrs={'class':'name'}).text
                name=re.sub(pat,'',name)
                try:department=frame.find(attrs={'class':'dl-horizontal'}).dd.text
                except:department='-'
                sec_frame=frame.find(attrs={'class':'contact-detail'})
                sec_frames=sec_frame.find_all(re.compile(r'd.+?'))[1:]
                tel_phone='-';address='-';province='-';city='-';mobile_phone='-';fax_num='-'
                for i in range(len(sec_frames)):
                    if sec_frames[i].text=='Telephone:':
                        tel_phone=sec_frames[i+1].contents[0]
                    elif sec_frames[i].text=='Address:':
                        address=sec_frames[i+1].contents[0]
                    elif sec_frames[i].text=='Province/State:':
                        province=sec_frames[i+1].contents[0]
                    elif sec_frames[i].text=='City:':
                        city=sec_frames[i+1].contents[0]
                    elif sec_frames[i].text=='Mobile Phone:':
                        mobile_phone=sec_frames[i+1].contents[0]
                    elif sec_frames[i].text=='Fax:':
                        fax_num=sec_frames[i+1].contents[0]
                    else:continue
                result=[url[0],url[1],name,department,tel_phone,mobile_phone,fax_num,address,province,city]
                queue_for_result.put(result)
                print(result)
            except:
                print('*'*20+u'程序运行失误，已跳过'+'*'*20+url[1])

    def run(self):
        self.get_info()

if __name__=='__main__':
    file_name='d:/spider/aliexpress/aliexpress_contact_href_2015-08-06.csv'
    href_temp=[]
    queue_for_result=Queue(0)
    with open(file_name,'r') as csv_file:
        reader=csv.reader(csv_file)
        for row in reader:
            href_temp.append(row)
    href_temp=href_temp[1:]
    href_temp_2=list_split.list_split(href_temp,2)
    Get_contact_detail_thread=[]
    for item in href_temp_2:
        Get_contact_detail_thread.append(Get_contact_detail(item))
    for item in Get_contact_detail_thread:
        item.start()
    for item in Get_contact_detail_thread:
        item.join()

    data=[]
    for i in range(queue_for_result.qsize()):
        data.append(queue_for_result.get())
    title=['shop_name','contact_page_href','contact_name','department','tel_phone','mobile_phone','fax_num','address','province','city']
    writer=My_Csv.Write_Csv(path='D:/spider/aliexpress',name='aliexpress_contact_detail',title=title,result=data)
    writer.add_title_data()
    print('*'*20+u'程序运行完毕，请检查数据'+'*'*20)
