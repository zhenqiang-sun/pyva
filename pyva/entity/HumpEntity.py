from sqlalchemy import Table

from pyva.entity.BaseEntity import *


class HumpEntity(BaseEntity):
    """字段驼峰形式的Entity"""

    # 开启继承
    __abstract__ = True

    # 将表字段转为小写下划线命名形式
    @classmethod
    def __table_cls__(cls, *arg, **kw):
        for obj in arg[1:]:
            if isinstance(obj, Column):
                obj.name = decamelize(obj.name)

        return Table(*arg, **kw)
