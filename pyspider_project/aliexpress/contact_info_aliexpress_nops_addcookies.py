#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on:2016/3/16 14:36
# Project:contact_info_aliexpress
# Author:yangmingsong

from ms_spider_fw.DBSerivce import DBService
import ms_proxy.proxy_collection as pc
import ms_proxy.proxy_test as pt
from pyquery.pyquery import PyQuery
from Queue import Queue, LifoQueue
import requests
import time
import re
import json
import threading
import random

# config_text
db_name = 'alibaba'
table_name = 'contact_info_aliexpress_com'
table_title = 'shop_url,contact_detail,crawl_time'
connect_dict = {
    'host': 'localhost',  # '10.118.187.12',
    'user': 'root',  # 'admin',
    'passwd': "",  # 'admin',
    'charset': 'utf8'
}

# compile regular expression pattern
pattern_contact_info = re.compile('<th>(.+?)</th>.*?<td>(.+?)</td>', re.DOTALL)

proxies_queue = LifoQueue(0)


def proxy_collection():
    # get proxies from website
    proxies_list_website = pc.get_proxies_from_website()
    # at the same time , get other proxies from local database
    table_names_proxies = 'proxy_other_source,proxy_you_dai_li'
    proxies_list_local = list()
    for proxies_t_n in table_names_proxies.split(','):
        dbs = DBService(dbName='base', tableName=proxies_t_n, **connect_dict)
        proxies_list_local += map(lambda x: x[0], dbs.getData(var='proxy_port'))
    return list(set(proxies_list_website + proxies_list_local))
    # first round test proxies


def proxies_test():
    proxies_list_total = proxy_collection()
    while True:
        for proxy in pt.test_from_list(proxies_list_total, 5):
            proxies_queue.put(proxy)


# database link object
db_server = DBService(dbName=db_name, tableName=table_name, **connect_dict)

_headers = {
    'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'
}

