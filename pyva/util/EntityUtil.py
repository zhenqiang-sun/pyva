from pyva.Global import G
from pyva.entity.BaseEntity import DeclarativeBase
from pyva.util.JsonUtil import JsonUtil


class EntityUtil:
    """
    EntityUtil 实体工具类
    object与dict转换函数
    :version: 2.1
    :date: 2019-01-08
    """

    @staticmethod
    def entityToDict(entity):
        # 判断: 是否为空
        if not entity:
            G.logger.error("entity is empty.")
            return None

        # 判断：类型
        if not isinstance(entity, DeclarativeBase):
            G.logger.error("entity is not DeclarativeBase object.")
            return None

        # 定义：返回数据
        data = {}

        # 遍历：实体
        for field, value in entity.__dict__.items():
            # 判断：过滤不需要的字段
            if field == "_sa_instance_state":
                continue

            data[field] = value

        return data

    @staticmethod
    def entityToJson(entity):
        data = EntityUtil.entityToDict(entity)
        json = JsonUtil.encode(data)
        return json
