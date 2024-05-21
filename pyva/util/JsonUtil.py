import datetime
import decimal
import re

import orjson

from pyva.Global import G


class JsonUtil:
    """
    JSON工具类

    作者：孙振强
    版本：2.0.1
    创建时间：2022-10-07
    修改时间：2023-11-21
    """

    # 定义JSONEncoders
    jsonEncoders = {
        # 解决日期和时间中“T”字符的格式问题
        datetime.datetime: lambda dt: dt.isoformat(" "),
        decimal.Decimal: lambda dt: str(dt),
    }

    def default(obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        raise TypeError

    @staticmethod
    def encode(obj):
        """
        编码对象为JSON字符串
        @param obj:
        @return:
        """
        return orjson.dumps(obj, default=JsonUtil.default).decode("utf-8")

    @staticmethod
    def decode(s):
        """
        解码JSON字符串
        @param s:
        @return:
        """
        return orjson.loads(s)

    @staticmethod
    def extract(content: str):
        """
        从字符串中提取JSON数据并转换为字典
        @param content:
        @return:
        """

        # 查找第一个 '{' 的位置
        startIndex = content.find('{')
        # 查找最后一个 '}' 的位置
        endIndex = content.rfind('}')

        # 提取并返回结果
        if startIndex == -1 or endIndex == -1:
            return None

        jsonStr = content[startIndex:endIndex + 1]

        if jsonStr.startswith("{'"):
            jsonStr = re.sub(r"',\n+(\s?)+'", "','", jsonStr)
            jsonStr = jsonStr.replace('\n', '\\n')
            return eval(jsonStr)

        jsonStr = re.sub(r'{\n+(\s?)+"', '{"', jsonStr)
        jsonStr = re.sub(r'",\n+(\s?)+"', '","', jsonStr)
        jsonStr = re.sub(r'"\n+(\s?)+}', '"}', jsonStr)
        jsonStr = jsonStr.replace('\n', '\\n')

        try:
            return orjson.loads(jsonStr)
        except Exception as e:
            G.logger.error(f"提取json数据失败: {e}")
            return None
