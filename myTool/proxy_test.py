import requests
import json
import re

patt_ip = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')


def original_ip_address():
    t = requests.get('http://httpbin.org/ip').text
    return json.loads(t).get('origin')


original = original_ip_address()


def test(proxy, port=None, timeout=1):
    """
    proxy_test the given proxy and port is ok,return true fo false
    :param proxy: ip address ; like '10.1.12.117' ; it can be given like this '10.1.12.117:8080'
    :param port:  port ; like '8080'
    :param timeout: time out setting , type is int
    :return: True or False

    Usage:
    test(proxy=12.1.1.113,port=9090,timeout=1)
    or
    test(proxy='12.1.1.1:8080')
    """

    if ':' in proxy:
        proxy_port = proxy
    elif port is None:
        print """the port is not given , please check"""
        raise
    else:
        proxy_port = str(proxy) + str(port)

    s = requests.Session()
    proxy_OK = {'http': 'http://%s' % proxy_port}
    try:
        res = s.get('http://httpbin.org/ip', proxies=proxy_OK, timeout=timeout)
    except Exception, e:
        # print e.message
        return False

    ip_return = re.findall(patt_ip, res.text)
    if ip_return \
            and proxy.split(':')[0] == ip_return[0] \
            and len(ip_return) == 1 \
            and original not in ip_return \
            and len(res.text) < 100:
        return True

    return False
