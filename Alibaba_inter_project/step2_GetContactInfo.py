#coding:utf-8
__author__ = '613108'

import os,csv,sys,urllib2,random
from pyquery import PyQuery as pq
from threading import Thread
from Queue import Queue
from urllib2 import HTTPError,URLError
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append(r'C:\Users\613108\Desktop\Project\tool_self')
import My_Csv,my_proxy,list_split

# 获取联系方式详细信息
class Get_contactHref():
    def __init__(self,href_file_path):
        self.href_file_path=href_file_path

    # 返回最新的一个文件
    def get_newFile(self):
        file_list=os.listdir(self.href_file_path)
        file_name_list=[self.href_file_path+'/'+item for item in file_list]
        temp_time=os.stat(file_name_list[0]).st_ctime
        temp_file_name=''
        for item in file_name_list:
            # 判断是否为目录，如为目录则跳过
            if os.path.isdir(item):continue
            # 获取各文件创建时间
            file_create_time=os.stat(item).st_ctime
            if temp_time<=file_create_time:
                temp_time=file_create_time
                temp_file_name=item
            else:continue
        return temp_file_name

    # 返回待抓取网页地址
    def get_contactHref(self):
        file_name=self.get_newFile()
        with open(file_name,'r') as temp_file:
            res=temp_file.readlines()
            # 返回链接所在列索引
            href_index=res[0].split(',').index('contact_href')
            # 放弃，英文中逗号分隔符太多，出错机率高
            # href_list=[item.split(',')[href_index] for item in res[1:]]
        # 利用dictionary对链接去重
        dict={}
        with open(file_name,'r') as temp_file:
            reader=csv.reader(temp_file)
            i=0
            for row in reader:
                if i>0:
                    dict[row[href_index]]=1
                i+=1
        contact_href_href=[]
        for item in dict.items():
            contact_href_href.append(item[0])
        return contact_href_href

