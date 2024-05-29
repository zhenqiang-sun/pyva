import importlib
import os

import yaml
from humps.main import pascalize

from pyva.Global import G
from pyva.util.DictUtil import DictUtil
from pyva.util.JsonUtil import JsonUtil
from pyva.util.NacosUtil import NacosUtil


class ConfigUtil:
    """
    配置工具类，读取配置、合并配置等

    作者：孙振强
    版本：1.0.1
    创建时间：2023-11-26
    修改时间：2023-11-26
    """

    @staticmethod
    def readSrcConfig(srcPath, configName):
        """
        读取源配置文件

        Args:
            srcPath (str): 源路径
            configName (str): 配置文件名

        Returns:
            dict: 配置内容
        """
        configPath = f"{srcPath}{os.sep}{configName}"

        if not os.path.exists(configPath):
            G.logger.warning(f"{configName}，文件不存在")
            return {}
        else:
            G.logger.info(f"读取本地配置文件：{configName}")
            try:
                with open(configPath, "r", encoding="utf-8") as f:
                    config = yaml.load(f, Loader=yaml.FullLoader)

                    if not config:
                        G.logger.warning(f"本地配置文件：{configName}，为空文件")
                        return {}
                    elif not isinstance(config, dict):
                        G.logger.error(f"{configName}，文件内容异常: {config}")
                        exit(1)

                    return config
            except Exception as e:
                G.logger.error(f"{configName}，文件无法加载，错误信息：{e}")
                exit(1)

    @staticmethod
    def importConfig(srcPath, name):
        """
        导入配置模块

        Args:
            srcPath (str): 源路径
            name (str): 配置名称

        Returns:
            object: 配置类
        """
        configName = f"{pascalize(name)}Config"
        configPath = f"{srcPath}{os.sep}config{os.sep}{configName}.py"

        if not os.path.exists(configPath):
            G.logger.debug(f"{configName}，文件不存在")
            return None

        try:
            configModule = importlib.import_module(f"src.config.{configName}")
            configClass = getattr(configModule, configName)
            return configClass
        except Exception as e:
            G.logger.error(f"{configName}，配置类无法加载，错误信息：{e}")
            exit(1)

    @staticmethod
    def updateConfig(obj: object, config: dict):
        """
        更新对象的属性值

        Args:
            obj (object): 对象
            config (dict): 配置字典
        """
        if not config:
            return

        for key, value in config.items():
            if hasattr(obj, key):
                setattr(obj, key, value)

    @staticmethod
    def readApplicationConfigByYaml(AppConfig):
        """
        通过YAML读取应用配置

        Args:
            AppConfig (object): 应用配置对象

        Returns:
            dict: 应用配置内容
        """
        applicationConfig = ConfigUtil.readSrcConfig(AppConfig.srcPath, "application.yml")

        ConfigUtil.updateConfig(AppConfig, applicationConfig.get("app"))

        applicationEnvConfig = ConfigUtil.readSrcConfig(AppConfig.srcPath, f"application-{AppConfig.env}.yml")

        # 合并本地文件配置
        DictUtil.mergeDict(applicationConfig, applicationEnvConfig)

        return applicationConfig

    @staticmethod
    def readApplicationConfigByNacos(srcPath, applicationConfig: dict, serviceEnabled=True):
        """
        通过Nacos读取应用配置

        Args:
            srcPath (str): 源路径
            applicationConfig (object): 应用配置对象
            serviceEnabled (bool, optional): Nacos服务是否启用，默认为True
        """

        if not applicationConfig.get("nacos"):
            return

        NacosConfig = ConfigUtil.importConfig(srcPath, "nacos")

        if NacosConfig:
            ConfigUtil.updateConfig(NacosConfig, applicationConfig.get("nacos"))

            nacos = NacosUtil(NacosConfig, serviceEnabled)

            if not nacos.config:
                G.logger.error("Nacos配置获取失败")
                exit(1)

            DictUtil.mergeDict(applicationConfig, nacos.config)

    @staticmethod
    def initConfigForStartup(AppConfig):
        """
        初始化启动配置

        Args:
            AppConfig (object): 应用配置对象
        """
        applicationConfig = ConfigUtil.readApplicationConfigByYaml(AppConfig)
        ConfigUtil.readApplicationConfigByNacos(AppConfig.srcPath, applicationConfig, False)

        if AppConfig.configCache:
            ConfigUtil.saveTemporary(AppConfig, applicationConfig)

        ConfigUtil.updateConfig(AppConfig, applicationConfig.get("app"))

    @staticmethod
    def initConfigForGlobal(AppConfig):
        """
        初始化全局配置

        Args:
            AppConfig (object): 应用配置对象
        """

        if AppConfig.configCache:
            applicationConfig = ConfigUtil.readTemporary(AppConfig)
        else:
            applicationConfig = None

        if not applicationConfig:
            applicationConfig = ConfigUtil.readApplicationConfigByYaml(AppConfig)
            ConfigUtil.readApplicationConfigByNacos(AppConfig.srcPath, applicationConfig)

        for key, value in applicationConfig.items():
            configClass = ConfigUtil.importConfig(AppConfig.srcPath, key)
            if configClass:
                ConfigUtil.updateConfig(configClass, value)

    @staticmethod
    def getTemporaryFilePath(AppConfig):
        filePath = f"{AppConfig.srcPath}{os.sep}temporary{os.sep}application-tmp.json"
        return filePath

    @staticmethod
    def saveTemporary(AppConfig, applicationConfig):
        filePath = ConfigUtil.getTemporaryFilePath(AppConfig)

        # 打开一个文件以追加内容，如果文件不存在则创建它
        with open(filePath, 'w') as file:
            # 向文件中追加内容
            file.write(JsonUtil.encode(applicationConfig))

    @staticmethod
    def readTemporary(AppConfig):
        filePath = ConfigUtil.getTemporaryFilePath(AppConfig)

        if not os.path.exists(filePath):
            return None

        with open(filePath, 'r') as file:
            # 读取文件的全部内容
            content = file.read()

        return JsonUtil.decode(content)

    @staticmethod
    def deleteTemporary(AppConfig):
        filePath = ConfigUtil.getTemporaryFilePath(AppConfig)

        if not os.path.exists(filePath):
            return None

        os.remove(filePath)
