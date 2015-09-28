#coding:utf-8
__author__ = '613108'

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from pyquery import PyQuery as pq
from threading import Thread
from Queue import Queue
import sys,time,random
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append(r'C:\Users\Administrator\Desktop\Project\tool_self')
import My_Csv,my_proxy,list_split

def get_info():
    driver=webdriver.PhantomJS()
    driver.get('http://www.361sport.com/')
    frames_1=driver.find_elements_by_css_selector('.mainlevel')[:-2]
    for item in frames_1:
        ActionChains(driver).move_to_element(item).perform()
    page_src=driver.page_source
    driver.quit()
    d=pq(page_src)
    # 只需选取其中三个主题【男子、女子、儿童】
    frames_1=d.find('.mainlevel')[:-2]
    title=['series_1','series_2','product_series','product_href']
    result=[]
    for item in frames_1:
        d=pq(item)
        series_1=d.find('.dd').text()
        frames_2=d.find('dl')[1:-1]
        for item_i in frames_2:
            d_i=pq(item_i)
            series_2=d_i('dt').text()
            frames_3=d_i('dd a')
            for item_i_i in frames_3:
                product_series=pq(item_i_i).text()
                product_href='http://www.361sport.com'+pq(item_i_i).attr('href')
                result.append([series_1,series_2,product_series,product_href])
    return result

# 网址生成
def gen_url(url_original='http://www.361sport.com/index.php?m=Product&a=index&p=',
            page_count=68):
    temp=url_original
    url_list=[]
    for i in range(page_count):
        url_list.append(temp+str(i+1))
    return url_list

class Get_productInfo(Thread):
    def __init__(self,url_list):
        Thread.__init__(self)
        self.url_list=url_list

    def get_info(self):
        for url in self.url_list:
            # url赋值仅测试代码使用
            # url='http://www.361sport.com/index.php?m=Product&a=index&p=1'
            d=pq(url)
            frames=d.find('.prl_c')
            for item in frames:
                d=pq(item)
                title=d.find('.title').text()
                price=d.find('.prl_des').my_text()[0][1:]
                price_original=d.find('.prl_des font').text()[1:]
                product_href='http://www.361sport.com'+d.find('#masterMap').attr('href')
                color_count=d.find('.prl_color').text()
                temp=[title,price,price_original,color_count,product_href]
                queue_for_result.put(temp)
                print(temp)
            time.sleep(abs(random.gauss(4,1)))

    def run(self):
        print('begin')
        self.get_info()

if __name__=='__main__':
    queue_for_result=Queue(0)
    # 网址生成
    url_list=gen_url()
    # 配置线程数
    thread_count=10
    url_list=list_split.list_split(url_list,thread_count)

    Get_productInfo_thread=[]
    for item in url_list:
        Get_productInfo_thread.append(Get_productInfo(url_list=item))
    for item in Get_productInfo_thread:
        item.start()
    for item in Get_productInfo_thread:
        item.join()

    # 结果持久化
    # 结果提取及标题处理
    result=[]
    for i in range(queue_for_result.qsize()):
        result.append(queue_for_result.get())
    title=['product_title','price','price_original','color_count','product_href']
    # 数据写入csv文件
    writer=My_Csv.Write_Csv(path=r'd:/spider/361du',name='361du_productHref',title=title,result=result)
    writer.add_title_data()