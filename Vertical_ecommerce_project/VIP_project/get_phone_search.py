#coding:utf-8
__author__ = '613108'

from selenium import webdriver
from threading import Thread
import time
from Queue import Queue
import xlrd
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append(r'C:\Users\613108\Desktop\Project\tool_self')
import My_Csv,list_split

class Get_phoneaddr(Thread):
    def __init__(self,com_list):
        Thread.__init__(self)
        self.com_list=com_list

    def get_info(self):
        driver=self.web_site()
        for item in self.com_list:
            try:
                driver.find_element_by_css_selector('#upquery').clear()
                driver.find_element_by_css_selector('#upquery').send_keys(item)
                driver.find_element_by_css_selector('#searchBtn').click()
                frames=driver.find_elements_by_css_selector('.joblist>tbody>tr')[1:]
                result=[self.get_result(frame=temp) for temp in frames]
                result_temp=[item for i in result for item in i]
                print(result_temp[1])
                if result[0]:
                    for temp in result:
                        try:print(temp)
                        except:pass
                    queue_result.put([item]+result)
                else:pass
            except:pass
        driver.quit()

    def web_site(self,url_temp='http://www.sogou.com/zhaopin',css_searchbox='#query',
                 css_submit='#stb',keyword=u'北京旺佳富鑫科技发展有限公司'):
        # 参数默认为搜狗招聘
        # driver=webdriver.PhantomJS()
        driver=webdriver.Chrome()
        # driver=webdriver.Firefox()
        driver.maximize_window()
        driver.get(url_temp)
        driver.find_element_by_css_selector(css_searchbox).clear()
        driver.find_element_by_css_selector(css_searchbox).send_keys(keyword)
        driver.find_element_by_css_selector(css_submit).click()
        # 返回浏览窗口
        time.sleep(1)
        return driver

    def get_result(self,frame,css_text='td:nth-child(2)>a>em',css_detail='td:nth-child(1)>h2>a',
             css_href='td:nth-child(1)>h2>a',css_city='td:nth-child(3)',
             css_source='td:nth-child(5)>a'):
        # css_text:公司名称，用于判断是否为待查找公司
        # css_detail:职位名称
        # css_href:职位源链接
        # css_city:城市
        # css_source:来源渠道
        spider_time=time.strftime('%Y-%m-%d %X',time.localtime())
        try:
            result=[
                    frame.find_element_by_css_selector(css_text).text,
                    frame.find_element_by_css_selector(css_detail).text,
                    frame.find_element_by_css_selector(css_href).get_attribute('href'),
                    frame.find_element_by_css_selector(css_city).text,
                    frame.find_element_by_css_selector(css_source).text]
            # print frame.find_element_by_css_selector(css_source).text
        except:result=''
        return result

    def run(self):
        self.get_info()

if __name__=='__main__':
    queue_result=Queue(0)
    Get_phoneaddr_thread=[]
    temp_com=xlrd.open_workbook(u'D:/spider/唯品会（VIPShop）商机线索输出_0731.xlsx')
    table=temp_com.sheet_by_index(0)
    arr_com=table.col_values(5)
    arr_com=[item for item in arr_com[1:] if item != u'-']
    temp_arr_com=list_split.list_split(arr_com,2)
    for arr in temp_arr_com:
        print(len(arr))
    for item in temp_arr_com:
        Get_phoneaddr_thread.append(Get_phoneaddr(item))
    for item in Get_phoneaddr_thread:
        item.start()
    for item in Get_phoneaddr_thread:
        item.join()
    result=[]
    for i in range(queue_result.qsize()):
        result.append(queue_result.get())
    result=[item for i in result for item in i]
    writer=My_Csv.Write_Csv(path='D:/spider/vip',name='vip_compang_phoneaddr',result=result)
    writer.add_title_data(title=[])
    print('*'*20+u'程序运行完毕，请检查数据'+'*'*20)