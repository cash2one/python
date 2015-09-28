#coding:utf-8
__author__ = 'Administrator'

from selenium import webdriver
import time,sys
reload(sys)
sys.setdefaultencoding('utf-8')

def get_cookie():
    driver=webdriver.Chrome()
    driver.delete_all_cookies()
    driver.get('http://www.tmall.com')
    driver.maximize_window()
    time.sleep(30)
    cookie=driver.get_cookies()
    return cookie

def logoin():
    # cookie=[{u'domain': u'login.tmall.com', u'secure': False, u'value': u'dw:1920&dh:1080&pw:1920&ph:1080&ist:0', u'expiry': 1754667656, u'path': u'/', u'name': u'_med'}, {u'domain': u'.tmall.com', u'secure': False, u'value': u'wAVRDh9qdH4CAdOUVhRR+ixx', u'expiry': 1754667657.67684, u'path': u'/', u'name': u'cna'}, {u'path': u'/', u'domain': u'.tmall.com', u'name': u'_tb_token_', u'value': u'0ak7TGKMYsk872', u'secure': False}, {u'path': u'/', u'domain': u'.tmall.com', u'name': u'ck1', u'value': u'', u'secure': False}, {u'path': u'/', u'domain': u'.tmall.com', u'name': u'uc1', u'value': u'lltime=1439307219&cookie14=UoW0G1luJ4PAyA%3D%3D&existShop=false&cookie16=UtASsssmPlP%2Ff1IHDsDaPRu%2BPw%3D%3D&cookie21=UIHiLt3xSifiVqTG1qWRUQ%3D%3D&tag=3&cookie15=VFC%2FuZ9ayeYq2g%3D%3D&pas=0', u'secure': False}, {u'path': u'/', u'domain': u'.tmall.com', u'name': u'uc3', u'value': u'nk2=E63ChZhE9WfMhA%3D%3D&id2=VWn6Utf5&vt3=F8dASM72HaNn1dN3Kug%3D&lg2=UIHiLt3xD8xYTw%3D%3D', u'secure': False}, {u'path': u'/', u'domain': u'.tmall.com', u'name': u'lgc', u'value': u'piding1986', u'secure': False}, {u'path': u'/', u'domain': u'.tmall.com', u'name': u'tracknick', u'value': u'piding1986', u'secure': False}, {u'path': u'/', u'domain': u'.tmall.com', u'name': u'cookie2', u'value': u'1cebf0b06a69b545d03f62f4cc85c0f8', u'secure': False}, {u'path': u'/', u'domain': u'.tmall.com', u'name': u'cookie1', u'value': u'WvnRVeYpFaoDXVkrLtf3DaF72I7qhj53eoiTDvBGC%2FI%3D', u'secure': False}, {u'path': u'/', u'domain': u'.tmall.com', u'name': u'unb', u'value': u'666826', u'secure': False}, {u'path': u'/', u'domain': u'.tmall.com', u'name': u't', u'value': u'f381980e75149b0c220f20ad6179d3f2', u'secure': False}, {u'path': u'/', u'domain': u'.tmall.com', u'name': u'skt', u'value': u'2874e0aa97a3629e', u'secure': False}, {u'path': u'/', u'domain': u'.tmall.com', u'name': u'_nk_', u'value': u'piding1986', u'secure': False}, {u'path': u'/', u'domain': u'.tmall.com', u'name': u'_l_g_', u'value': u'Ug%3D%3D', u'secure': False}, {u'path': u'/', u'domain': u'.tmall.com', u'name': u'cookie17', u'value': u'VWn6Utf5', u'secure': False}, {u'domain': u'.tmall.com', u'secure': False, u'value': u'', u'expiry': 1441899671.26321, u'path': u'/', u'name': u'hng'}, {u'path': u'/', u'domain': u'.tmall.com', u'name': u'login', u'value': u'true', u'secure': False}, {u'domain': u'www.tmall.com', u'secure': False, u'value': u'ccp%3D0', u'expiry': 1470843673, u'path': u'/', u'name': u'cq'}, {u'domain': u'.tmall.com', u'secure': False, u'value': u'AqioDd7VWKcbNhDPEslxWdE3-Ji60Azb', u'expiry': 1896134400, u'path': u'/', u'name': u'l'}, {u'domain': u'.tmall.com', u'secure': False, u'value': u'9FA71C950216D3BE37E980925998E4BE', u'expiry': 1441899687, u'path': u'/', u'name': u'isg'}, {u'domain': u'.mmstat.com', u'secure': False, u'value': u'wAVRDh9qdH4CAdOUVhRR+ixx', u'expiry': 1754667657.3283, u'path': u'/', u'name': u'cna'}, {u'path': u'/', u'domain': u'.mmstat.com', u'name': u'sca', u'value': u'19378222', u'secure': False}, {u'domain': u'.mmstat.com', u'secure': False, u'value': u'666826', u'expiry': 1754667671.66944, u'path': u'/', u'name': u'cnaui'}, {u'path': u'/', u'domain': u'.mmstat.com', u'name': u'tbsa', u'value': u'b399d08ccd74fbbb100e5307_1439307726_4', u'secure': False}, {u'domain': u'.mmstat.com', u'secure': False, u'value': u'666826', u'expiry': 1754667686.76766, u'path': u'/', u'name': u'aui'}, {u'domain': u'.mmstat.com', u'secure': False, u'value': u'2a900de68f5a97cfd0fda2d4_1439307741', u'expiry': 1754667686.76778, u'path': u'/', u'name': u'atpsida'}]
    # cookie=get_cookie()
    cookie=[{u'domain': u'.tmall.com', u'secure': False, u'value': u'+w1RDvN7UkcCAdOUVhRznhPI', u'expiry': 1754669765.09625, u'path': u'/', u'name': u'cna'}
            ,{u'domain': u'login.tmall.com', u'secure': False, u'value': u'dw:1920&dh:1080&pw:1920&ph:1080&ist:0', u'expiry': 1754669778, u'path': u'/', u'name': u'_med'}
            ,{u'domain': u'.tmall.com', u'secure': False, u'value': u'Al1daZz-7uxzouXQj9LcLkxf7TdXepHM', u'expiry': 1896134400, u'path': u'/', u'name': u'l'}
            ,{u'domain': u'.tmall.com', u'secure': False, u'value': u'CA68801B899E30BC23997ED9FB968434', u'expiry': 1441901798, u'path': u'/', u'name': u'isg'}
            ,{u'domain': u'login.taobao.com', u'secure': False, u'value': u'ED0C8356A3E0CCB84B4315392C12F5062728D680AF952E924B0F883556A02D9AE447CCBEC050E73A2F688FC37AA0F9AD87F3E0737B2B005D1CF815FF6961024BE8B733844DE112F2', u'expiry': 1470845784, u'path': u'/member', u'name': u'_umdata'}
            ,{u'domain': u'.taobao.com', u'secure': False, u'value': u'cn', u'expiry': 1470845764.48641, u'path': u'/', u'name': u'thw'}
            ,{u'path': u'/', u'domain': u'.taobao.com', u'name': u'v', u'value': u'0', u'secure': False}
            ,{u'path': u'/', u'domain': u'.taobao.com', u'name': u'_tb_token_', u'value': u'4hgNRxH6DhWXp8', u'secure': False}
            ,{u'domain': u'.taobao.com', u'secure': False, u'value': u'1E9E267B72A06C98421D3075531B5A07', u'expiry': 1441901798, u'path': u'/', u'name': u'isg'}
            ,{u'path': u'/', u'domain': u'.taobao.com', u'name': u'uc1', u'value': u'lltime=1439309528&cookie14=UoW0G1luKaWj2g%3D%3D&existShop=false&cookie16=V32FPkk%2FxXMk5UvIbNtImtMfJQ%3D%3D&cookie21=WqG3DMC9EdFmJgkfqj2c3Q%3D%3D&tag=3&cookie15=V32FPkk%2Fw0dUvg%3D%3D&pas=0', u'secure': False}
            ,{u'domain': u'.taobao.com', u'secure': False, u'value': u'nk2=E63ChZhE9WfMhA%3D%3D&id2=VWn6Utf5&vt3=F8dASM73AC7KR9BB%2FFs%3D&lg2=VFC%2FuZ9ayeYq2g%3D%3D', u'expiry': 1441901798.7521398, u'path': u'/', u'name': u'uc3'}
            ,{u'path': u'/', u'domain': u'.taobao.com', u'name': u'existShop', u'value': u'MTQzOTMwOTg1Mw%3D%3D', u'secure': False}
            ,{u'domain': u'.login.taobao.com', u'secure': False, u'value': u'piding1986', u'expiry': 1470845798.7525601, u'path': u'/', u'name': u'lid'}
            ,{u'domain': u'.taobao.com', u'secure': False, u'value': u'piding1986', u'expiry': 1441901798.75278, u'path': u'/', u'name': u'lgc'}
            ,{u'domain': u'.taobao.com', u'secure': False, u'value': u'piding1986', u'expiry': 1470845798.75294, u'path': u'/', u'name': u'tracknick'}
            ,{u'path': u'/', u'domain': u'.taobao.com', u'name': u'sg', u'value': u'667', u'secure': False}
            ,{u'path': u'/', u'domain': u'.taobao.com', u'name': u'cookie2', u'value': u'1c1b0097f529b045fed27e597c7e2811', u'secure': False}
            ,{u'domain': u'.taobao.com', u'secure': False, u'value': u'np=', u'expiry': 1439914598.75332, u'path': u'/', u'name': u'mt'}
            ,{u'path': u'/', u'domain': u'.taobao.com', u'name': u'cookie1', u'value': u'WvnRVeYpFaoDXVkrLtf3DaF72I7qhj53eoiTDvBGC%2FI%3D', u'secure': False}
            ,{u'path': u'/', u'domain': u'.taobao.com', u'name': u'unb', u'value': u'666826', u'secure': False}
            ,{u'path': u'/', u'domain': u'.taobao.com', u'name': u'skt', u'value': u'74058b8542c08576', u'secure': True}
            ,{u'domain': u'.taobao.com', u'secure': False, u'value': u'f650796e966f38cafd2a524641cdac62', u'expiry': 1447085798.75407, u'path': u'/', u'name': u't'}
            ,{u'path': u'/', u'domain': u'.taobao.com', u'name': u'publishItemObj', u'value': u'Ng%3D%3D', u'secure': False}
            ,{u'domain': u'.taobao.com', u'secure': False, u'value': u'UtASsssmfA%3D%3D', u'expiry': 1470845798.75439, u'path': u'/', u'name': u'_cc_'}
            ,{u'domain': u'.taobao.com', u'secure': False, u'value': u'0', u'expiry': 1493309798.75788, u'path': u'/', u'name': u'tg'}
            ,{u'path': u'/', u'domain': u'.taobao.com', u'name': u'_l_g_', u'value': u'Ug%3D%3D', u'secure': False}
            ,{u'path': u'/', u'domain': u'.taobao.com', u'name': u'_nk_', u'value': u'piding1986', u'secure': False}
            ,{u'path': u'/', u'domain': u'.taobao.com', u'name': u'cookie17', u'value': u'VWn6Utf5', u'secure': False}
            ,{u'domain': u'.login.taobao.com', u'secure': False, u'value': u'Vy0SMMOI%2BWzBFGIQtGUJ', u'expiry': 1441901798.75871, u'path': u'/', u'name': u'lc'}
            ,{u'domain': u'.taobao.com', u'secure': False, u'value': u'ApSUR/ZsD3DyVnyL3mUFxU3v5NwGyLjX', u'expiry': 1896134400, u'path': u'/', u'name': u'l'}]
    driver=webdriver.Chrome()
    driver.get('http://www.tmall.com')
    for item in cookie:
        print(item)
        driver.add_cookie(item)
    driver.refresh()
    # time.sleep(10)
    # driver.get('http://www.tmall.com')
    driver.maximize_window()

if __name__=='__main__':
    logoin()