_cookie_d = {
    1: """ali_apache_id=101.105.37.177.1438705554786.260685.7; xman_us_f=x_l=1&x_locale=en_US&no_popup_today=n&x_user=US|yang|young|ifm|768474461&last_popup_time=1457712623354; aep_usuc_f=region=US&site=glo&b_locale=en_US&isb=y&isfm=y&c_tp=USD&x_alimid=768474461&reg_ver=new; intl_common_forever=rL5z+pTJEMOqSRr7MKiguZ9Lihf5oTyQRXJT8FtnVwNdRxp5uU1O5Q==; xman_f=6h/npGRCn8PCxoOVd+ue381gNqVAQGBg6f+jrlxyGbjxI6OUURdWZejPr1msspHIQEwM8SJpZNIUm14F+GhdzSfktjgh5/GMO5yA+qU1wD2owvJzr3HKslkoZaZcsKtcNz3AvPuo9SeiXrF7jgd1QXPY/UKDRO0nX4/1v6rGB6aWdfYMKt318vLhWIrmQrZQ4oheJxWqlJvixq92djQGQqnIfqMEtiGiYak3o51oWkCRF4N81S9LxC18FPxXHwjYyIAoUDWv7BVeykIDtRJtbS5sdMne0gc2pupQJx9sdHEJEr3GehcGxdpUJiYRC6lIX+3y8vior2X4xrdYH2agXOY9VFF5GExTbAdNQxhr6oBDhNkL/lM42Ee7JgqXK4tTRVpXQ+XekMIymgMmxR0oVyJ4BNOOlrLb; ali_beacon_id=220.152.150.99.1433075894474.773074.1; cna=PDviDaz2VHICAdyYlirqiemC; __utma=3375712.324010086.1438705507.1458384428.1458388505.11; l=AgAA/C6h38RBbszMOKKq5h4L8IDS7ORb; aep_history=keywords%5E%0Akeywords%09%0A%0Aproduct_selloffer%5E%0Aproduct_selloffer%0932328512449%0932320594174%0932379793562%0932312953658%0932602972005; _umdata=8D5462A7710B16F8D1DE8DF86205FD525C80C1F3E9ED159353D27A988B78E33A486FC569B0FB883C6705A9C6F940A638B43E266F5C7442047DCA4915D89FB7108E94AD13019CB44D; __utmz=3375712.1458388505.11.2.utmcsr=aliexpress.com|utmccn=(referral)|utmcmd=referral|utmcct=/category/200003482/dresses.html; _ga=GA1.2.324010086.1438705507; ali_apache_track=mt=1|ms=|mid=us1149212384ijsz; isg=580CC597EE0CF236F5283A13388FEF5B; d_ab_f=f12887f4ca9643129dfe6be772bb1c8d; aep_common_f=q4D4WHUu8LURVHlV+ZWTmdw4tcu1GZaUE+q0QzAaL+l3PdjHUgygiQ==; JSESSIONID=2848429EB23B3C6BB077C066C1B1923F; acs_usuc_t=acs_rt=243129bb6ae3438c9a9bfc4c59b82a31; xman_t=yPdVpMwygp/1uJRRe/aRCOVu7qxTo0j4NxOaYy1Px7+qxl/YeFLljop+D4dXpySUtoLvePze6njxvzuEHviXYvtqd7EcYDCOUJ+GOEwyBeb/R+fsYaSOILTOMizYulrgJkbq8zl6+RdWiTldpJAiqyIXsyk8bOy0OKfiyjCfT+5NqCvCGraThzyhQiTkQCaNGuHol2OAe5xLIZWKP08FwdjqX9RnxhBLMniaDJNjufN8RukWlkIXAfqxvLLM5Z37a1kIcQ4Uut26XfxPJhpzMod9sv8GNlvNdTibgvAqL5HQHh+MtWevinhVLJX2NtXdM/WVapXaLTjtQf71x7yMwWVFjPF9GE2NXenpinDrg7oRy3oBM7FwYpvqiy28LItoRKlXzL8Xmf/EwsTEpX7IS9Fi0+7Ts6yWhL3+MdA1grGNUsltGr9a5kS/yZiF4MmdUNlbsEp4uAcpjT5gcMyDxXnmDz/RDHHL1ayvGndWISTpF6SNqd6LO+gd76Hm3e+uo6WX3VvNCRWzC/hpZ92mZ2RHOpCuvZvYKKskYSCF3HwoZANaLFIk+g04LqADCTPjQUE+jm1UG/l3VbrhzQ8wkOzdBJ4/cJ29iTj1I67dcgGVs9F795wUOu8Qcux/bnOp; intl_locale=en_US; __utmc=3375712; _mle_tmp0=eNrz4A12DQ729PeL9%2FV3cfUx8KvOTLFSsjQ2dzRxczUyMHI2dXU1dLF0dDV1MXUysDA3M3BydXZS0kkusTI0MbUwtjCxMDMyMDTWSUxGE8itsDKojQIApWsX%2Fw%3D%3D; ali_apache_tracktmp=W_signed=Y; u_info=PzPojPc60gU9BgN7gGdVe/HeSj7zFohb8RmPP904RxI=; __utmb=3375712.7.10.1458388505; xman_us_t=x_lid=us1149212384ijsz&sign=y&x_user=tMwQ8hJci/ZHhxqofsUOYS/G9Uo5udG12uV1XaI35NY=&ctoken=ibova_l11_rq&need_popup=y&l_source=aliexpress; aep_usuc_t=ber_l_fg=A0; __utmt=1; _gat=1""",
    2: """ali_apache_id=10.182.248.30.1458411611442.548448.8; JSESSIONID=F7827C5D1DD88D0352038D7FDD897975; ali_apache_track=mt=1|ms=|mid=us1150986244hdqi; ali_apache_tracktmp=W_signed=Y; xman_us_f=x_l=0&x_locale=en_US&no_popup_today=n&x_user=US|Michael|carter|ifm|769100574&last_popup_time=1458411772766; aep_usuc_f=site=glo&region=US&b_locale=en_US&isb=y&isfm=y&x_alimid=769100574&c_tp=USD&reg_ver=new; acs_usuc_t=acs_rt=6e7ad199dede41b5ad5030ff76db9db7; xman_t=Cw/JlL6kaI8QwR5dSX5euRpeSvGzryHQxYdsmO/xEg+uuYlIcwXDmjXeaobfkNowLh2u/GtMyi52VDO8VhJA30Zvl7S+kCK67PwZlfDh5Aws8QCwRaopAb42QwXGhJWZYJjYzGGRlViJpvFbnG7b1dqOYuI8MLyEaFPMk3rzo0N37rvzD9a3/yZLnHjVDM7raF5ynonzl4Wjf8ZARJ1DqgBptM1r+28r2FHdbXPF86Td5GjHFdWHf5Kydem2pDa8sgE6AUIV8PP8Z0XLvSkae1ll7OxbUVhi+JNq6qnLnxOv94cNeOugNh7490bp3VcYGSk5Bs728MAV8vJzsXQVhfC+gIanwmvxqhiMEj6p6wal5fVvgFvSv2SENR8f83k7jqGw3fVtrLqY6wlKu7z6m/SsV0PxcuuqT3RfKqLAQ6kcN7c/jYHBKvoex7CCJrnjn4D0+ZwZdNrb0S17gTaUyUh8rJIq3CDtsAiso3rRI/Wod/RXEZdHpuPqF5+A4PaUv/p7iyq0ctG5CHv/nNGqlegOuh4s0GG43zgLaSl3i+HF5Q4cjGZc6b4OydKr+TxCi54fifBYNYb8wpInuYwWfW/baccAKA+wUBlq0bhoDyESBtucVNOh2bntMTC1pJfZSUqFqwH3eSs=; intl_locale=en_US; intl_common_forever=gAzWbQmsYxO9a3WWSCHLvGO8CaEgGvY166P9LZnm4YB/xbQ7/fc/bQ==; xman_f=+ccGJh5y6no9uHlB9TweBrTAqNzARoD3fyXqYVcT4popnwww4WG4Ppb/WUSh6TnGmFYz92q0oJJEBHpTkRtAg46vw+BbuOINMA6Gic+mj3xuModVk59a40llTCtXkivODVTwnwuWrCBqARsWpy8ROClBxzgdEbIW5k6chyOrXinHX6dBxljjEzA1vTKm75NMComdvWsq1g3jLE5NZcn4hZvXAE7pxx9lHAbp9AdmXhl2Sqd0iK9TWxm7GTX86UD2FLRixeOcQj+QgM2hJlFvpM3Nq2US2LL64TKk2fqbyMKLxcy4/FaMxWDlJBxpuPp1HRRhYnXs5H9Se1AmQzBTp9/liJnPv450kms2JBs5Yh/i1ldOMn64Qt/P8PjLv8MEuPUNoasGhJQM3jUnIU6+UgCoOlSJcyWf; _ga=GA1.2.1399073401.1458411514; _gat=1; __utma=3375712.1399073401.1458411514.1458411514.1458411514.1; __utmb=3375712.9.9.1458411707204; __utmc=3375712; __utmz=3375712.1458411514.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; ali_beacon_id=10.182.248.30.1458411611442.548448.8; cna=XoZ0D1g4vj0CAUTrOWYOhskd; isg=DB023282D50ECDFD48DA766876E2E92B; l=AqurffV6LUiE3N-dWJuhd6jAG8GVnb9a; aep_common_f=JM6RoNFoOe/g9k9kbbLlcNJQX7oW246Y7J6NHtTDkgIhkFP5QAsyNQ==; xman_us_t=x_lid=us1150986244hdqi&sign=y&x_user=G2g3H72Sn0HuhJKL4k6ObLNn4kYh6Xjsx8VcMdSEAyo=&ctoken=1565ajs278isp&need_popup=y; u_info=yn6XEjZ8lVb7fFgclT6OxijgZifcyAgj+1uU0zrORbg=; aep_usuc_t=ber_l_fg=A0; _mle_tmp0=eNrz4A12DQ729PeL9%2FV3cfUx8KvOTLFScrE0djU2N3ZzNjU3dHN1NjM0drU0MDIzcnNyMrQ0d3NR0kkusTI0MbUwMTS0MDAyMDXVSUxGE8itsDKojQIAoKkX3A%3D%3D; d_ab_f=67f94be10fa84ce9b936b7e325cf5d2f; aep_history=keywords%5E%0Akeywords%09%0A%0Aproduct_selloffer%5E%0Aproduct_selloffer%09828504209""",
    3: """ali_apache_id=174.139.5.221.145841358483.164192.9; ali_apache_track=mt=1|ms=|mid=us1149061838lfln; ali_apache_tracktmp=W_signed=Y; xman_us_f=x_l=0&x_locale=en_US&no_popup_today=n&x_user=US|joshua|eddy|ifm|768809794&last_popup_time=1458413629747; aep_usuc_f=region=US&site=glo&b_locale=en_US&isb=y&isfm=y&c_tp=USD&x_alimid=768809794&reg_ver=new; acs_usuc_t=acs_rt=fb3b1acf1d3645e5a345c6ed9f4b058e; xman_t=hoY9GxrMHHzIPio9Dkobg2rPOxWlxaXmAfRh1TapT82HxPUHPDcDwHGL0oCg39dQbM8RZmqsySyyPvkT8VF5ejsFSzPYBKyw9SIuGZGcQ12D55XOkfUs4zLC2oaykNkoUxDP6ncUpSW0WRFRHyLV/+/4Bt0rCQ3JTH5kimfdLII8//gCCuZgSN+3ubUJFbpC9mLbe37NTJnRAxTFNALBPSeQkr+Kc2MF45l02ftBsz4N7353gTPz2/kFi0PuWJIDiI+3mMYKJkD4FGXcGUXe3r4QtfHem7mG8TQ8LubQCg0z7dvXNafYdn2BJoOCzdpCvcBv/dIWhuBZgdQO35dxBHC5YJRS4XSd5YTM2gOi/qzRCweQWwO+dB0lFT9BOUlQJB7X+dHEgY9MxGGQEUwFdiH+fLG9ZkmV65KBOy1s1PaLPBFj885unWj5Hn/b/hK9F80zttwim6h8NBlB/HwB5cwq4ZA78B8Dypou1U6a4RmrPC6ozepbcBC0kL0dfTilNDyrBF7VuNQbDtSVv4OD/5mMBj81E8/5eOREx2AEWilxhS8RfgCJP3Po9dzqpArxud0QWMy9qgSLAJsLhwR3+5/8L/68O+8HdDWcYyHl/wILMBjZBh18t7s6XhQ+X8d/UZHIFpDhSEg=; xman_f=WEm20MFoFmt7gVaCFWkn03Lz3yepwracBjmHg9eKhtEMTsA5iLSMjhMlmRP1wPwJSMtC8ShtxwnNpDP07SSvwpcn9mlCf+6wLsrsgptjnJqjfiFPm9kk0GFHYGCWy50jtgk4HiyOaKJKmqWMVZAAfm0nkg9IG/f1jtQGt1hPPIfXHJatds9vtTOZKsvIPDZo/ulJONDn9hObbfL/dieE8xqPf9LDsHlgNcdLz+eFgfCEN5JBj3G/Xj8dDo3xEZRS64CkVevRc6MErtQxRFwG4OgNlZgTyaWqFous+BsJ8DRkqv3EIUidXasQhd1r40P1/AwlIWbsJw/Y1il461iiOH1WjbM04JG55yf/AeihmSUxipQOO0uHE7MprU99v9cIny9NS66agehGU92pvp/ZzbjUFRoOAP4X; __utma=3375712.345480204.1458413486.1458413486.1458413486.1; __utmb=3375712.8.9.1458413564378; __utmc=3375712; __utmz=3375712.1458413486.1.1.utmcsr=m0.mail.sina.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/classic/index.php; __utmt=1; ali_beacon_id=174.139.5.221.145841358483.164192.9; cna=EY50D2g0bUQCAa6LBd0oCf+t; isg=0E20D42340A3596CABA98A5A7ECF9143; l=Aq-vcBpF8p0I7Vsh5K/to7WQH825VgN2; aep_common_f=TXOpYwNXnaGg24vIpRyMCny7B8BlJeSwoK65N3zU2JMAEdisfqsYdA==; xman_us_t=x_lid=us1149061838lfln&sign=y&x_user=bHs+GL1WsrbB4uVevBukWhAKyxNB6baNurLcvHBWM/M=&ctoken=duxx_40n9iut&need_popup=y; JSESSIONID=E9A44A9045DBC353AE68422C4D5183E7; u_info=KrJthPwGHzzZxKj14jS2BqFGnZrLoeTMVa0WeaOVe9k=; intl_locale=en_US; intl_common_forever=zrYVHMAxDgfZMIgpg55Pz15gYCxeuVgp5+G0nge0Nf9DZqhgHdk7nA==; _ga=GA1.2.345480204.1458413486; _gat=1; aep_usuc_t=ber_l_fg=A0; _mle_tmp0=eNrz4A12DQ729PeL9%2FV3cfUx8KvOTLFScjUwNzZxtDCxNHMyNXYys7AwdXIycTYwcbJwNDU1NnZT0kkusTI0MbUwMTQ2M7U0MTbRSUxGE8itsDKojQIAlgUXvw%3D%3D; d_ab_f=41a817ac3f3e4961b06b839ac9c11779; aep_history=keywords%5E%0Akeywords%09%0A%0Aproduct_selloffer%5E%0Aproduct_selloffer%0932422842972%0932451707186""",
    4: """ali_apache_id=204.45.182.132.1458417088513.071582.9; ali_apache_track=mt=1|ms=|mid=us1149697939kiub; ali_apache_tracktmp=W_signed=Y; xman_us_f=x_l=0&x_locale=en_US&no_popup_today=n&x_user=US|ethan|hill|ifm|770368567&last_popup_time=1458417126666; aep_usuc_f=site=glo&region=US&b_locale=en_US&isb=y&isfm=y&x_alimid=770368567&c_tp=USD&reg_ver=new; acs_usuc_t=acs_rt=67d9ebccaac84e5aa328c2bb55f70427; xman_t=VHC5Cx3GrWHFNrY/3f3p7/mSpqfpOJ7UsPPKwywKgsrT6JT/Ufmv1OmxDmjdPnnw/H+428QtBrc9HAKEuW5vzbfnLPXfSlQcuilyOo2PpXyKbWXwS9eNUcVeNZQuC0F8DqJvGqndirMSXyiEQ47uGePsoEHjF81LdG2klpVl2Vu33nVy7JC2/CIfR1zgF+Ff80h2XzXJHbt5betjXbXjJTmMtFspmhb+C2+nszO9XY+jMrCT1si7BLeWqXDkZwayyPdcDCxZVYJv7xWIoNmcfLKMVIfEGgGYtjVrctGYeBrsd1BufN+OC4f3eGCU8aoYmFV3RJ0DEzoDdM/DQgZwDdjDasrNtXjY+82y5wJfkogCc3Ba4BO6KojEsppOtks17VK4cNhkLntRXVQLhhqX+c/Mn4rNYMW2vESvLwvgHNeiO8z76zphPIRloAE5ICF2PSjxeGOcfmQ1auCJTHKOeV95rF8l8sJTU5uwtaTrBcwyMAaBZC22GVbadQ+GqRAEmqVI/iceQvYO3UL6gyYQYYY+lC9pq89fWUE644R/UuCTDTp6ouTlI1f8tUVfa/OeQs6FsIcbnEWARAescnxMKPIvHFTkN+jemsRij7kRWUl5+tZ7Cs+Rr4vnQAsuwMYw; xman_f=DasiQTspQvjgk7S5bqRqZs2MrngFC7VIgb0xFMgSioqMFf+dEWb7Jsi/pEZNRfe24+8n4B/jUCT8nqYsuPb1HV2YN9ykNmQWeCwJKwTXp05UyKE3qty6isjGxCAOuGiEsIKZm1p7/w+YGtDJ8+saSMrvLSVouEz7Z3Lxpkrqln6iKPbLCpO1+kiTuXErG34spuLUayIZrxeEqHb+dZmodluItnimrqm+exN3nanvHMxDADLKNUzNzuoKzGuWIRBI/D0V+La3np8YIHggSgfAxIsS21qtCmV8rcWrU5y/6RImu/S+qHSOhr+AxrQYST1gUNCtdr+rmk+2vEdpihLYL5B0l6qS8IE6GMJ8RzI2EtqHjd7aiE/iH+q0yBI2cGoNEO4TVhBqyCmWTgNcQwbxuY+Xd6fT/Mh5; ali_beacon_id=204.45.182.132.1458417088513.071582.9; __utma=3375712.162358738.1458416992.1458416992.1458416992.1; __utmb=3375712.8.9.1458417075185; __utmc=3375712; __utmz=3375712.1458416992.1.1.utmcsr=m0.mail.sina.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/classic/index.php; __utmt=1; cna=KZN0D0Zfiz0CAcwttoToYNNU; isg=DDD660AF0E4A271B5481C260CF8D4013; l=AmZmzwbzr5ArvqJu1bxUFDo4ltLoGKoE; aep_common_f=nwWPHjTU5zHKk1zmAZm5p6YR1eOuzjKS0XpbxZxwBXU2dvglLuPhIA==; xman_us_t=x_lid=us1149697939kiub&sign=y&x_user=CkBnLtRU+FHO5XMUV0zky3DW/5s+HFovAo1XaEF/QXU=&ctoken=dfxf9n3ridz1&need_popup=y; JSESSIONID=4CAECC9D053E1812A4F224FE25AB5B54; u_info=TSbYZKMuT6/T4ys35JCxHlQWY+jINwH2/5i2bYLUUpw=; intl_locale=en_US; intl_common_forever=tgynVpL/MMM+KdryobRosD4EnKx6CNAt26YbCLHFrpaTaanby+d11g==; _ga=GA1.2.162358738.1458416992; _gat=1; aep_usuc_t=ber_l_fg=A0; _mle_tmp0=eNrz4A12DQ729PeL9%2FV3cfUx8KvOTLFSMnRzNTWydHMzsnBxMjRyNXJxtTQ3MjV2dDI0MHcxNzJU0kkusTI0MbUwMTQ3NDcwMzbUSUxGE8itsDKojQIAnQ0XxQ%3D%3D; d_ab_f=e0a5334c686f422d83a9bf9556494042; aep_history=keywords%5E%0Akeywords%09%0A%0Aproduct_selloffer%5E%0Aproduct_selloffer%0932243265383%0932593604961"""
}


