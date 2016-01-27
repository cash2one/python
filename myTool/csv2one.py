# coding:utf-8
__author__ = 'Administrator'

import csv
import os
import MyCsv


def all_to_one(path):
    file_list = os.listdir(path)
    file_list = [path + '/' + item for item in file_list]
    result = []
    title = []
    fileCount = len(os.listdir(path))
    count = 1
    for item in file_list:
        print(u'正在合并第 %s 个文件，总共 %s 个文件' % (count, fileCount))
        with open(item, 'r') as csv_file:
            reader = csv.reader(csv_file)
            i = 0
            for row in reader:
                if i:
                    result.append(row)
                else:
                    if title:
                        if title[0] == row:
                            pass
                        else:
                            print(u'表头不一致，请检查数据源')
                    else:
                        title.append(row)
                i += 1
        count += 1
    writer = MyCsv.Write_Csv(path=path, name='Total', title=title[0], result=result)
    writer.add_title_data()


def all_to_one_Distinct(path):
    d = {}
    title = []
    for item in os.listdir(path):
        with open(path + '/' + item, 'r') as f:
            reader = csv.reader(f)
            i = 1
            for row in reader:
                if i == 1:
                    title = row
                else:
                    # print(row)
                    # 配置项，利用哪一列内容去重
                    d[row[1]] = row
                i += 1
    result = [item[1] for item in d.items()]
    # result=[item.split('|||') for item in result]
    writer = MyCsv.Write_Csv(path=path, name='Total_Distinct', title=title, result=result)
    writer.add_title_data()


def one_to_N(fileName):
    with open(fileName, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)


if __name__ == '__main__':
    # t = time.time()
    # # all_to_one(r'C:\Users\613108\Desktop\jdcomment\src1')
    all_to_one_Distinct(r'D:\spider\tmall\20151026')
    # print('*' * 15 + u'文件合并完毕，请检查数据' + '*' * 15)
    # t = time.time() - t
    # print('*' * 16 + u'总计耗时：%f 秒' + '*' * 16) % t
    # one_to_N(r'D:\spider\jd\commentDetail\Total_Distinct_2015-08-30 18_39_49.csv')
    # all_to_one_Distinct(r'D:\spider\taobao\baseInfo')
