from humps.main import decamelize
from sqlalchemy import Column, BOOLEAN, String, CHAR, VARCHAR, TEXT, TIMESTAMP, Time, DATE, DATETIME, JSON, INT, FLOAT, DECIMAL, text, UniqueConstraint, Index
from sqlalchemy.dialects.mysql import INTEGER, TINYINT, BIGINT, LONGTEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declared_attr

DeclarativeBase = declarative_base()


class BaseEntity(DeclarativeBase):
    """基础Entity模型对象"""

    # 开启继承
    __abstract__ = True

    # 表名，帕斯卡命名形式的类名转为小写下划线命名形式
    @declared_attr
    def __tablename__(cls):
        return decamelize(cls.__name__)

    # 表参数，将类注释变为表注释
    @declared_attr
    def __table_args__(cls):
        args = {
            "mysql_charset": "utf8mb4",
            "mysql_collate": "utf8mb4_general_ci",
        }

        if cls.__doc__:
            args["comment"] = cls.__doc__

        return args


if __name__ == "__main__":
    Column, BOOLEAN, String, CHAR, VARCHAR, TEXT, TIMESTAMP, Time, DATE, DATETIME, JSON, INT, BIGINT, FLOAT, DECIMAL, text, UniqueConstraint, Index, INTEGER, TINYINT, LONGTEXT
