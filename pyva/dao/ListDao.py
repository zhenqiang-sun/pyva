import math
from typing import List

from sqlalchemy import and_, func

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
        # if listReqDto.is_deleted != 'all':
        #     filters.append(self.Entity.is_deleted == 0)

        # 判断：是否限制指定用户的数据
        if listReqDto.user_id:
            filters.append(self.Entity.user_id == listReqDto.user_id)

        # 增加：传入调整
        filters.extend(self._handle_list_filters(listReqDto.filters))

        # 判断：是否进行关键词搜索
        if listReqDto.keywords and hasattr(self.Entity, 'search'):
            filters.append(and_(*[self.Entity.search.like('%' + kw + '%') for kw in listReqDto.keywords.split(' ')]))

        # 执行：数据检索
        query = self.db.query(self.Entity).filter(*filters)
        count = query.count()

        # 判断： 结果数，是否继续查询
        if count > 0:
            orders = self._handle_list_orders(listReqDto.orders)
            obj_list = query.order_by(*orders).offset((listReqDto.page - 1) * listReqDto.size).limit(
                listReqDto.size).all()
        else:
            obj_list = []

        # 构造：返回结构
        data = ListPageDto()
        data.page = listReqDto.page
        data.size = listReqDto.size
        data.count = count
        data.page_count = math.ceil(count / listReqDto.size)  # 计算总页数
        data.list = self._handle_list_keys(listReqDto.keys, obj_list)  # 处理list

        return data

    def _handle_list_filters(self, args_filters: ListFilterDto):
        """
        处理list接口传入的过滤条件
        :param args_filters: 传入过滤条件
        :return: 转换后的sqlalchemy过滤条件
        """
        filters = []

        if args_filters:
            for item in args_filters:
                if hasattr(self.Entity, item.key):
                    attr = getattr(self.Entity, item.key)

                    if item.condition == '=':
                        filters.append(attr == item.value)
                    elif item.condition == '!=':
                        filters.append(attr != item.value)
                    elif item.condition == '<':
                        filters.append(attr < item.value)
                    elif item.condition == '>':
                        filters.append(attr > item.value)
                    elif item.condition == '<=':
                        filters.append(attr <= item.value)
                    elif item.condition == '>=':
                        filters.append(attr >= item.value)
                    elif item.condition == 'like':
                        filters.append(attr.like('%' + item.value + '%'))
                    elif item.condition == 'in':
                        filters.append(attr.in_(item.value.split(',')))
                    elif item.condition == '!in':
                        filters.append(~attr.in_(item.value.split(',')))
                    elif item.condition == 'null':
                        filters.append(attr.is_(None))
                    elif item.condition == '!null':
                        filters.append(~attr.isnot(None))

        return filters

    def _handle_list_orders(self, args_orders: ListOrderDto):
        """
        处理list接口传入的排序条件
        :param args_orders: 传入排序条件
        :return: 转换后的sqlalchemy排序条件
        """
        orders = []

        if args_orders:
            for item in args_orders:
                if hasattr(self.Entity, item.key):
                    attr = getattr(self.Entity, item.key)

                    if item.condition == 'desc':
                        orders.append(attr.desc())
                    elif item.condition == 'acs':
                        orders.append(attr)
                    elif item.condition == 'rand':  # 随机排序
                        orders.append(func.rand())

        return orders

    def _handle_list_keys(self, args_keys: ListKeyDto, obj_list: List):
        """
        处理list返回数据，根据传入参数keys进行过滤
        :param args_keys: 传入过滤字段
        :return: 转换后的list数据，数据转为dict类型
        """
        keys = []

        if args_keys:
            for item in args_keys:
                if hasattr(self.Entity, item.key):
                    keys.append(item)

        resp_list = []

        for obj in obj_list:
            dict_1 = EntityUtil.entityToDict(obj)

            # 判断：keys存在，不存在则返回所有字段
            if keys:
                dict_2 = {}
                for item in keys:
                    if item.rename:
                        dict_2[item.rename] = dict_1[item.key]
                    else:
                        dict_2[item.key] = dict_1[item.key]
            else:
                dict_2 = dict_1

            resp_list.append(dict_2)

        return resp_list