def gen_cookie():
    return dict(
            map(lambda x: (x.split('=', 1)[0].strip(), x.split('=', 1)[1]),
                _cookie_d.get(random.randint(1, len(_cookie_d))).split(';'))
    )


# for testing cookies
# _cookie_t = """ali_apache_id=101.105.37.177.1438705554786.260685.7; xman_us_f=x_l=1&x_locale=en_US&no_popup_today=n&x_user=US|yang|young|ifm|768474461&last_popup_time=1457712623354; aep_usuc_f=region=US&site=glo&b_locale=en_US&isb=y&isfm=y&c_tp=USD&x_alimid=768474461&reg_ver=new; intl_common_forever=rL5z+pTJEMOqSRr7MKiguZ9Lihf5oTyQRXJT8FtnVwNdRxp5uU1O5Q==; xman_f=6h/npGRCn8PCxoOVd+ue381gNqVAQGBg6f+jrlxyGbjxI6OUURdWZejPr1msspHIQEwM8SJpZNIUm14F+GhdzSfktjgh5/GMO5yA+qU1wD2owvJzr3HKslkoZaZcsKtcNz3AvPuo9SeiXrF7jgd1QXPY/UKDRO0nX4/1v6rGB6aWdfYMKt318vLhWIrmQrZQ4oheJxWqlJvixq92djQGQqnIfqMEtiGiYak3o51oWkCRF4N81S9LxC18FPxXHwjYyIAoUDWv7BVeykIDtRJtbS5sdMne0gc2pupQJx9sdHEJEr3GehcGxdpUJiYRC6lIX+3y8vior2X4xrdYH2agXOY9VFF5GExTbAdNQxhr6oBDhNkL/lM42Ee7JgqXK4tTRVpXQ+XekMIymgMmxR0oVyJ4BNOOlrLb; ali_beacon_id=220.152.150.99.1433075894474.773074.1; cna=PDviDaz2VHICAdyYlirqiemC; __utma=3375712.324010086.1438705507.1458384428.1458388505.11; l=AgAA/C6h38RBbszMOKKq5h4L8IDS7ORb; aep_history=keywords%5E%0Akeywords%09%0A%0Aproduct_selloffer%5E%0Aproduct_selloffer%0932328512449%0932320594174%0932379793562%0932312953658%0932602972005; _umdata=8D5462A7710B16F8D1DE8DF86205FD525C80C1F3E9ED159353D27A988B78E33A486FC569B0FB883C6705A9C6F940A638B43E266F5C7442047DCA4915D89FB7108E94AD13019CB44D; __utmz=3375712.1458388505.11.2.utmcsr=aliexpress.com|utmccn=(referral)|utmcmd=referral|utmcct=/category/200003482/dresses.html; _ga=GA1.2.324010086.1438705507; ali_apache_track=mt=1|ms=|mid=us1149212384ijsz; isg=580CC597EE0CF236F5283A13388FEF5B; d_ab_f=f12887f4ca9643129dfe6be772bb1c8d; aep_common_f=q4D4WHUu8LURVHlV+ZWTmdw4tcu1GZaUE+q0QzAaL+l3PdjHUgygiQ==; JSESSIONID=2848429EB23B3C6BB077C066C1B1923F; acs_usuc_t=acs_rt=243129bb6ae3438c9a9bfc4c59b82a31; xman_t=yPdVpMwygp/1uJRRe/aRCOVu7qxTo0j4NxOaYy1Px7+qxl/YeFLljop+D4dXpySUtoLvePze6njxvzuEHviXYvtqd7EcYDCOUJ+GOEwyBeb/R+fsYaSOILTOMizYulrgJkbq8zl6+RdWiTldpJAiqyIXsyk8bOy0OKfiyjCfT+5NqCvCGraThzyhQiTkQCaNGuHol2OAe5xLIZWKP08FwdjqX9RnxhBLMniaDJNjufN8RukWlkIXAfqxvLLM5Z37a1kIcQ4Uut26XfxPJhpzMod9sv8GNlvNdTibgvAqL5HQHh+MtWevinhVLJX2NtXdM/WVapXaLTjtQf71x7yMwWVFjPF9GE2NXenpinDrg7oRy3oBM7FwYpvqiy28LItoRKlXzL8Xmf/EwsTEpX7IS9Fi0+7Ts6yWhL3+MdA1grGNUsltGr9a5kS/yZiF4MmdUNlbsEp4uAcpjT5gcMyDxXnmDz/RDHHL1ayvGndWISTpF6SNqd6LO+gd76Hm3e+uo6WX3VvNCRWzC/hpZ92mZ2RHOpCuvZvYKKskYSCF3HwoZANaLFIk+g04LqADCTPjQUE+jm1UG/l3VbrhzQ8wkOzdBJ4/cJ29iTj1I67dcgGVs9F795wUOu8Qcux/bnOp; intl_locale=en_US; __utmc=3375712; _mle_tmp0=eNrz4A12DQ729PeL9%2FV3cfUx8KvOTLFSsjQ2dzRxczUyMHI2dXU1dLF0dDV1MXUysDA3M3BydXZS0kkusTI0MbUwtjCxMDMyMDTWSUxGE8itsDKojQIApWsX%2Fw%3D%3D; ali_apache_tracktmp=W_signed=Y; u_info=PzPojPc60gU9BgN7gGdVe/HeSj7zFohb8RmPP904RxI=; __utmb=3375712.7.10.1458388505; xman_us_t=x_lid=us1149212384ijsz&sign=y&x_user=tMwQ8hJci/ZHhxqofsUOYS/G9Uo5udG12uV1XaI35NY=&ctoken=ibova_l11_rq&need_popup=y&l_source=aliexpress; aep_usuc_t=ber_l_fg=A0; __utmt=1; _gat=1"""
# _cookie = dict(map(lambda x: (x.split('=', 1)[0].strip(), x.split('=', 1)[1]),_cookie_t.split(';')))