class Get_contactInfo(Thread):
    def __init__(self,contact_href_list,proxy=1):
        Thread.__init__(self)
        self.contact_href_list=contact_href_list
        # proxy表示是否使用代理；默认使用代理，若无需使用proxy赋值0（可提供效率，但被不能过度抓取，容易被封）
        self.proxy=proxy

    # 本方法直接利用pyquery获取网页源码，可能被封
    def get_contactInfo(self):
        contact_href=self.contact_href_list
        result=[]
        for item in contact_href:
            try:d=pq(item)
            except HTTPError,e:print(e.code);break
            except URLError,e:print(e.reason);break
            except:break
            contact_name=d.find('#contact-person .name').text()
            # 进入源码自定义my_text方法，支持返回列表
            # 返回联系方式：姓名、职位、电话等
            contact_detail_1=d.find('dt').my_text()
            contact_detail_2=d.find('dd').my_text()
            resut_zip_1=zip(contact_detail_1,contact_detail_2)
            # 返回公司名称、办公地址、网址等
            contact_detail_3=d.find('th').my_text()
            contact_detail_4=d.find('th').next().my_text()
            resut_zip_2=zip(contact_detail_3,contact_detail_4)
            resut_zip_temp=resut_zip_1+resut_zip_2
            resut_title_data=[('contact_name:',contact_name)]+resut_zip_temp+[('contact_href:',item)]
            # 常量，用于匹配返回结果数据
            title=['contact_name:', 'Department:', 'Job Title:', 'Telephone:', 'Mobile Phone:', 'Fax:', 'Address:',
                   'Zip:', 'Country/Region:', 'Province/State:', 'City:', 'Company Name:', 'Operational Address:',
                   'Website:', 'Website on alibaba.com:', 'Aliexpress.com Store:', 'contact_href:']
            result_temp=['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-']
            for i in range(len(title)):
                for item in resut_title_data:
                    if item[0]==title[i]:
                        result_temp[i]=item[1]
            queue_for_result.put(result_temp)
            print(result_temp)
        #     result.append(result_temp)
        # return result

    # 返回代理
    def use_proxy(self):
        proxy_port=my_proxy.is_proxy_exists()
        return proxy_port

    # 本方法利用urllib2获取网页源码，如果被封则调用proxy模块，转换代理
    def get_contactInfo_new(self):
        contact_href=self.contact_href_list
        cookies=urllib2.HTTPCookieProcessor
        # 调用代理
        proxy_port=self.use_proxy()
        proxy=random.sample(proxy_port,1)[0]
        proxy=proxy[0]+':'+proxy[1]
        proxyHandler=urllib2.ProxyHandler({'http':r'http://%s'%proxy})
        opener=urllib2.build_opener(cookies,proxyHandler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0')]
        for item in contact_href:
            try:
                res_temp=opener.open(item)
                src=res_temp.read()
                res_temp.close()
            except:
                # 更换代理
                proxy=random.sample(proxy_port,1)[0]
                proxy=proxy[0]+':'+proxy[1]
                proxyHandler=urllib2.ProxyHandler({'http':r'http://%s'%proxy})
                opener=urllib2.build_opener(cookies,proxyHandler)
                continue
                # 本操作对失败网址（item）作弃用处理，若需二度处理可put到列表再调用本方法
            d=pq(src)
            contact_name=d.find('#contact-person .name').text()
            # 进入源码自定义my_text方法，支持返回列表
            # 返回联系方式：姓名、职位、电话等
            contact_detail_1=d.find('dt').my_text()
            contact_detail_2=d.find('dd').my_text()
            resut_zip_1=zip(contact_detail_1,contact_detail_2)
            # 返回公司名称、办公地址、网址等
            contact_detail_3=d.find('th').my_text()
            contact_detail_4=d.find('th').next().my_text()
            resut_zip_2=zip(contact_detail_3,contact_detail_4)
            resut_zip_temp=resut_zip_1+resut_zip_2
            resut_title_data=[('contact_name:',contact_name)]+resut_zip_temp+[('contact_href:',item)]
            # 常量，用于匹配返回结果数据
            title=['contact_name:', 'Department:', 'Job Title:', 'Telephone:', 'Mobile Phone:', 'Fax:', 'Address:',
                   'Zip:', 'Country/Region:', 'Province/State:', 'City:', 'Company Name:', 'Operational Address:',
                   'Website:', 'Website on alibaba.com:', 'Aliexpress.com Store:', 'contact_href:']
            result_temp=['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-']
            for i in range(len(title)):
                for item in resut_title_data:
                    if item[0]==title[i]:
                        result_temp[i]=item[1]
            queue_for_result.put(result_temp)
            print(result_temp)

    def run(self):
        if self.proxy:
            self.get_contactInfo_new()
        else:
            self.get_contactInfo()

# 当日代理可能未有，需先行调用，避免开启多线程的时候同时抓取代理
def use_proxy():
    proxy_port=my_proxy.is_proxy_exists()
    return proxy_port

if __name__=='__main__':
    queue_for_result=Queue(0)

    # 返回链接
    get_contactHref_d=Get_contactHref(r'D:\spider\alibaba_inter').get_contactHref()

    # 链接列表切割，为多个线程服务
    # 配置项：计划开启线程数
    thread_count=10
    get_contactHref_split=list_split.list_split(get_contactHref_d,thread_count)

    # 信息获取
    # 配置项，是否使用代理
    is_proxy=1
    if is_proxy:
        use_proxy()

    Get_contactInfo_thread=[]
    for item in get_contactHref_split:
        Get_contactInfo_thread.append(Get_contactInfo(contact_href_list=item,proxy=is_proxy))
    for item in Get_contactInfo_thread:
        item.start()
    for item in Get_contactInfo_thread:
        item.join()

    # 结果持久化
    # 结果提取及标题处理
    result=[]
    for i in range(queue_for_result.qsize()):
        result.append(queue_for_result.get())
    title=['contact_name:', 'Department:', 'Job Title:', 'Telephone:', 'Mobile Phone:', 'Fax:', 'Address:',
           'Zip:', 'Country/Region:', 'Province/State:', 'City:', 'Company Name:', 'Operational Address:',
           'Website:', 'Website on alibaba.com:', 'Aliexpress.com Store:', 'contact_href:']
    title=[item[:-1] for item in title]
    # 数据写入csv文件
    writer=My_Csv.Write_Csv(path='d:/spider/alibaba_inter',name='alibaba_inter_com_contactDetail',title=title,result=result)
    writer.add_title_data()