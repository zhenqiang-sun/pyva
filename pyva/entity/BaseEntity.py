from sqlalchemy import Column, String, TIMESTAMP, text, DECIMAL, Date, DateTime, JSON, VARCHAR
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, LONGTEXT, TINYINT
from sqlalchemy.ext.declarative import declarative_base

DeclarativeBase = declarative_base()


class BaseEntity(DeclarativeBase):
    """
    基础Model模型对象
    """
    # 开启继承
    __abstract__ = True
    # 表参数
    __table_args__ = {
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_general_ci',
    }


if __name__ == "__main__":
    Column, String, TIMESTAMP, text, DECIMAL, Date, DateTime, JSON, VARCHAR, BIGINT, INTEGER, LONGTEXT, TINYINT
