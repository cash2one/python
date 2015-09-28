__author__ = 'Administrator'

import urllib2
import json,sys
reload(sys)
sys.setdefaultencoding('utf-8')

url = 'http://s.club.jd.com/productpage/p-1647298052-s-0-t-0-p-2.html?callback=fetchJSON_comment'
jsonFile = urllib2.urlopen(url).read()
jsonFile = jsonFile.split('(',1)[1][:-2]
jsonFile = jsonFile.decode('GBK','ignore')
print(jsonFile)

jsonFile = json.loads(jsonFile)

commentCount = jsonFile['productCommentSummary']['commentCount']
print(commentCount)
commentList = jsonFile['comments']

for item in commentList:
    print('*'*50)
    userId = item['id']
    userGuid = item['guid']
    content = item['content']
    createTime = item['creationTime']
    referenceId = item['referenceId']
    referenceTime = item['referenceTime']
    replyCount = item['replyCount']
    score = item['score']
    userLevelId = item['userLevelId']
    userProvince = item['userProvince']
    productColor = item['productColor']
    userLevelName = item['userLevelName']
    userClientShow = item['userClientShow']
    userClientShow = userClientShow.split('>',1)[1].split('<',1)[0] if userClientShow else '-'
    isMobile = item['isMobile']
    resultTemp = [userId,userGuid,content,createTime,referenceId,
                  referenceTime,replyCount,score,userLevelId,userProvince,productColor,
                  userLevelName,userClientShow,isMobile
                  ]
    for item in resultTemp:
        print(item)