def crawled_urls():
    if not db_server.isTableExist():
        db_server.createTable(tableTitle=table_title.split(','))
        return []
    else:
        return map(
                lambda x: x.rsplit('/', 1)[0] + '/contactinfo/' + x.rsplit('/', 1)[1] + '.html',
                map(lambda x: x[0], db_server.getData(var='shop_url'))
        )


crawled_urls = crawled_urls()


def gen_url():
    def url_join(t):
        if '.html' in t:
            return None
        else:
            temp = t.rsplit('/', 1)
            return temp[0] + '/contactinfo/' + temp[1] + '.html'

    def change_par(x):
        if '//www' in x:
            return url_join(x)
        elif '//pt' in x:
            return url_join(x.replace('//pt', '//www'))
        elif '//ru' in x:
            return url_join(x.replace('//ru', '//www'))
        elif '//es' in x:
            return url_join(x.replace('//es', '//www'))
        else:
            return None

    db_g = DBService(dbName=db_name, tableName='aliexpress_temp', **connect_dict)
    href_list_t = db_g.getData(var='store_href', distinct=True)
    href_s = map(
            lambda t: change_par(t), map(
                    lambda x: x[0], href_list_t
            )
    )
    return list(set(filter(lambda x: 1 if x else 0, href_s)))


