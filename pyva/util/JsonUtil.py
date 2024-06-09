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

    @staticmethod
    def extract(content: str):
        """
        从字符串中提取JSON数据并转换为字典
        @param content:
        @return:
        """

        if not content:
            return None

        content = content.replace('\\"', '||')

        # 查找第一个 '{' 的位置
        startIndex = content.find('{')
        # 查找最后一个 '}' 的位置
        endIndex = content.rfind('}')

        # 提取并返回结果
        if startIndex == -1 or endIndex == -1:
            return None

        s = content[startIndex:endIndex + 1]

        if s.startswith("{'"):
            s = re.sub(r"',\n+(\s?)+'", "','", s)
            s = s.replace('\n', '\\n')
            return eval(s)

        try:
            return orjson.loads(s)
        except Exception as e:
            pass

        s = re.sub(r'{\n+(\s?)+"', '{"', s)

        if not s.startswith('{"'):
            return None

        s = re.sub(r'"\n(\s?)+"(.*?)": "', r'",\n"\g<2>": "', s)
        s = re.sub(r'”\n(\s?)+"(.*?)": "', r'",\n"\g<2>": "', s)
        s = re.sub(r'",\n+(\s?)+"', '","', s)
        s = re.sub(r'"\n+(\s?)+}', '"}', s)
        s = re.sub(r'null,\n+(\s?)+"', 'null,"', s)
        s = re.sub(r'null\n+(\s?)+}', 'null}', s)
        s = s.replace('\n', '\\n')

        try:
            return orjson.loads(s)
        except Exception as e:
            G.logger.debug(f"第一次尝试提取json数据失败: {e}")
            pass

        i = 0
        while i != -1:
            i = s.find('"', i + 1)

            if i == -1:
                break

            if (i == 1 or s[i - 2:i] == '",' or s[i - 3:i] == '": ' or s[i - 5:i] == 'null,'
                    or s[i:i + 4] == '": "' or s[i:i + 3] == '","' or s[i:i + 2] == '"}'):
                continue
            else:
                s = s[0:i] + "'" + s[i + 1:]

        try:
            return orjson.loads(s)
        except Exception as e:
            G.logger.error(f"提取json数据失败: {e}")
            return None
