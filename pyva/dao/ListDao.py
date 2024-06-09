import math
from typing import List

from sqlalchemy import and_, func

from pyva.common.FilterConditionEnum import FilterConditionEnum
from pyva.common.OrderConditionEnum import OrderConditionEnum
from pyva.dao.BaseDao import BaseDao
from pyva.dto.ListDto import ListReqDto, ListFilterDto, ListOrderDto, ListKeyDto, ListPageDto
from pyva.util.EntityUtil import EntityUtil


class ListDao(BaseDao):
    """
    List(基础)Dao，用于被继承.
    """

    def list(self, listReqDto: ListReqDto) -> ListPageDto:
        """
        读取数据列表
        :param listReqDto: 聚合参数，详见：ListArgsSchema
        :return: 返回数据列表结构，详见：RespListSchema
        """

        # 定义：query过滤条件
        filters = []

        # 判断：是否包含已软删除的数据
        if hasattr(self.Entity, "deleted"):
            if not hasattr(listReqDto, "deleted") or (hasattr(listReqDto, "deleted") and listReqDto.deleted != 'all'):
                filters.append(self.Entity.deleted == False)

        # 判断：是否限制指定用户的数据
        if hasattr(listReqDto, "userId") and hasattr(self.Entity, "userId") and listReqDto.userId:
            filters.append(self.Entity.userId == listReqDto.userId)

        # 增加：传入调整
        if hasattr(listReqDto, "filters") and listReqDto.filters:
            filters.extend(self._handleListFilters(listReqDto.filters))

        # 判断：是否进行关键词搜索
        if hasattr(listReqDto, "keywords") and hasattr(self.Entity, 'search') and listReqDto.keywords:
            filters.append(and_(*[self.Entity.search.like('%' + kw + '%') for kw in listReqDto.keywords.split(' ')]))

        # 执行：数据检索
        query = self.db.query(self.Entity).filter(*filters)
        count = query.count()

        # 判断： 结果数，是否继续查询
        if count == 0:
            objList = []
        else:
            if hasattr(listReqDto, "orders") and listReqDto.orders:
                orders = self._handleListOrders(listReqDto.orders)
                query = query.order_by(*orders)

            objList = query.offset((listReqDto.page - 1) * listReqDto.size).limit(listReqDto.size).all()

        # 构造：返回结构
        data = ListPageDto()
        data.page = listReqDto.page
        data.size = listReqDto.size
        data.count = count
        data.pageCount = math.ceil(count / listReqDto.size)  # 计算总页数

        if hasattr(listReqDto, "keys") and listReqDto.keys:
            data.list = self._handleListKeys(listReqDto.keys, objList)  # 处理list
        else:
            data.list = objList

        return data

    def _handleListFilters(self, argsFilters: List[ListFilterDto]):
        """
        处理list接口传入的过滤条件
        :param argsFilters: 传入过滤条件
        :return: 转换后的sqlalchemy过滤条件
        """
        filters = []

        if not argsFilters:
            return filters

        for item in argsFilters:
            if not hasattr(self.Entity, item.key):
                continue

            attr = getattr(self.Entity, item.key)

            match item.condition:
                case FilterConditionEnum.EQ.value:
                    filters.append(attr == item.value)
                case FilterConditionEnum.NE.value:
                    filters.append(attr != item.value)
                case FilterConditionEnum.LT.value:
                    filters.append(attr < item.value)
                case FilterConditionEnum.GT.value:
                    filters.append(attr > item.value)
                case FilterConditionEnum.LTE.value:
                    filters.append(attr <= item.value)
                case FilterConditionEnum.GTE.value:
                    filters.append(attr >= item.value)
                case FilterConditionEnum.LIKE.value:
                    filters.append(attr.like('%' + item.value + '%'))
                case FilterConditionEnum.IN.value:
                    filters.append(attr.in_(item.value.split(',')))
                case FilterConditionEnum.NOT_IN.value:
                    filters.append(~attr.in_(item.value.split(',')))
                case FilterConditionEnum.IS_NULL.value:
                    filters.append(attr.is_(None))
                case FilterConditionEnum.NOT_NULL.value:
                    filters.append(~attr.isnot(None))

        return filters

    def _handleListOrders(self, argsOrders: List[ListOrderDto]):
        """
        处理list接口传入的排序条件
        :param argsOrders: 传入排序条件
        :return: 转换后的sqlalchemy排序条件
        """
        orders = []

        if not argsOrders:
            return orders

        for item in argsOrders:
            if not hasattr(self.Entity, item.key):
                continue

            attr = getattr(self.Entity, item.key)

            match item.condition:
                case OrderConditionEnum.DESC.value:
                    orders.append(attr.desc())
                case OrderConditionEnum.ASC.value:
                    orders.append(attr.asc())
                case OrderConditionEnum.RAND.value:
                    orders.append(func.rand())

        return orders

    def _handleListKeys(self, argsKeys: List[ListKeyDto], objList: List):
        """
        处理list返回数据，根据传入参数keys进行过滤
        :param argsKeys: 传入过滤字段
        :return: 转换后的list数据，数据转为dict类型
        """
        keys = []

        if argsKeys:
            for item in argsKeys:
                if hasattr(self.Entity, item.key):
                    keys.append(item)

        respList = []

        for obj in objList:
            dict1 = EntityUtil.entityToDict(obj)

            # 判断：keys存在，不存在则返回所有字段
            if keys:
                dict2 = {}
                for item in keys:
                    if item.rename:
                        dict2[item.rename] = dict1[item.key]
                    else:
                        dict2[item.key] = dict1[item.key]
            else:
                dict2 = dict1

            respList.append(dict2)

        return respList