all_urls = gen_url()


def download_page(url):
    _cookie = gen_cookie()
    _proxy = proxies_queue.get(timeout=36000)
    print "--PROXY => %s ; COOKIES => %s" % (_proxy, _cookie.get('ali_apache_id'))
    try:
        r = requests.get(url, cookies=_cookie, headers=_headers,
                         proxies={'http': 'http://%s' % _proxy}, timeout=5)
        response = r.content
        r.close()
        return response, _proxy
    except Exception:
        return None, _proxy


def page_parse(content, url):
    d = PyQuery(content)
    # print content[:200].encode('utf8')
    shop_name = d.find('.shop-name>a').text()
    shop_years = d.find('.shop-time>em').text()
    open_time = d.find('.store-time>em').text()
    contact_person = d.find('.contactName').text()
    contact_block = d.find('.box.block.clear-block').html()
    contact_detail = re.findall(pattern_contact_info, contact_block)
    crawl_time = time.strftime('%Y-%m-%d %X', time.localtime())
    return [
        url.replace('contactinfo/', '').replace('.html', ''),
        json.dumps(dict([
                            ('shop_name', shop_name),
                            ('contact_url', url),
                            ('shop_years', shop_years),
                            ('open_time', open_time),
                            ('contact_person', contact_person)
                        ] + contact_detail)
                   ),
        crawl_time
    ]


