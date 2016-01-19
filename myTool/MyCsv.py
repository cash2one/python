# coding:utf-8
# __author__ = '613108'

import csv
import time


class Write_Csv:
    def __init__(self, path, name, title, result):
        self.result = result
        self.title = title
        self.path = path
        self.name = name

    # 生成文件存储路径
    def get_filename(self):
        filename = (self.path + '/' + self.name + '_%s.csv') % str(time.strftime('%Y-%m-%d %H_%M_%S'))
        return filename

    # 仅添加数据
    def add_data(self):
        filename = self.get_filename()
        csvfile = file(filename, 'wb')
        writer = csv.writer(csvfile)
        writer.writerows(self.result)
        csvfile.close()

    # 仅添加标题
    def add_title(self):
        filename = self.get_filename()
        with open(filename, 'wb') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(self.title)

    # 同时添加标题与数据,需提供标题列表
    def add_title_data(self):
        filename = self.get_filename()
        with open(filename, 'wb') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(self.title)
            writer.writerows(self.result)
