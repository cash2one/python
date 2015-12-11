# coding:utf8
__author__ = 'YangMingSong'
import csv, os, time
import sys
reload(sys)
sys.setdefaultencoding('utf8')

"""
功能设计
1、提供csv文件写入功能并保存的功能，参数：保存路径；【文件名保存可选择是否加上日期/时间】
2、csv数据返回功能，以list形式返回，依据提供参数（目录名或文件绝对路径）自动选择返回内容
3、多个csv文件合并，参数为目录名
4、csv文件分割功能，返回多个csv文件，文件名以原文件名为base,外加1-n区分
5、header功能，仅返回指定条目数据（如果文件观测数少于指定数目则仅返回观测数目）
6、title功能,仅返回表头（list形式）
"""


class CSV:
    def __init__(self):
        pass

    def writeCsv(self, savePath=None, fileTitle=None, data=None, fileName=None, fileNameType=2):
        """
        # 提供写csv文件之功能，参数说明如下：
        # savePath:可为目录路径或文件名（绝对路径），其中如果为文件名，fileName参数可忽略
        # fileTile:csv数据表头，参数形式为list,若忽略csv表头将以title_N之形式填充
        # data:待写入数据集，list形式；不得忽略或传入空列表
        # fileName:文件名称
        # fileNameType:文件名称后缀；默认为2，表示将日期+时间置于文件名后方；1表示仅添加日期；其他（一般为0）表示不添加日期或时间
        :param savePath:str
        :param fileTitle:
        :param data:
        :param fileName:
        :param fileNameType:
        :return:
        """

        def fileNameTemp(par):
            """
            # 依据fileNameType返回文件名后缀字符串
            :param par:
            :return:
            """
            fileNameTemp = ''
            if par == 2:
                fileNameTemp = str(time.strftime('%Y-%m-%d+%H-%M-%S'))
            elif par == 1:
                fileNameTemp = str(time.strftime('%Y-%m-%d'))
            else:
                pass
            return fileNameTemp

        def saveData(FN, FT, DA):
            """pritn
            # 保存数据：FN表示fileName;FT表示fileTitle;DA表示data
            :param FN:
            :param FT:
            :param DA:
            :return:
            """
            with open(FN, 'wb') as f:
                writer = csv.writer(f)
                writer.writerow(FT)
                writer.writerows(DA)

        def save2fileName(FN, FT, DA):
            """
            # 保存数据：FN表示fileName;FT表示fileTitle;DA表示data
            :param FN:
            :param FT:
            :param DA:
            :return:
            """
            if FT:
                saveData(FN=FN, FT=FT, DA=DA)
            else:
                # x = raw_input(u'|->fileTitle 参数为None或空值，是否继续（标题取默认值）？ 继续，Y;取消，N …\n')
                x = 'y'
                if x.upper() == 'Y':
                    if isinstance(DA[0], list):
                        FT = ['title_' + str(i) for i in range(len(DA[0]))]
                    elif isinstance(DA[0], str):
                        FT = ['title_' + str(i) for i in range(len(DA))]
                    else:
                        FT = []
                    saveData(FN=FN, FT=FT, DA=DA)
                else:
                    return None

        if not savePath:
            print(u'-->writeCsv->savePath 保存路径缺失。')
            return None
        elif os.path.isdir(savePath):
            if not data:
                print(u'-->writeCsv->data 参数错误（不应为空或None）。')
                return None
            fileNameAsu = savePath + '/' + fileName + fileNameTemp(fileNameType) + '.csv'
            save2fileName(FN=fileNameAsu, FT=fileTitle, DA=data)

        elif os.path.isfile(savePath):
            save2fileName(FN=savePath, FT=fileTitle, DA=data)
        else:
            print('-->writeCsv->savePath 参数错误（不为目录或文件路径）。')
            return None

    def getDataFromFile(self, fileName):
        """
        # 从给定文件中（绝对路径文件名）读取数据
        :param fileName:
        :return:
        """
        res = []
        with open(fileName, 'r') as f:
            reader = csv.reader(f)
            i = 0
            for row in reader:
                if i:
                    res.append(row)
                i += 1
        return res

    def getData(self, filePath):
        """
        # filePath可为文件名或目录名；若为目录名则返回指定目录内所有csv文件数据
        :param filePath:
        :return:
        """
        res = []
        if os.path.isfile(filePath):
            return self.getDataFromFile(filePath)
        elif os.path.isdir(filePath):
            fileList = os.listdir(filePath)
            fileList = [item for item in fileList if item[-3:] == 'csv']
            assert len(fileList) > 0
            for item in fileList:
                fileName = filePath + '/' + item
                res.extend(self.getDataFromFile(fileName=fileName))
        return res

    def csv2one(self, filePath, isReturnData=0, isSaveFile=1, fileName='TOTAL', fileNameType=2):
        """
        # 根据传入目录路径参数，合并目录内所有csv文件
        # filePath:目录路径
        # isReturnData:是否返回合并数据（List形式），默认不返回
        # isSaveFile:是否保存为文件，默认合并
        # fileName:苦果保存为文件则需提供文件名，如不提供则默认为TOTAL
        # fileNameType:文件名称后缀；默认为2，表示将日期+时间置于文件名后方；1表示仅添加日期；其他（一般为0）表示不添加日期或时间
        :param filePath:
        :return:
        """
        if not os.path.isdir(filePath):
            print(u'-->csv2one->filePath 参数有误，不是有效有目录路径。')
        fileList = os.listdir(filePath)
        fileList = [item for item in fileList if item[-3:] == 'csv']
        fileList = [filePath + '/' + item for item in fileList]
        assert len(fileList) > 0
        data = []
        title = None
        for item in fileList:
            with open(item, 'r') as csv_file:
                reader = csv.reader(csv_file)
                i = 0
                for row in reader:
                    if i:
                        data.append(row)
                    else:
                        if title:
                            if title == row:
                                pass
                            else:
                                print(u'-->csv2one 表头不一致，请检查数据源。')
                        else:
                            title = row
                    i += 1
        if isSaveFile and isReturnData:
            self.writeCsv(savePath=filePath, fileTitle=title, data=data, fileName=fileName, fileNameType=fileNameType)
            return data
        elif isSaveFile and not isReturnData:
            self.writeCsv(savePath=filePath, fileTitle=title, data=data, fileName=fileName, fileNameType=fileNameType)
        elif not isSaveFile and isReturnData:
            return data

    def csvSplit(self):
        pass

    def header(self, n=10):
        pass

    def getTitle(self):
        return self.header(0)
