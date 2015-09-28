#coding:utf-8
__author__ = 'Administrator'
from selenium import webdriver
import time

def login(send_driver):
    # url='https://login.taobao.com/member/login.jhtml?' \
    #     'style=b2b&from=b2b&full_redirect=true&redirect_url=https%3A%2F%2F' \
    #     'login.1688.com%2Fmember%2Fjump.htm%3Ftarget%3Dhttp%253A%252F%252F' \
    #     'login.1688.com%252Fmember%252FmarketSigninJump.htm%253FDone%253D' \
    #     'http%25253A%25252F%25252Fmember.1688.com%25252Fmember%25252F' \
    #     'operations%25252Fmember_operations_jump_engine.htm%25253F' \
    #     'tracelog%25253Dlogin%252526operSceneId%25253Dafter_pass_from_taobao%252526' \
    #     'defaultTarget%25253Dhttp%2525253A%2525252F%2525252F' \
    #     'work.1688.com%2525252F%2525253Ftracelog%2525253Dlogin_target_is_blank_1688&' \
    #     'reg=http%3A%2F%2Fmember.1688.com%2Fmember%2Fjoin%2Fenterprise_join.htm%3F' \
    #     'lead%3Dhttp%253A%252F%252Fmember.1688.com%252Fmember%252Foperations%252F' \
    #     'member_operations_jump_engine.htm%253Ftracelog%253Dlogin%2526operSceneId%253D' \
    #     'after_pass_from_taobao%2526defaultTarget%253Dhttp%25253A%25252F%25252F' \
    #     'work.1688.com%25252F%25253Ftracelog%25253Dlogin_target_is_blank_1688%26leadUrl%3D' \
    #     'http%253A%252F%252Fmember.1688.com%252Fmember%252Foperations%252F' \
    #     'member_operations_jump_engine.htm%253Ftracelog%253Dlogin%2526operSceneId%253D' \
    #     'after_pass_from_taobao%2526defaultTarget%253Dhttp%25253A%25252F%25252F' \
    #     'work.1688.com%25252F%25253Ftracelog%25253Dlogin_target_is_blank_1688%26' \
    #     'tracelog%3Dmember_signout_signin_s_reg%22%20allowtransparency=%22true%22%20b' \
    #     'order=%220%22%20scrolling=%22no%22%20data-spm-act-id=%22a261o.2206477.5817989.i1.P059Hh'
    url="""https://login.taobao.com/member/login.jhtml?style=b2b&from=b2b&full_redirect=true&redirect_url=https%3A%2F%2Flogin.1688.com%2Fmember%2Fjump.htm%3Ftarget%3Dhttp%253A%252F%252Flogin.1688.com%252Fmember%252FmarketSigninJump.htm%253FDone%253Dhttp%25253A%25252F%25252Fwww.1688.com%25252F&reg=http%3A%2F%2Fmember.1688.com%2Fmember%2Fjoin%2Fenterprise_join.htm%3Flead%3Dhttp%253A%252F%252Fwww.1688.com%252F%26leadUrl%3Dhttp%253A%252F%252Fwww.1688.com%252F%26tracelog%3Dnotracelog_s_reg"""
    driver=send_driver
    driver.get(url)
    driver.maximize_window()
    driver.find_element_by_css_selector('#TPL_username_1').clear()
    # driver.find_element_by_css_selector('#TPL_username_1').send_keys('15035159221')
    # driver.find_element_by_css_selector('#TPL_password_1').send_keys('cjy911027.')
    driver.find_element_by_css_selector('#TPL_username_1').send_keys('piding1986')
    driver.find_element_by_css_selector('#TPL_password_1').send_keys('ysy20101108')
    time.sleep(3)
    driver.find_element_by_css_selector('#J_SubmitStatic').click()
    if driver.title==u'买家成长中心':
        print(u'登录成功，返回浏览器！')
    time.sleep(20)
    return driver

if __name__=='__main__':
    driver=webdriver.Firefox()
    login(driver)