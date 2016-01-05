# coding:utf8
__author__ = 'YangMingSong'
import pymysql

"""
# 提供更简单、友好的API以进行MySql数据库操作
"""


class DBBase:
    """
    # 数据库基本类，仅提供数据库连接
    """

    def __init__(self, dbName, **kwargs):
        """
        # 提供数库连接服务，生成实例必选参数为dbName及tableName;
        # 连接数据库为默认数据库，如需连接至其他MySql数据库请提供字典参数{host,user,passwd,charset}
        :param dbName:
        :param tableName
        :param kwargs:
        :return:
        """
        self.dbName = dbName
        if kwargs:
            self.host = kwargs['host']
            self.user = kwargs['user']
            self.passwd = kwargs['passwd']
            self.charset = kwargs['charset']
        else:
            self.host = None
            self.user = None
            self.passwd = None
            self.charset = None

    def isDBExist(self):
        """
        # 返回数据库实例是否存在【待实现】
        :return:
        """
        pass

    def genConn(self):
        """
        # 返回数据库连接
        :return:
        """
        if self.host:
            conn = pymysql.connect(
                host=self.host, user=self.user, passwd=self.passwd, charset=self.charset, db=self.dbName)
        else:
            conn = pymysql.connect(
                host='10.118.187.12', user='admin', passwd='admin', charset='utf8', db=self.dbName)
        return conn


class DBService(DBBase):
    """
    # 本类继承自DBBase基本类，由父类提供数据库连接实现
    """

    def __init__(self, dbName, tableName, **kwargs):
        DBBase.__init__(self, dbName, **kwargs)
        self.tableName = tableName

    def isTableExist(self):
        """
        # 用于凑数表格是否存在，如果表存在返回1，若不存在返回0
        :return:
        """
        conn = self.genConn()
        cursor = conn.cursor()
        sql = "select table_name from `INFORMATION_SCHEMA`." \
              "`TABLES` where table_name ='%s'" % self.tableName
        res = cursor.execute(sql)
        conn.close()
        return res

    def getData(self, var='*', limit=None, distinct=False):
        """
        # 依据var变量参数选择返回值;
        # var可为字符串或列表，不指定var则返回全部列数据；
        # limit可指定返回观测数量，不指定则返回全部观测数据；
        # distinct提供数据去重支持，默认为False
        :param var:
        :param limit:
        :param distinct:
        :return:
        """
        isTableExist = self.isTableExist()
        if isTableExist:
            pass
        else:
            print(u'-->表格不存在于数据库，无法获得数据。')
            return None

        conn = self.genConn()
        cursor = conn.cursor()
        sql = None
        if var == '*':
            sql = 'select * from %s' % self.tableName
        elif isinstance(var, list):
            tempforsql = ','.join(var)
            sql = 'select ' + tempforsql + ' from %s' % self.tableName
        elif isinstance(var, str):
            sql = 'select %s from %s' % (var, self.tableName)
        else:
            print(u'-->getData ->var 参数有误，请检查参数。')

        if not limit:
            pass
        elif isinstance(limit, int):
            sql = sql + ' LIMIT ' + str(limit)
        else:
            print(u'-->getData ->limit 参数有误，请检查参数。')

        cursor.execute(sql)
        data = cursor.fetchall()
        conn.close()

        if not distinct:
            pass
        else:
            data = set(data)

        data = [list(item) for item in data]

        return data

    def createTable(self, tableTitle=None, x="N"):
        """
        # 用于创建表格，tableTitle参数为LIST形式提供；
        # 创建之前会先行检查表格是否已经存在，若不存在直接创建；
        # 如果表格已经存在会要求确认是否覆盖前表，如果要求覆盖则会执行删除表格操作后再重新创建表格。
        # x表示如果存在表格，默认直接跳过（不会覆盖更新）
        :param tableTitle:
        :return:
        """
        if not tableTitle:
            print(u'-->createTable->tableTitle 参数有误，请提供表头列表(List形式)')
            return None
        else:
            isTableExist = self.isTableExist()
            if isTableExist:
                if x.upper() == 'N':
                    return None
                else:
                    x = raw_input(u'|->表已存在，是否需要重新创建（将删除前面已经存在的表格）？是，Y；否，N ……\n')
                    if x.upper() == 'Y':
                        sql = 'drop table %s' % self.tableName
                        conn = self.genConn()
                        cursor = conn.cursor()
                        cursor.execute(sql)
                        conn.commit()
                        conn.close()
                        self.forCreateTable(tableTitle=tableTitle)
                        return 1
                    else:
                        return None
            else:
                self.forCreateTable(tableTitle=tableTitle)
                return 1

    def forCreateTable(self, tableTitle):
        """
        # 用于类内部调用，不建议外部直接调用【可能出错】
        :param tableTitle:
        :return:
        """
        conn = self.genConn()
        cursor = conn.cursor()
        typeForTitle = ['varchar(300)' for i in tableTitle]
        titleForSql = zip(tableTitle, typeForTitle)
        titleForSql = ','.join([' '.join(item) for item in titleForSql])  # 组织sql语句
        createTableSql = \
            'create table %s (id int NOT NULL AUTO_INCREMENT,' % self.tableName \
            + titleForSql + ',PRIMARY KEY (`id`))'
        print(createTableSql)
        cursor.execute(createTableSql)
        conn.close()

    def getTableTitle(self):
        """
        用于返回表头（List形式），如果表不存在返回None
        :return:
        """
        if not self.isTableExist():
            return None
        else:
            conn = self.genConn()
            cursor = conn.cursor()
            sql = 'show columns from %s' % self.tableName
            cursor.execute(sql)
            res = cursor.fetchall()
            res = [item[0] for item in res]
            conn.close()
            if res[0] == 'id':
                res = res[1:]
            else:
                print(u'-->请确认；表头无ID列')
            return res

    def data2DB(self, data=None, tableTitle=None):
        """
        # 用于数据存入MySql数据库;参数说明如下：
        # tableTitle存储字段，若不提供则默认为全字段插入
        # data为list形式数据
        :param tableTitle:
        :param data:
        :return:u
        """
        if not self.isTableExist():
            print(u'-->data2DB 表格: %s' % self.tableName + u' 不存在。')
            return None
        if not data:
            print(u'-->data2DB->data 参数无效或缺失。')
            return None
        else:
            if tableTitle:
                self.forData2DB(tableTitle=tableTitle, data=data)
            else:
                tableTitle = self.getTableTitle()
                self.forData2DB(tableTitle=tableTitle, data=data)

    def forData2DB(self, tableTitle, data):
        """
        # 用于类内部调用，不建议外部直接调用
        # 本方法会检查传入的tableTitle(或采用默认值：表内所有字段)与data参数的长度，长度相等的情况下才会执行插入操作
        :param tableTitle:
        :param data:
        :return:
        """

        def ifParOk(TC, DC):
            if len(TC) == len(DC):
                return 1
            else:
                print(u'-->forData2DB->tableTitle & data 参数长度不一致。')
                return 0

        titleForSql = ','.join(tableTitle)
        valuesForSql = ','.join(['%s' for i in tableTitle])
        conn = self.genConn()
        cursor = conn.cursor()
        tableName = self.tableName
        sql = 'insert into %s (' % tableName + titleForSql + ') values (' + valuesForSql + ')'
        if isinstance(data[0], list):
            if ifParOk(tableTitle, data[0]):
                cursor.executemany(sql, data)
        else:
            if ifParOk(tableTitle, data):
                cursor.execute(sql, data)
        conn.commit()
        conn.close()
