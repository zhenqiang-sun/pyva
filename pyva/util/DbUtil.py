import os
from datetime import datetime
from decimal import Decimal
from urllib.parse import quote_plus

from humps.main import camelize
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session, Session

from pyva.Global import G
from pyva.config.DbConfig import DbConfig


class DbUtil:
    """
    pyva DbUtils DB工具类
    :version: 1.5
    :createdDate: 2020-02-11
    :updatedDate: 2022-10-03
    """

    config: DbConfig
    sess: Session

    def __init__(self, dbConfig: DbConfig):
        """
        初始化时创建session
        :param dbConfig:
        """
        self.config = dbConfig
        self.sess = self.getSession(dbConfig)
        self.sess.autocommit = dbConfig.autoCommit

    def __del__(self):
        """
        销毁时关闭sess
        :return:
        """

        if self.sess:
            self.sess.close()

    @staticmethod
    def getConfigUrl(config):
        """
        获取完整连接地址
        :return:
        """

        config = [
            config.driver,
            "://",
            config.username,
            ":",
            quote_plus(config.password),
            "@",
            config.host,
            ":",
            str(config.port),
            "/",
            config.database,
            "?charset=",
            config.charset,
        ]

        return "".join(config)

    @staticmethod
    def getSession(dbConfig: DbConfig):
        """
        获取sess
        :param dbConfig: 数据库连接配置文件
        :return:
        """
        engine = create_engine(
            DbUtil.getConfigUrl(dbConfig),
            pool_size=dbConfig.poolSize,
            max_overflow=dbConfig.maxOverflow,
            pool_recycle=dbConfig.poolRecycle,
            pool_pre_ping=dbConfig.poolPrePing,
            echo=dbConfig.echo,
            **dbConfig.otherParam
        )

        session_factory = sessionmaker(
            # autocommit=dbConfig.autoCommit,
            autoflush=dbConfig.autoFlush,
            bind=engine,
            expire_on_commit=dbConfig.expireOnCommit)

        return scoped_session(session_factory)

    # 根据文件获取SQL文件
    @staticmethod
    def getSql(filePath, params: dict = {}):
        """
        从文件中获取SQL语句
        :param filePath: 文件路径
        :param params: 替换参数
        :return:
        """
        if G.sqlPath:
            filePath = G.sqlPath + os.sep + filePath

        sql = DbUtil.getFile(filePath)
        return sql.format(**params)

    # 获取SQL文件
    @staticmethod
    def getFile(filePath):
        """
        获取文件内容
        :param filePath: 文件路径
        :return:
        """
        with open(filePath, "r", encoding="utf-8") as f:
            return f.read()

    @staticmethod
    def rowToDict(row):
        """
        row转dict
        :param row:
        :return:
        """
        if not row:
            return None

        # 定义一个字典对象
        dictionary = {}

        for key in row._keymap:
            if isinstance(key, str):
                if isinstance(row[key], Decimal):
                    dictionary[key] = str(row[key])
                elif isinstance(row[key], bytes):
                    dictionary[key] = ord(row[key])
                else:
                    dictionary[key] = row[key]

        return dictionary

    @staticmethod
    def rowsToList(rows):
        """
        rows转list
        :param rows:
        :return:
        """
        # 定义一个字典数组
        dataList = []

        for row in rows:
            dataList.append(DbUtil.rowToDict(row))

        return dataList

    @staticmethod
    def getOne(sess: Session, sql: str):
        """
        查找一个结果
        :param sess:
        :param sql:
        :return:
        """
        row = DbUtil.executeSql(sess, sql).fetchone()
        return DbUtil.rowToDict(row)

    @staticmethod
    def getOneAndCamelize(sess: Session, sql: str):
        """
        查找一个结果并转为驼峰命名
        :param sess:
        :param sql:
        :return:
        """
        data = DbUtil.getOne(sess, sql)

        if data:
            return camelize(data)
        else:
            return None

    @staticmethod
    def getAll(sess: Session, sql: str):
        """
        查找全部结果
        :param sess:
        :param sql:
        :return:
        """
        rows = DbUtil.executeSql(sess, sql).fetchall()
        return DbUtil.rowsToList(rows)

    @staticmethod
    def getAllAndCamelize(sess: Session, sql: str):
        """
        查找全部结果并转为驼峰命名
        :param sess:
        :param sql:
        :return:
        """
        data = DbUtil.getAll(sess, sql)

        if data:
            return camelize(data)
        else:
            return None

    @staticmethod
    def handleSqlField(field: str) -> str:
        return "`{}`".format(field.replace("`", "").replace(".", "`.`"))

    @staticmethod
    def getSqlFields(obj: dict) -> str:
        """
        获取sql的fields部分，增加重音符号
        :param obj: 数据对象
        :return: sql字段，增加重音符，以逗号分割
        """

        fields = []

        for field in obj:
            fields.append(DbUtil.handleSqlField(field))

        return ", ".join(fields)

    @staticmethod
    def handleValue(value) -> str:
        """
        处理Sql的值，转义字符串
        :param value:
        :return:
        """

        return str(value).replace(
            "\\", "\\\\").replace(
            '\"', '\\\"').replace(
            ":", "\\:").replace(
            "%", "\\%")

    @staticmethod
    def handleSqlValue(value) -> str:
        """
        处理Sql的值，转义字符串
        :param value:
        :return:
        """

        if not value and "" != value and 0 != value:
            return "null"
        elif type(value) in [int, float, bool, Decimal]:
            return str(value)
        elif type(value) in [datetime]:
            return '"{}"'.format(value)
        elif "" == value:
            return '""'
        else:
            return '"{}"'.format(DbUtil.handleValue(value))

    @staticmethod
    def getSqlValues(obj: dict) -> str:
        """
        获取sql的values部分
        :param obj: 数据对象
        :return:
        """
        values = []

        for field in obj:
            value = obj[field]
            values.append(DbUtil.handleSqlValue(value))

        return "({})".format(", ".join(values))

    @staticmethod
    def getSqlInsert(table: str, obj: dict, replace: bool = False) -> str:
        """
        获取单记录的写入SQL语句
        :param table: 写入表名
        :param obj: 写入对象
        :param replace: 是否为replace语句
        :return:
        """
        return DbUtil.getSqlInserts(table, [obj], replace)

    @staticmethod
    def getSqlInserts(table: str, objList: list, replace: bool = False) -> str:
        """
        获取多记录的写入SQL语句
        :param table: 写入表名
        :param objList: 写入对象list
        :param replace: 是否为replace语句
        :return:
        """
        if not table or not objList or not objList[0]:
            return ""

        table = DbUtil.handleSqlField(table)
        fields = DbUtil.getSqlFields(objList[0])
        valuesList = []

        for obj in objList:
            valuesList.append(DbUtil.getSqlValues(obj))

        if replace:
            command = "REPLACE"
        else:
            command = "INSERT"

        sql = "{} INTO {} ({}) VALUES {};".format(command, table, fields, ", ".join(valuesList))
        return sql

    @staticmethod
    def getSqlUpdate(table: str, obj: dict, where: str):
        """
        获取单记录的更新SQL语句
        :param table:
        :param obj:
        :param where:
        :return:
        """
        if not table or not obj or not where:
            return ""

        table = DbUtil.handleSqlField(table)
        values = []

        for field in obj:
            value = obj[field]
            values.append("{} = {}".format(DbUtil.handleSqlField(field), DbUtil.handleSqlValue(value)))

        sql = "UPDATE {} SET {} WHERE {}".format(table, ", ".join(values), where)
        return sql

    @staticmethod
    def getSqlDelete(table: str, where: str):
        """
        获取删除SQL语句
        :param table:
        :param obj:
        :param where:
        :return:
        """
        if not table or not where:
            return ""

        table = DbUtil.handleSqlField(table)

        sql = "DELETE FROM {} WHERE {}".format(table, where)
        return sql

    @staticmethod
    def executeSql(sess: Session, sql: str):
        """
        执行SQL语句
        :param sess:
        :param sql:
        :return:
        """
        return sess.execute(text(sql))

    @staticmethod
    def executeFile(sess: Session, filePath, params: dict = {}):
        """
        执行SQL文件
        :param sess:
        :param sql:
        :return:
        """
        sql = DbUtil.getSql(filePath, params)

        return DbUtil.executeSql(sess, sql)
