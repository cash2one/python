#coding:utf-8
__author__ = '613108'

from selenium import webdriver
import time

temp=('27.202.44.239','80')
f=open('d:/test1.pac','w')
f.write('''function FindProxyForURL(url, host) {return "%s:%s";}'''%temp)
f.close()
f=open('d:/test1.pac','r')
print(f.read())
f.close()

temp=('117.165.100.107','8123')
f=open('d:/test2.pac','w')
f.write('''function FindProxyForURL(url, host) {return "%s:%s";}'''%temp)
f.close()
f=open('d:/test2.pac','r')
print(f.read())
f.close()

proxy_t1=webdriver.FirefoxProfile()
proxy_t1.set_preference("network.proxy.type",2)
proxy_t1.set_preference('network.proxy.autoconfig_url','file:///d:/test1.pac')
proxy_t1.update_preferences()
proxy_t2=webdriver.FirefoxProfile()
proxy_t2.set_preference("network.proxy.type",2)
proxy_t2.set_preference('network.proxy.autoconfig_url','file:///d:/test2.pac')
proxy_t2.update_preferences()
driver1=webdriver.Firefox(proxy_t1)
driver2=webdriver.Firefox(proxy_t2)

for i in range(100):
    driver1.get('http://www.baidu.com')
    time.sleep(20)
    driver2.get('http://www.baidu.com')
    time.sleep(20)
    print(driver1.title)