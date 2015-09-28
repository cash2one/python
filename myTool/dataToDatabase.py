# coding:utf-8
__author__ = '613108'
"""
弃用
"""

def connectDatabase(dbName=None):
    if not dbName:
        print(u'--请输入数据库实例名')
        return None

    import pymysql

    connect = pymysql.connect(host='10.118.187.12', user='admin', passwd='admin', charset='utf8', db=dbName)
    return connect


def csvDataToDatabase(path=r'D:\spider\jd\productDetail', dbName=None, tableTitle=None):
    if not dbName:
        print(u'--请检查参数：需指定dbName')
        yield dbName
    if not tableTitle:
        print(u'--请检查参数：需指定dbName')
        yield tableTitle
    import os, csv

    conn = connectDatabase(dbName=dbName)
    fileList = os.listdir(path)
    result = []
    isTableExist(tableTitle=tableTitle)
    for item in fileList:
        fileName = path + '/' + item
        i = 0
        with open(fileName, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if not i:
                    i += 1
                    print "Okay~"
                    continue
                else:
                    # data2database(tableTitle=tableTitle, data=row)
                    result.append(row)
            data2database(tableTitle=tableTitle, data=result)
        result = []
    conn.close()


def get_module():
    # 用于返回当前模块名称
    import sys, os

    def main_module_name():
        mod = sys.modules['__main__']
        fileinner = getattr(mod, '__file__', None)
        return fileinner and os.path.splitext(os.path.basename(fileinner))[0]

    def modname(fvars):
        fileinner, name = fvars.get('__file__'), fvars.get('__name__')
        if fileinner is None or name is None:
            return None

        # if name == '__main__':
        name = main_module_name()
        return name

    module_name = modname(globals())
    return module_name


def isTableExist(tableTitle=None):
    """
    :param tableTitle:本参数用于指定对应表格表头，可用于自动创建待插入数据的表格，如果确定对应表格已经存在则无需指定。
    :return:无返回值。
    """
    if not tableTitle:
        tableTitle = []
    connect = connectDatabase()
    cursor = connect.cursor()
    tableName = get_module()
    ifExistSql = "select table_name from `INFORMATION_SCHEMA`." \
                 "`TABLES` where table_name ='%s'" % tableName
    if cursor.execute(ifExistSql):
        pass
    else:
        if not tableTitle:
            print(u'--请检查参数：无对应表头列表，不能创建表。')
        else:
            title = tableTitle
            typeOfTitle = ['varchar(300)' for i in title]
            titleForSql = zip(title, typeOfTitle)
            # 组织sql语句
            titleForSql = ','.join([' '.join(item) for item in titleForSql])
            # 利用模块名称作目标表名
            createTableSql = \
                'create table %s (id int NOT NULL AUTO_INCREMENT,' % tableName \
                + titleForSql + ',PRIMARY KEY (`id`))'
            cursor.execute(createTableSql)
            print(u'++表已创建！')


def data2database(tableTitle=None, data=None,dbName=None):
    if not tableTitle or not data or not dbName:
        print(u'--无参数，请输入参数！')
    else:
        titleForSql = ','.join(tableTitle)
        valuesForSql = ','.join(['%s' for i in tableTitle])
        connect = connectDatabase(dbName)
        cursor = connect.cursor()
        tableName = get_module()
        insertSql = 'insert into %s (' % tableName + titleForSql + ') values (' + valuesForSql + ')'
        cursor.executemany(insertSql, data)
        connect.commit()
