#coding:utf-8
__author__ = '613108'

import sys,csv,urllib2,urllib,os
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append(r'C:\Users\613108\Desktop\Project\Vertical_ecommerce_project\VIP_project')
sys.path.append(r'C:\Users\613108\Desktop\Project\tool_self\Tool_self')
import get_phone_search,My_Csv,list_split
from Queue import Queue
from threading import Thread
from bs4 import BeautifulSoup

def company_list():
    # 配置文件路径
    path='D:/spider/aliexpress/res'
    file_name_list=os.listdir(path)
    file_name_list=[path+'/'+item for item in file_name_list]
    # 筛选去重
    company=[]
    for file_name in file_name_list:
        try:
            with open(file_name,'r') as csv_file:
                reader=csv.reader(csv_file)
                for row in reader:
                    company.append([row[3],row[5]])
        except:continue
    d={}
    for item in company:
        if 'list' in item[1]:continue
        else:
            d[item[1]]=item[0]
    for item in d.items():
        print(item)
    # 提取符合条件的公司列表
    company_ok=[]
    for item in d.items():
        # 判断是否为公司
        if 'LTD'in item[1].upper() or 'LIMITED' in item[1].upper() \
            or '&CO.' in item[1].upper() or 'INC.' in item[1].upper() \
            or 'CORP.' in item[1].upper():
            company_ok.append(item[1])
        else:continue
    return company_ok

class Get_contact_href(Thread):
    def __init__(self,com_list):
        Thread.__init__(self)
        self.com_list=com_list

    def get_href(self):
        send_headers = {
         'Referer':'www.alibaba.com',
         'User-Agent':'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
         'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
         'Connection':'keep-alive'
        }
        for com_name in self.com_list:
            url_b='http://www.alibaba.com/trade/search?'
            url_p={'fsb':'y','IndexArea':'company_en','CatId':'','SearchText':com_name}
            url=url_b+urllib.urlencode(url_p)
            print(url)
            r=urllib2.Request(url=url,headers=send_headers)
            res=urllib2.urlopen(r)
            result=res.read()
            res.close()
            soup=BeautifulSoup(result,from_encoding='utf-8')
            try:
                frames=soup.find_all(attrs={'class':'f-icon'})
                for item in frames:
                    temp=item.find(attrs={'class':'item-title'})
                    if temp:
                        name=temp.h2.a.text
                    else:continue
                    if name==com_name:
                        try:
                            href=item.find(attrs={'class':'company'}).a['href']
                            print(href)
                            print('*'*60)
                            result=[name,href]
                            queue_result.put(result)
                            break
                        except:pass
                    else:continue
            except:pass

    def run(self):
        self.get_href()

if __name__=='__main__':
    queue_result=Queue(0)
    com_list=company_list()
    # for item in com_list:
    #     print(item)
    # print(len(com_list))

    # 从阿里巴巴匹配公司联系方式
    # com_list=list_split.list_split(com_list,30)
    # Get_contact_href_thread=[]
    # for item in com_list:
    #     Get_contact_href_thread.append(Get_contact_href(item))
    # for item in Get_contact_href_thread:
    #     item.start()
    # for item in Get_contact_href_thread:
    #     item.join()
    #
    # data=[]
    # for i in range(queue_result.qsize()):
    #     data.append(queue_result.get())
    # writer=My_Csv.Write_Csv(path='D:/spider/aliexpress',name='aliexpress_contact_href',title=[],result=data)
    # writer.add_title_data()

    # 从搜狗搜索匹配公司联系方式
    # queue_result=Queue(0)
    # temp_arr_com=list_split.list_split(com_list,2)
    # Get_phoneaddr_thread=[]
    # for arr in temp_arr_com:
    #     print(len(arr))
    # for item in temp_arr_com:
    #     Get_phoneaddr_thread.append(get_phone_search.Get_phoneaddr(item))
    # for item in Get_phoneaddr_thread:
    #     item.start()
    # for item in Get_phoneaddr_thread:
    #     item.join()
    # result=[]
    # for i in range(queue_result.qsize()):
    #     result.append(queue_result.get())
    # result=[item for i in result for item in i]
    # writer=My_Csv.Write_Csv(path='D:/spider/aliexpress',name='aliexpress_phone_addr',title=[],result=result)
    # writer.add_title_data()
    print('*'*20+u'程序运行完毕，请检查数据'+'*'*20)