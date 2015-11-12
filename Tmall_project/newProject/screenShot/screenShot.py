# coding:utf8
__author__ = '613108'


def saveScreenShot(url='http://shop115634117.taobao.com', driver=None,title=''):
    from selenium import webdriver
    from selenium.webdriver.common.action_chains import ActionChains
    import time

    if not driver:
        # dri=webdriver.PhantomJS()
        dri = webdriver.Chrome()
    else:
        dri = driver
    dri.get(url)
    dri.maximize_window()
    # try:title = dri.title.split('-')[1]
    # except:title=dri.title
    tm = time.strftime("%Y-%m-%d+%H-%M-%S", time.localtime())
    TITLE = title + '+' + tm + '+BASE'
    time.sleep(2)
    dri.save_screenshot('d:/spider/tmall/screenShot/%s.png' % TITLE)

    try:
        element = dri.find_element_by_xpath(".//*[@class='main-info']/div[1]/div[2]/span")
        ActionChains(dri).move_to_element(element).perform()
        time.sleep(2)

        TITLE = title + '+' + tm + '+DETAIL'
        dri.save_screenshot('d:/spider/tmall/screenShot/%s.png' % TITLE)
    except:pass
    # dri.quit()
    return dri
