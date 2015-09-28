#coding:utf-8
__author__ = '613108'

from pyquery import PyQuery as pq
from threading import Thread
from Queue import Queue
import sys,urllib2,time,random
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append(r'C:\Users\613108\Desktop\Project\tool_self')
import my_proxy,My_Csv
import os,csv,socket,re
socket.setdefaulttimeout(2)

def use_proxy():
    proxy_port=my_proxy.is_proxy_exists()
    return proxy_port

# 返回待抓取见面地址列表
# href_file_path代表文件所在目录路径
# index_title代表目标链接所有列的表头,如为最后一列，请添加\n
def get_href_list(href_file_path,index_title):
    file_list=os.listdir(href_file_path)
    file_name_list=[href_file_path+'/'+item for item in file_list]
    temp_time=os.stat(file_name_list[0]).st_ctime
    temp_file_name=file_name_list[0]
    for item in file_name_list:
        # 判断是否为目录，如为目录则跳过
        if os.path.isdir(item):continue
        # 获取各文件创建时间
        file_create_time=os.stat(item).st_ctime
        if temp_time<=file_create_time:
            temp_time=file_create_time
            temp_file_name=item
    with open(temp_file_name,'r') as temp_file:
        res=temp_file.readlines()
        href_index=res[0].split(',').index(index_title)
    dict={}
    with open(temp_file_name,'r') as temp_file:
        reader=csv.reader(temp_file)
        i=0
        for row in reader:
            if i>0:
                dict[row[href_index]]=1
            i+=1
    href_list=[]
    for item in dict.items():
        href_list.append(item[0])
    return href_list

# 获取sku信息，主要包括销量、颜色等等
class Get_productInfoDetail(Thread):
    # 对应循环1之构造函数
    # def __init__(self,href_list):
    #     Thread.__init__(self)
    #     self.href_list=href_list

    # 对应循环2之构造函数
    def __init__(self):
        Thread.__init__(self)

    def get_info(self):
        proxy_port=use_proxy()
        proxy=random.sample(proxy_port,1)[0]
        proxy=proxy[0]+':'+proxy[1]
        proxyHandler=urllib2.ProxyHandler({'http':r'http://%s'%proxy})
        cookies=urllib2.HTTPCookieProcessor
        opener=urllib2.build_opener(cookies,proxyHandler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0')]
        # 循环1：分割url列表，若需更换代理url将被遗弃
        # for url in self.href_list:
        # 循环2：利用queue在线程间同步数据，若需更换代理则将url put到queue,不会遗弃
        while queue_for_href_list.qsize()>0:
            url=queue_for_href_list.get()
            print('*'*60)
            print(url)
            try:
                res_temp=opener.open(url)
                src=res_temp.read()
                res_temp.close()
            except:
                queue_for_href_list.put(url)
                proxy=random.sample(proxy_port,1)[0]
                print(u'更换代理：%s:%s'%(proxy[0],proxy[1]))
                proxy=proxy[0]+':'+proxy[1]
                proxyHandler=urllib2.ProxyHandler({'http':r'http://%s'%proxy})
                opener=urllib2.build_opener(cookies,proxyHandler)
                continue
            d=pq(src)
            exp_price=d.find('.f_l.pricekt>span').text().split(':')[1]
            colors=d.find('#color_id')
            temp_for_size=len(colors)
            color=[]
            for item in colors:
                temp=pq(item).attr('title')
                color.append(temp)
            color='+'.join(color)
            sizes=d.find('.doselected')[temp_for_size:]
            size=[]
            for item in sizes:
                temp=pq(item).attr('data-sizes')
                size.append(temp)
            size='+'.join(size)
            sale=d.find('.kuc').text().split('已售 ')[1].split(' 件')[0]
            temp=d.find('.content.clearfix li')
            brand='-';sku='-';launch_date='-';sex='-'
            for item in temp:
                tt=pq(item).text()
                tt_1=tt.split('：')[0]
                tt_2=tt.split('：')[1]
                if tt_1==u'品牌':
                    brand=tt_2
                elif tt_1==u'货号':
                    sku=tt_2
                elif tt_1==u'上市时间':
                    launch_date=tt_2
                elif tt_1==u'性别':
                    sex=tt_2
                else:continue
            temp=[url,brand,sku,launch_date,sex,exp_price,color,size,sale]
            queue_for_result.put(temp)

    def run(self):
        self.get_info()

if __name__=='__main__':
    t=time.time()
    temp=use_proxy()

    queue_for_href_list=Queue(0)
    queue_for_result=Queue(0)

    href_list=get_href_list(href_file_path=r'D:\spider\361du\product_href',index_title='product_href\n')
    for item in href_list:
        queue_for_href_list.put(item)

    # 配置项：线程数
    thread_count=50
    Get_productInfoDetail_thread=[]

    for i in range(thread_count):
        Get_productInfoDetail_thread.append(Get_productInfoDetail())
    for item in Get_productInfoDetail_thread:
        item.start()
    for item in Get_productInfoDetail_thread:
        item.join()

    # 结果持久化
    # 结果提取及标题处理
    result=[]
    for i in range(queue_for_result.qsize()):
        result.append(queue_for_result.get())
    title=['product_url','brand','sku','launch_date','sex','exp_price','color','size','sale']
    # 数据写入csv文件
    writer=My_Csv.Write_Csv(path=r'd:/spider/361du',name='361du_productInfoDetail',title=title,result=result)
    writer.add_title_data()

    print('*'*20+u'程序运行完毕，请检查数据'+'*'*20)

    t=time.time()-t
    print('*'*16+u'总计耗时：%f 秒'+'*'*16)%t