def __page_parse(url):
    content, proxy = download_page(url)
    return page_parse(content, url)


class Aliexpress_Company_Contact_Information_Spider(object):
    def __init__(self):
        self.queue_urls = Queue(0)
        self.crawled_url = crawled_urls
        self.gen_urls = all_urls
        self.url_start = list(set(self.gen_urls).difference(set(self.crawled_url)))

    def __url_putting(self):
        for url in self.url_start:
            self.queue_urls.put(url)

    def single_thread(self, lock):
        while self.queue_urls.qsize():
            url = self.queue_urls.get()
            content, proxy = download_page(url)
            try:
                page_data = page_parse(content, url)
                proxies_queue.put(proxy)
                print page_data
                db_server.data2DB(data=page_data)
            except Exception, e:
                print e.message
                self.queue_urls.put(url)

    def __gen_thread_and_run(self, thread_lock, thread_count=3):
        run_thread_pool = list()
        run_thread_pool.append(threading.Thread(target=proxies_test))
        while thread_count > 0:
            run_thread_pool.append(
                    threading.Thread(target=self.single_thread, args=(thread_lock,),
                                     name='SPIDER_' + str(thread_count)))
            thread_count -= 1
        for task in run_thread_pool:
            task.start()
        for task in run_thread_pool:
            task.join()

    def crawl(self, thread_count=3):
        self.__url_putting()
        thread_lock = threading.Lock()
        self.__gen_thread_and_run(thread_count=thread_count, thread_lock=thread_lock)


if __name__ == '__main__':
    spider = Aliexpress_Company_Contact_Information_Spider()
    spider.crawl(50)
