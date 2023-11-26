import os


class PathUtil:
    """
    路径工具类

    作者：孙振强
    版本：1.0.1
    创建时间：2023-11-25
    修改时间：2023-11-25
    """

    @staticmethod
    def getAbsolutePath(relativePath):
        """
        将相对路径转换为绝对路径

        参数:
        relativePath (str): 相对路径

        返回:
        str: 绝对路径
        """
        return os.path.abspath(relativePath)

    @staticmethod
    def getDirectoryPath(filePath, depth: int = 0):
        """
        获取给定文件的目录路径

        参数:
        filePath (str): 文件路径
        depth (int, optional): 切割目录层数，默认为0

        返回:
        str: 目录路径
        """
        for i in range(depth):
            filePath = os.path.dirname(filePath)

        return os.path.dirname(filePath)

    @staticmethod
    def joinPaths(*paths):
        """
        连接多个路径部分

        参数:
        *paths: 多个路径部分

        返回:
        str: 连接后的路径
        """
        return os.path.join(*paths)

    @staticmethod
    def getFilename(filePath):
        """
        从路径中获取文件名

        参数:
        filePath (str): 文件路径

        返回:
        str: 文件名
        """
        return os.path.basename(filePath)

    @staticmethod
    def splitExtension(filePath):
        """
        分离文件名和扩展名

        参数:
        filePath (str): 文件路径

        返回:
        tuple: 文件名和扩展名
        """
        return os.path.splitext(filePath)
