from sqlalchemy import Column, String, TIMESTAMP, text, DECIMAL, Date, DateTime, JSON, VARCHAR
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, LONGTEXT, TINYINT
from sqlalchemy.ext.declarative import declarative_base

from pyva.config.DbConfig import DbConfig

DeclarativeBase = declarative_base()


class Base(DeclarativeBase):
    """
    基础Model模型对象
    """
    # 开启继承
    __abstract__ = True
    # 表前缀
    _the_prefix = DbConfig.prefix
    __table_args__ = {
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_general_ci',
    }


if __name__ == "__main__":
    Column, String, TIMESTAMP, text, DECIMAL, Date, DateTime, JSON, VARCHAR, BIGINT, INTEGER, LONGTEXT, TINYINT
