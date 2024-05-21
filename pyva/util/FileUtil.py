import os

from pyva.Global import G


class FileUtil:

    @staticmethod
    def getFileContent(filePath):
        """
        获取文件内容
        :param filePath: 文件路径
        :return:
        """

        if not os.path.exists(filePath):
            return ""

        with open(filePath, "r", encoding="utf-8") as f:
            return f.read()

    @staticmethod
    def getFileAndFormat(filePath, params: dict = {}):
        """
        从文件中获取内容并格式化
        :param filePath: 文件路径
        :param params: 替换参数
        :return:
        """

        content = FileUtil.getFileContent(filePath)
        return content.format(**params)

    @staticmethod
    def getTemplateFile(filePath, params: dict = {}):
        """
        从模版文件中获取内容并格式化
        :param filePath: 文件路径
        :param params: 替换参数
        :return:
        """
        if G.path:
            filePath = G.path + os.sep + "template" + os.sep + filePath

        return FileUtil.getFileAndFormat(filePath, params)
