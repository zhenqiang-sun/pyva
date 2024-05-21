class DictUtil:
    """
    字典工具类，字典合并等

    作者：孙振强
    版本：1.0.1
    创建时间：2023-11-26
    修改时间：2023-11-26
    """

    @staticmethod
    def mergeDict(dictA, dictB):
        """
        合并两个实体对象
        :param dictA: 字典A
        :param dictB: 字典B
        """

        for key, value in dictB.items():
            if key in dictA and isinstance(value, dict) and isinstance(dictA[key], dict):
                DictUtil.mergeDict(dictA[key], value)
            else:
                dictA[key] = value
