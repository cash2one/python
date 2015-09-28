#coding:utf-8
__author__ = 'Administrator'

import urllib,urllib2,sys,random,socket,time,csv
from bs4 import BeautifulSoup
from threading import Thread
from Queue import Queue
from pyquery import PyQuery as pq
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append(r'C:\Users\613108\Desktop\Project\tool_self')
import My_Csv,my_proxy
socket.setdefaulttimeout(20)

# 产品链接抓取类
class Get_productHref():

    def get_pageCount(self):
        # url='http://www.xtep.com.cn/list_goods/'
        url='http://www.xtep.com.cn/list_goods/lists?app_page=null&t=0.00000000000000000&is_ajax'
        # post参数
        data={'ajax_div':'showGoodsLists','ajax_url':'/list_goods/lists?app_page=null','page':1}
        data=urllib.urlencode(data)
        req=urllib2.urlopen(url=url,data=data)
        result=req.read()
        req.close()

        soup=BeautifulSoup(result)
        pagecount=soup.find_all(attrs={'class':'pageNext'})[1]['onclick']
        pagecount=int(pagecount.split(',')[3])

        return pagecount

    def get_productHref(self):
        result = []
        page_count=self.get_pageCount()
        url='http://www.xtep.com.cn/list_goods/lists?app_page=null&t=0.00000000000000000&is_ajax'
        for i in range(page_count):
            # post参数
            data={'ajax_div':'showGoodsLists','ajax_url':'/list_goods/lists?app_page=null','page':(i+1)}
            data=urllib.urlencode(data)
            req=urllib2.urlopen(url=url,data=data)
            res=req.read()
            req.close()
            soup = BeautifulSoup(res)
            frames=soup.find_all(attrs={'class':'mt5'})
            for item in frames:
                # title=item.a.text.encode('GB18030')
                href='http://www.xtep.com.cn'+item.a['href']
                result.append([href])
        title=['href']
        # 数据写入csv文件
        writer=My_Csv.Write_Csv(path=r'd:/spider/xtep',name='xtep_productHref',title=title,result=result)
        writer.add_title_data()

# 产品信息抓取类
class Get_productInfo(Thread):
    def __init__(self):
        Thread.__init__(self)

    def get_info(self):
        proxy_port=my_proxy.is_proxy_exists()
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
            if 'goods' in url:
                print('*'*60)
                print(url)
                try:
                    res_temp=opener.open(url)
                except:
                    queue_for_href_list.put(url)
                    proxy=random.sample(proxy_port,1)[0]
                    print(u'更换代理：%s:%s'%(proxy[0],proxy[1]))
                    proxy=proxy[0]+':'+proxy[1]
                    proxyHandler=urllib2.ProxyHandler({'http':r'http://%s'%proxy})
                    opener=urllib2.build_opener(cookies,proxyHandler)
                    continue
                src=res_temp.read()
                res_temp.close()
                d=pq(src)
                frame=d.find('.detailsRight.fr')
                d=pq(frame)
                title=d.find('.fb').text()
                try:price=d.find('.goodsPrice .styleUL span').eq(0).text()[1:]
                except:continue
                price_original=d.find('.goodsPrice .styleUL span').eq(1).text()
                price_original=price_original.split('：')[1][1:]
                product_sn=d.find('.goodsPrice dd').eq(2).text().split('： ')[1]
                sale=d.find('.goodsPrice dd').eq(3).text().split('： ')[1]
                jifeng=d.find('.goodsPrice dd').eq(4).text().split('： ')[1]
                colors=d.find('#gxm_selcolor')
                res_col=[]
                for item in colors:
                    temp=pq(item).attr('value')
                    res_col.append(temp)
                color='+'.join(res_col)
                sizes=d.find('.goodsSize li a')[:-1]
                res_size=[]
                for item in sizes:
                    temp=pq(item).attr('value')
                    res_size.append(temp)
                size='+'.join(res_size)
                result=[title,price,price_original,product_sn,sale,jifeng,color,size]
                print(result)
                # for item in result:
                #     print(item)
                queue_for_result.put(result)

    def run(self):
        self.get_info()

