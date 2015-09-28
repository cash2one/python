# coding:utf-8
__author__ = '613108'
import sys
sys.path.append(r'../tool_self')


def myInvoing(func):
    def new(*args):
        print(u'正在调用：' + func.func_name)
        return func(*args)

    return new


# 返回天猫数据(mySql->yms_tmall_shopinfo_com_withoutjudge)
@myInvoing
def returnCommentPageData():
    import pymysql

    conn = pymysql.connect(host='10.118.187.12', user='admin', passwd='admin', charset='utf8', db='elec_platform')
    cursor = conn.cursor()
    sqlSelect = 'SELECT * FROM yms_tmall_shopinfo_com_withoutjudge'
    cursor.execute(sqlSelect)
    data = cursor.fetchall()
    conn.close()
    return data


# 返回本地数据；每周更新的天猫数据，用于匹配行业、公司名称等信息
@myInvoing
def returnWeeklyDataFromLocalSrc():
    import csv

    fileName = r'C:\Users\613108\Desktop\Total_Distinct_2015-08-28 17_22_56.csv'
    data = []
    with open(fileName, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(row)
    return data


@myInvoing
def tmallShop2Company():
    comData = returnCommentPageData()
    shopData = returnWeeklyDataFromLocalSrc()

    dShop = {}
    for item in shopData:
        dShop[item[1] + '/'] = item

    dComIndustry = {}
    for item in comData:
        dComIndustry[item[2]] = item[5]

    dComCompanyName = {}
    for item in comData:
        dComCompanyName[item[2]] = item[4]

    data=[]
    for itemShop in dShop.keys():
        try:
            tempIndustry=dComIndustry[itemShop].encode('gbk','ignore')
            tempCompanyName=dComCompanyName[itemShop].encode('gbk','ignore')
            temp=dShop[itemShop]+[tempIndustry]+[tempCompanyName]
            data.append(temp)
        except:continue

    dataSaved(data)

@myInvoing
def dataSaved(result):
    import My_Csv, dirCheck

    title = []
    writer = My_Csv.Write_Csv(path=dirCheck.dirGen('d:/operationAnalysis'), name='temp',title=title, result=result)
    writer.add_title_data()

if __name__ == '__main__':
    tmallShop2Company()
