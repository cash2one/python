#coding:utf-8
__author__ = '613108'

import json
import urllib2

#构造小米商品评论get请求，返回json格式数据
for i in range(53):
    get_url='http://comment.www.xiaomi.com/comment/vlist/goods_id/2011/pagesize/10/pageindex/'+\
            str(i+1)+'/comment_grade/0/orderby/1/cnum/0?callback=commentList'
    result=urllib2.urlopen(get_url)
    res=result.read()
    result.close()
    res=res.split('(',1)[1][:-3]
    # print(res)
    res=json.loads(res)
    res=(res['data']['comments'])
    # print(type(res))
    for i in res:
        temp=i['comment_content']
        print(temp.encode('gbk','ignore'))