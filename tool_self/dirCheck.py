# coding:utf-8
__author__ = '613108'
import os, platform


def ifDirOrCreate(root='d:', **kwargs):
    # root为根目录，directory为末级目录（必须为list）；
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


def dirGen(dirTarget='d:/spider'):
    if platform.system() == 'Windows':
        path = dirTarget
    else:
        path = '/home/613108/' + dirTarget.split('/', 1)[1]
    return path


if __name__ == '__main__':
    ifDirOrCreate(root='D:/spider', directory_1st='jd', directory_2nd=[['commentDetail', 'dd']])
