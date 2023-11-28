import _thread
import os
import random
import time

import nacos
import requests
import yaml

from pyva.Global import G
from pyva.config.NacosConfig import NacosConfig
from pyva.util.DictUtil import DictUtil
from pyva.util.JsonUtil import JsonUtil


class NacosUtil:
    """
    Nacos工具了
    :version: 3.0
    :createdDate: 2020-02-28
    :updatedDate: 2022-10-03
    """

    nacosConfig: NacosConfig
    url: str
    client = None
    config = None

    def __init__(self, nacosConfig: NacosConfig, serviceEnabled=True):
        """
        初始化
        """

        self.nacosConfig = nacosConfig

        if nacosConfig.ssl:
            protocol = "https"
        else:
            protocol = "http"

        self.url = "{}://{}:{}".format(
            protocol,
            nacosConfig.host,
            nacosConfig.port)

        # 获取client
        self.getClient(self.url, nacosConfig.namespace)

        # 获取配置
        self.getConfig()

        # 判断配置赋值
        if self.config and self.config.get("nacos"):
            # 判断更新配置：注册服开启状态
            if self.config.get("nacos").get("serviceEnabled") is not None:
                nacosConfig.serviceEnabled = self.config.get("nacos").get("serviceEnabled")

            # 判断更新配置：注册服务IP
            if self.config.get("nacos").get("serviceIp"):
                nacosConfig.serviceIp = self.config.get("nacos").get("serviceIp")
            elif os.getenv("SERVICE_IP"):
                nacosConfig.serviceIp = os.getenv("SERVICE_IP")

        if not nacosConfig.serviceEnabled or not serviceEnabled:
            return

        # 注册实例
        self.client.add_naming_instance(
            self.nacosConfig.serviceName,
            self.nacosConfig.serviceIp,
            self.nacosConfig.servicePort,
            self.nacosConfig.clusterName,
            self.nacosConfig.weight,
            self.nacosConfig.metadata,
            self.nacosConfig.enable,
            self.nacosConfig.healthy,
            self.nacosConfig.ephemeral,
            self.nacosConfig.group)

        # 发送心跳
        _thread.start_new_thread(self.sendHeartbeat, ())

    def __del__(self):
        """
        销毁时注销服务
        :return:
        """

        if self.client:
            self.client.unsubscribe(self.nacosConfig.serviceName)

    def sendHeartbeat(self):
        """
        发送心跳
        :return:
        """
        while True:
            # 发送心跳
            try:
                self.client.send_heartbeat(
                    self.nacosConfig.serviceName,
                    self.nacosConfig.serviceIp,
                    self.nacosConfig.servicePort,
                    self.nacosConfig.clusterName,
                    self.nacosConfig.weight,
                    self.nacosConfig.metadata,
                    self.nacosConfig.ephemeral,
                    self.nacosConfig.group)
            except:
                G.logger.error("Nacos服务器连接失败")

            time.sleep(self.nacosConfig.heartInterval)

    def getClient(self, url, namespace):
        """
        获取client
        :param url:
        :param namespace:
        :return:
        """
        self.client = nacos.NacosClient(url, namespace=namespace)
        return self.client

    def getConfig(self):
        """
        获取配置
        :return:
        """
        if not self.nacosConfig.dataIdList:
            self.nacosConfig.dataIdList = [self.nacosConfig.dataId]

        config = {}

        for dataId in self.nacosConfig.dataIdList:
            G.logger.info(f"Nacos配置文件读取：{dataId}")
            try:
                configStr = self.client.get_config(dataId, self.nacosConfig.group)
                if configStr:
                    if dataId.endswith(".yml"):
                        DictUtil.mergeDict(config, yaml.full_load(configStr))
                    elif dataId.endswith(".json"):
                        DictUtil.mergeDict(config, JsonUtil.decode(configStr))
                    else:
                        G.logger.error(f"Nacos配置文件后缀不支持：{dataId}")
            except Exception as e:
                G.logger.error(f"Nacos配置文件读取失败：{dataId}，错误：{e}")

        self.config = config

        return self.config

    @staticmethod
    def resetConfig(obj: object, config: dict):
        if not config:
            return

        for key, value in config.items():
            if hasattr(obj, key):
                setattr(obj, key, value)

    def setConfig(self, obj: object, key):
        if not self.config:
            self.getConfig()

        if self.config.get(key):
            self.resetConfig(obj, self.config.get(key))

    def getInstanceUrl(self, service_name):
        instance_list = self.client.list_naming_instance(service_name)

        if not instance_list.get('hosts'):
            return None

        # 提取第一个实例
        # instance = instance_list.get('hosts')[0]
        # 随机取一个实例
        instance = random.choice(instance_list.get('hosts'))

        # 判断是否dev环境，是则用nocos服务器的host地址代替实例的ip
        if self.nacosConfig.env == 'dev':
            url = '{}:{}'.format(self.client.get_server()[0], instance.get('port'))
        else:
            url = 'http://{}:{}'.format(instance.get('ip'), instance.get('port'))

        return url

    def request(self, method: str, serviceName: str, path: str, **kwargs):
        """
        请求屏幕系统服务POST方法
        :param method 请求方式
        :param serviceName 服务名
        :param path 请求地址
        """

        url = self.getInstanceUrl(serviceName) + path

        resp = requests.request(method=method, url=url, **kwargs)

        if resp.status_code == 200:
            return resp.json()
        else:
            G.logger.error(resp.text)

            try:
                return resp.json()
            except:
                return None

    def get(self, serviceName: str, path: str, **kwargs):
        return self.request("get", serviceName, path, **kwargs)

    def post(self, serviceName: str, path: str, **kwargs):
        return self.request("post", serviceName, path, **kwargs)

    def put(self, serviceName: str, path: str, **kwargs):
        return self.request("put", serviceName, path, **kwargs)

    def patch(self, serviceName: str, path: str, **kwargs):
        return self.request("patch", serviceName, path, **kwargs)

    def delete(self, serviceName: str, path: str, **kwargs):
        return self.request("delete", serviceName, path, **kwargs)
