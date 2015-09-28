__author__ = '613108'
from spiderFrame.CSVService import CSV

C=CSV()
# C.csv2one(filePath=r'D:\spider\tmall\20150921',fileNameType=0)
data=C.getData(filePath=r'D:\spider\tmall\20150921')
S={}
for item in data:
    if item[1] in S.keys():
        S[item[1]]+=1
    else:S[item[1]]=1
data=[item for item in data if item[1] in S]
# data=[item for item in ]
C.writeCsv(savePath=r'D:\spider\tmall\20150921',data=data,fileName='TOTAL')
