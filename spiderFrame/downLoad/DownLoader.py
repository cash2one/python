# coding:utf8
__author__ = 'Administrator'
"""
类说明：
仅提供源码下载功能（不作任何分析）
"""


# noinspection PyPep8Naming,PyBroadException,PyPep8
class DownLoader:
    def __init__(self, url):
        self.url = url
        self.proxyPool = None
        self.pageSource = None

    def urllib2(self):
        """
        # 使用基本类库，适用于简单网页（网页不需js等渲染即包含待抓取信息）
        :return:
        """
        import urllib2

        temp = urllib2.urlopen(self.url)
        src = temp.read()
        temp.close()
        self.pageSource = src
        return src

    def highOrderUrllib2(self, proxyOption=1, tryCount=5):
        """
        # 高阶下载器，适用于频繁抓取（以防IP被封杀）
        # proxyOption:是否使用代理，默认使用代理
        # tryCount:重试次数，默认重试5次
        :return:
        """
        import urllib2, random

        cookies = urllib2.HTTPCookieProcessor

        def proxyHandler():
            """
            # 返回代理列表，构建代理池
            """
            from myTool import myProxy

            if proxyOption:
                if not self.proxyPool:
                    proxyPool = myProxy.proxyExistsAll()
                    self.proxyPool = [[item[0], item[1]] for item in proxyPool]
            proxy = random.sample(self.proxyPool, 1)[0]
            proxy = proxy[0] + ':' + proxy[1]
            return urllib2.ProxyHandler({'http': r'http://%s' % proxy})

        def returnUserAgent():
            userAgentList = \
                [['chrome',
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
            userAgent = random.sample(userAgentList, 1)
            return userAgent[0][1]

        def returnOpener():
            if proxyOption:
                openerInner = urllib2.build_opener(cookies, proxyHandler())
            else:
                openerInner = urllib2.build_opener(cookies)
            openerInner.addheaders = [('User-agent', returnUserAgent())]
            return openerInner

        opener = returnOpener()
        src = None
        while tryCount >= 1:
            try:
                res_temp = opener.open(self.url)
                src = res_temp.read()
                res_temp.close()
                break
            except:
                tryCount -= 1
                opener = returnOpener()
        if not src:
            print('drop:' + self.url)
        self.pageSource = src
        return src

    def selenium(self, webdriverOption=0):
        """
        # 调用浏览器下载，适用于任何情形
        :return:
        """
        if not self.url[:4] == 'http':
            return None

        driver = None
        if webdriverOption == 0:
            from selenium.webdriver import PhantomJS

            driver = PhantomJS()
        elif webdriverOption == 1:
            from  selenium.webdriver import Chrome

            driver = Chrome()
        elif webdriverOption == 2:
            from selenium.webdriver import Firefox

            driver = Firefox()

        if not driver:
            print(u'-->DownLoader->Selenium driver初始化出错，请检查运行环境或webdriverOption选项')

        driver.get(self.url)
        src = driver.page_source
        driver.quit()
        self.pageSource = src
        return src

    def getPageSource(self):
        """
        # 推荐使用本方法返回源码
        # 返回源码,自动选择highOrderUrllib2方法或selenium方法；保证能返回页面源码信息
        :return:
        """
        src = self.highOrderUrllib2()
        if not src:
            src = self.selenium()
        return (self.url, src)

    def getHttpCode(self):
        """
        返回状态码，用于判断是否成功访问
        :return:
        """
        pass

    def getHttpHeader(self):
        """
        返回网页表
        :return:
        """
        pass
