# coding:utf-8
__author__ = 'Administrator'
import urllib2, random, cookielib, time
from pyquery import PyQuery as pq

# sys.path.append(r'C:\Users\613108\Desktop\Project\myTool')
import myProxy

def forRequest():
    global proxyExistsAll
    proxyExistsAll=myProxy.proxyExistsAll()

forRequest()

def requestByProxy(url):
    # forRequest()

    i = 0
    src = ''
    proxy_port = myProxy.proxyExistsAll()
    x=random.randint(0,len(proxy_port)-1)
    proxy = proxy_port[x]
    # print(proxy[0])
    proxy = proxy[0] + ':' + proxy[1]
    # print(proxy)
    # print('=' * 5 + u'开始使用的代理：' + 'http://%s' % proxy)
    proxyHandler = urllib2.ProxyHandler({'http': r'http://%s' % proxy})

    cookies = urllib2.HTTPCookieProcessor
    opener = urllib2.build_opener(cookies, proxyHandler)
    # opener = urllib2.build_opener(proxyHandler)
    userAgentList = [['chrome',
                      'Mozilla/5.0 (Windows NT 5.2) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30'],
                     ['Firefox', 'Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0'],
                     ['IE8',
                      'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)'],
                     ['IE9',
                      'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)'],
                     ['Opera', 'Opera/9.80 (Windows NT 5.1; U; zh-cn) Presto/2.9.168 Version/11.50'],
                     ['360 safe Browser in IE8',
                      'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)'],
                     ['Safari',
                      'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1'],
                     ['Maxthon',
                      'Mozilla/5.0 (Windows; U; Windows NT 5.1; ) AppleWebKit/534.12 (KHTML, like Gecko) Maxthon/3.0 Safari/534.12']]
    opener.addheaders = [
        ('User-agent', random.sample(userAgentList, 1)[0][1])]
    count = 1
    src=''
    while i == 0:
        try:
            res_temp = opener.open(url)
            src = res_temp.read()
            res_temp.close()
            # d = pq(src)
            # d.find('title')
            # if d.find('title').text() == u'淘宝网 - 淘！我喜欢':
            #     # time.sleep(abs(random.gauss(1, 1)))
            #     raise Exception
            i += 1
        except:
            count+=1
            # 如若尝试超过5次均无法连接成功，则抛弃
            if count>5:
                print('drop:'+url)
                break
            # proxy = random.sample(proxy_port, 1)[0]
            proxy = proxy_port[random.randint(0,len(proxy_port)-1)]
            print(u'更换代理：%s:%s' % (proxy[0], proxy[1]))
            proxy = proxy[0] + ':' + proxy[1]
            proxyHandler = urllib2.ProxyHandler({'http': r'http://%s' % proxy})
            opener = ''
            opener = urllib2.build_opener(cookies, proxyHandler)
            # opener = urllib2.build_opener(proxyHandler)
            continue
    return src


def requestByProxyAddReferer(url, refererUrl):
    forRequest()

    i = 0
    src = ''
    proxy_port = proxyExistsAll
    proxy = proxy_port[random.randint(0,len(proxy_port)-1)]
    proxy = proxy[0] + ':' + proxy[1]
    # print(proxy)
    print('=' * 5 + u'开始使用的代理：' + 'http://%s' % proxy)
    proxyHandler = urllib2.ProxyHandler({'http': r'http://%s' % proxy})

    c = cookielib.LWPCookieJar()
    cookies = urllib2.HTTPCookieProcessor(c)
    opener = urllib2.build_opener(cookies, proxyHandler)
    opener = urllib2.build_opener(proxyHandler)
    userAgentList = [['chrome',
                      'Mozilla/5.0 (Windows NT 5.2) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30'],
                     ['Firefox', 'Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0'],
                     ['IE8',
                      'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)'],
                     ['IE9',
                      'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)'],
                     ['Opera', 'Opera/9.80 (Windows NT 5.1; U; zh-cn) Presto/2.9.168 Version/11.50'],
                     ['360 safe Browser in IE8',
                      'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)'],
                     ['Safari',
                      'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1'],
                     ['Maxthon',
                      'Mozilla/5.0 (Windows; U; Windows NT 5.1; ) AppleWebKit/534.12 (KHTML, like Gecko) Maxthon/3.0 Safari/534.12']]
    userAgentListMobile = [['Android QQ浏览器 For android',
                            'MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'],
                           ['Android UC For android',
                            'JUC (Linux; U; 2.3.7; zh-cn; MB200; 1080*1920) UCWEB7.9.3.103/139/999'],
                           ['iPad',
                            'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10'],
                           ['Windows Phone Mango',
                            'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)']]
    # userAgentList = userAgentListMobile
    opener.addheaders = [
        ('User-agent', random.sample(userAgentList, 1)[0][1]),
        ('Host', 'list.tmall.com'),
        ('Referer', refererUrl),
        ('Connection', 'keep-alive')]
    while i == 0:
        try:
            res_temp = opener.open(url)
            src = res_temp.read()
            res_temp.close()
            i += 1
        except:
            proxy = proxy_port[random.randint(0,len(proxy_port)-1)]
            print(u'更换代理：%s:%s' % (proxy[0], proxy[1]))
            proxy = proxy[0] + ':' + proxy[1]
            proxyHandler = urllib2.ProxyHandler({'http': r'http://%s' % proxy})
            # opener = urllib2.build_opener(cookies, proxyHandler)
            opener = urllib2.build_opener(proxyHandler)
            continue
    return src


if __name__ == '__main__':
    # requestByProxyAddReferer(url='http://www.baidu.com', refererUrl='http://www.hao123.com')
    # forRequest()

    import re
    ip_regex = re.compile("(([0-9]{1,3}\.){3}[0-9]{1,3})")
    count=1
    for i in range(100):
        print('*'*80)
        temp=ip_regex.findall(requestByProxy('http://1111.ip138.com/ic.asp'))[0][0]
        print(temp)
        if temp=='183.12.65.53':
            count+=1
    print(count)