# 评论抓取类
class Get_commentDetail(Thread):
    def __init__(self):
        Thread.__init__(self)

    def get_pageCount(self,product_sn):
        # url='http://www.xtep.com.cn/list_goods/'
        url='http://www.xtep.com.cn/?app_act=goods/comment&goods_sn='+str(product_sn)+'&app_page=null&t=0.00000000000000000&is_ajax'
        # post参数
        data={'ajax_div':'all_commentList','ajax_url':'/?app_act=goods/comment&goods_sn='+str(product_sn)+'&app_page=null','page':1}
        data=urllib.urlencode(data)

        proxy_port=my_proxy.is_proxy_exists()
        proxy=random.sample(proxy_port,1)[0]
        proxy=proxy[0]+':'+proxy[1]
        print(proxy)
        while True:
            proxyHandler=urllib2.ProxyHandler({'http':r'http://%s'%proxy})
            cookies=urllib2.HTTPCookieProcessor
            opener=urllib2.build_opener(cookies,proxyHandler)
            opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0')]
            try:
                req=opener.open(fullurl=url,data=data)
                result=req.read()
            except:
                proxy=random.sample(proxy_port,1)[0]
                proxy=proxy[0]+':'+proxy[1]
                print(u'更换代理：%s'%(proxy))
                continue
            req.close()
            soup=BeautifulSoup(result)
            try:
                pagecount=soup.find_all(attrs={'class':'pageNext'})[1]['onclick']
                pagecount=int(pagecount.split(',')[3])
            except:pagecount=1
            print(pagecount)
            # 跳出死循环
            break
        return pagecount

    def get_commentDetail(self):
        result=[]
        while queue_for_comment_productSn.qsize()>0:
            product_sn=queue_for_comment_productSn.get()
            page_count=self.get_pageCount(product_sn)
            url='http://www.xtep.com.cn/?app_act=goods/comment&goods_sn='+str(product_sn)+'&app_page=null&t=0.00000000000000000&is_ajax'
            data_list=[]
            for i in range(page_count):
                # 生成所有post参数，添加到data_list中
                data={'ajax_div':'all_commentList','ajax_url':'/?app_act=goods/comment&goods_sn='+str(product_sn)+'&app_page=null','page':(i+1)}
                data=urllib.urlencode(data)
                data_list.append(data)

            proxy_port=my_proxy.is_proxy_exists()
            proxy=random.sample(proxy_port,1)[0]
            proxy=proxy[0]+':'+proxy[1]
            proxyHandler=urllib2.ProxyHandler({'http':r'http://%s'%proxy})
            cookies=urllib2.HTTPCookieProcessor
            opener=urllib2.build_opener(cookies,proxyHandler)
            opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0')]
            while len(data_list)>0:
                # post参数
                data_temp=random.sample(data_list,1)[0]
                data_list.remove(data_temp)
                time.sleep(1)
                try:
                    req=opener.open(fullurl=url,data=data_temp)
                    res=req.read()
                except:
                    data_list.append(data_temp)
                    proxy=random.sample(proxy_port,1)[0]
                    print(u'更换代理：%s:%s'%(proxy[0],proxy[1]))
                    proxy=proxy[0]+':'+proxy[1]
                    proxyHandler=urllib2.ProxyHandler({'http':r'http://%s'%proxy})
                    opener=urllib2.build_opener(cookies,proxyHandler)
                    continue
                res=res.decode('utf-8','ignore')
                req.close()
                d=pq(res)
                frames=d.find('.commentList')
                page_num=data_temp.split('page=')[1].split('&')[0]
                for item in frames:
                    d=pq(item)
                    comment_person=d('p').text()
                    comment_time=d.find('.commentTitle').my_text()[0]
                    comment_detail=d.find('.mt10.colorA7').text()
                    res_temp=[product_sn,page_num,comment_person,comment_time,comment_detail]
                    result.append(res_temp)
                    for item in res_temp:
                        print(item)
        title=['product_sn','page_num','comment_person','comment_time','comment_detail']
        # 数据写入csv文件
        writer=My_Csv.Write_Csv(path=r'd:/spider/xtep',name='xtep_commentDetail',title=title,result=result)
        writer.add_title_data()

    def run(self):
        self.get_commentDetail()

# 获取待抓取的产品链接
def get_productHrefList_from_local(file_name='D:/spider/xtep/xtep_productHref.csv'):
    with open(file_name,'r') as temp:
        result=temp.readlines()
        result=result[1:]
    for item in result:
        # 因为本列为唯一一列（即最后一列），后面带有\n,故需做切片操作
        temp=item[:-1]
        queue_for_href_list.put(temp)
        try:
            temp_product_sn=temp.split('sn=')[1]
            if 'diy' in temp_product_sn:
                continue
            else:
                queue_for_comment_productSn.put(temp.split('sn=')[1])
                print(temp_product_sn)
        except:pass

if __name__=='__main__':
    t=time.time()

    # # 抓取产品链接
    # Get_productHref().get_productHref()
    queue_for_href_list=Queue(0)
    queue_for_result=Queue(0)
    queue_for_comment_productSn=Queue(0)
    # 取得待抓取链接
    get_productHrefList_from_local()
    # 抓取产品详情信息
    # 配置项：开启线程数
    # thread_count=20
    # Get_productInfo_thread=[]
    # for i in range(thread_count):
    #     Get_productInfo_thread.append(Get_productInfo())
    # for item in Get_productInfo_thread:
    #     item.start()
    # for item in Get_productInfo_thread:
    #     item.join()

    # test
    # Get_productInfo().start()

    # 结果持久化
    # 结果提取及标题处理
    result=[]
    for i in range(queue_for_result.qsize()):
        result.append(queue_for_result.get())
    title=['title','price','price_original','product_sn','sale','jifeng','color','size']
    # 数据写入csv文件
    writer=My_Csv.Write_Csv(path=r'd:/spider/xtep',name='xtep_productInfoDetail',title=title,result=result)
    writer.add_title_data()

    # 评论抓取
    # 获取产品编码：product_sn
    # product_sn_list=[]
    # with open('D:/spider/xtep/xtep_productInfoDetail_2015-08-16 22_03_24.csv','r') as temp_file:
    #     reader=csv.reader(temp_file)
    #     for row in reader:
    #         product_sn_list.append(row[3])
    # product_sn_list=product_sn_list[1:]
    # product_sn_list=[int(item) for item in product_sn_list]
    # print(product_sn_list)

    # 抓取评论详细信息
    # 配置线程数
    thread_count_comment=10
    Get_commentDetail_thread=[]
    for i in range(thread_count_comment):
        Get_commentDetail_thread.append(Get_commentDetail())
    for item in Get_commentDetail_thread:
        item.start()
    for item in Get_commentDetail_thread:
        item.join()

    print('*'*20+u'程序运行完毕，请检查数据'+'*'*20)

    t=time.time()-t
    print('*'*16+u'总计耗时：%f 秒'+'*'*16)%t