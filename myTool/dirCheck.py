# coding:utf-8
__author__ = '613108'
import os
import platform


# noinspection PyBroadException
def isDirExistOrCreate(root='d:', **kwargs):
    """
    # 判断目录是否存在，若存在则跳过，不存在则创建
    # root为根目录，directory为末级目录（必须为list）；
    # **kwargs参数解析，支持二层嵌套:dir_1st="" OR dir_1st=[] dir_2nd=[]
    :param root:
    :param kwargs:
    :return:
    """
    # 初始化
    pathListWindows_temp = []
    pathListWindows = []
    # **kwargs参数解析，仅支持二层嵌套
    for key in kwargs:
        if key == 'directory_1st':
            if isinstance(kwargs[key], list):
                for item in kwargs[key]:
                    pathListWindows_temp.append(root + '/' + item)
                    pathListWindows.append(root + '/' + item)
            elif isinstance(kwargs[key], str):
                pathListWindows_temp.append(root + '/' + kwargs[key])
                pathListWindows.append(root + '/' + kwargs[key])

        elif key == 'directory_2nd':
            if isinstance(kwargs[key], list):
                for k_k in kwargs[key]:
                    if isinstance(k_k, list):
                        for item2 in k_k:
                            pathListWindows.append(pathListWindows_temp[kwargs[key].index(k_k)] + '/' + item2)
                    elif isinstance(k_k, str):
                        try:
                            pathListWindows.append(pathListWindows_temp[kwargs[key].index(k_k)] + '/' + k_k)
                        except:
                            for item in pathListWindows_temp:
                                pathListWindows.append(item + '/' + k_k)
            elif isinstance(kwargs[key], str):
                for item in pathListWindows_temp:
                    pathListWindows.append(item + '/' + kwargs[key])

    # 判断系统类别
    if platform.system() == 'Windows':
        pathList = pathListWindows
    else:
        pathList = ['/home/613108/' + item.split('/', 1)[1] for item in pathListWindows]

    # 判断是否已存在相关文件夹，如无则创建
    for item in pathList:
        if os.path.exists(item):
            print(item + u' 目录已存在，无需创建！')
            continue
        else:
            os.mkdir(item)
            print(item + u' 目录已创建！')


def dirGen(windowsDir='d:/spider', linuxDir='/home/613108/'):
    """
    目录返回，常用于目录拼接，基于给定的windows目录返回linux目标目录（需配置linux根目录）
    :param :
    :return:
    """
    if platform.system() == 'Windows':
        path = windowsDir
    else:
        path = linuxDir + windowsDir.split('/', 1)[1]
    return path


if __name__ == '__main__':
    isDirExistOrCreate(root='D:/spider', directory_1st='jd', directory_2nd=[['commentDetail', 'dd']])
