import datetime

from pyva.Global import G
from pyva.entity.BaseEntity import DeclarativeBase
from pyva.util.JsonUtil import JsonUtil


class EntityUtil:
    """
    EntityUtil 实体工具类，转化字典、JSON字符串、合并等

    作者：孙振强
    版本：2.2.1
    创建时间：2019-01-08
    修改时间：2023-11-21
    """

    @staticmethod
    def entityToDict(entity):
        """
        将实体对象转换为字典对象
        :param entity: 实体对象
        :return: 字典对象
        """

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

            if isinstance(value, datetime.datetime):
                data[field] = value.isoformat(" ")
            else:
                data[field] = value

        return data

    @staticmethod
    def entityToJson(entity):
        """
        将实体对象转换为JSON字符串
        :param entity: 实体对象
        :return: JSON字符串
        """
        data = EntityUtil.entityToDict(entity)
        jsonStr = JsonUtil.encode(data)
        return jsonStr

    @staticmethod
    def mergeEntity(entityA, entityB):
        """
        合并两个实体对象
        :param entityA: 实体对象A
        :param entityB: 实体对象B
        """
        for field, value in entityB.__dict__.items():
            # 判断：过滤不需要的字段
            if field == "_sa_instance_state":
                continue

            if hasattr(entityA, field):
                setattr(entityA, field, value)

    @staticmethod
    def dictToEntity(data, entityClass):
        """
        将字典对象转换为实体对象
        :param data: 字典对象
        :param entityClass: 实体类
        :return: 实体对象
        """
        entity = entityClass()

        for field, value in data.items():
            if hasattr(entity, field):
                setattr(entity, field, value)

        return entity

    @staticmethod
    def jsonToEntity(jsonStr, entityClass):
        """
        将JSON字符串转换为实体对象
        :param jsonStr: JSON字符串
        :param entityClass: 实体类
        :return: 实体对象
        """
        data = JsonUtil.decode(jsonStr)
        entity = EntityUtil.dictToEntity(data, entityClass)
        return entity
