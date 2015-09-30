# coding:utf8
__author__ = 'Administrator'
import time
# from ProxySupporter import ProxySupporter

# psu = ProxySupporter()
# res = psu.gather()
# with open('proxyTemp.txt', 'wb') as f:
#     for item in res:
#         f.write(item)
#         f.write('\n')
#         print(item)



def proxyTest(threadCount=300):
    import urllib2
    from Queue import Queue
    from threading import Thread

    proxyList = []
    queueForProxyTest = Queue(0)
    queueForProxyOk = Queue(0)

    with open('proxyTemp.txt', 'r') as f:
        for row in f:
            if len(row) <= 22 & len(row) > 11:
                proxyList.append(row.split('\n')[0])
                queueForProxyTest.put(row.split('\n')[0])

    class ProxyTestInner(Thread):
        def __init__(self):
            Thread.__init__(self)

        def test(self):
            while queueForProxyTest.qsize() > 0:
                p = queueForProxyTest.get()
                proxyHandler = urllib2.ProxyHandler({'http': r'http://%s' % p})
                userAgent = 'Mozilla/5.0 (Windows NT 5.2) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30'
                opener = urllib2.build_opener(proxyHandler)
                opener.addheaders = [('User-agent', userAgent)]
                try:
                    temp = opener.open(fullurl='http://www.baidu.com', timeout=3)
                    src = temp.read()
                    temp.close()
                    queueForProxyOk.put(p)
                except:
                    pass

        def run(self):
            self.test()

    testThread = []
    for i in range(threadCount):
        testThread.append(ProxyTestInner())
    for item in testThread:
        item.setDaemon(True)
        item.start()
        # for item in testThread:
        #     item.join()
    return queueForProxyOk


if __name__ == '__main__':
    que=proxyTest(threadCount=300)
    time.sleep(300)
    while que.qsize()>0:
        print(que.get())
    print('-----OK-----')
