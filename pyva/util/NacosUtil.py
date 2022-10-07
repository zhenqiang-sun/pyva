import _thread
import json
import random
import time

import nacos
import yaml
from requests import request

from pyva.config.NacosConfig import NacosConfig


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

    def __init__(self, nacosConfig: NacosConfig):
        self.nacosConfig = nacosConfig

        if nacosConfig.ssl:
            protocol = "https"
        else:
            protocol = "http"

        self.url = "{}://{}:{}".format(
            protocol,
            nacosConfig.host,
            nacosConfig.port)

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
                    None, 1, None)
            except:
                print("Nacos服务器连接失败")

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
        configStr = self.client.get_config(self.nacosConfig.dataId, self.nacosConfig.group)

        if self.nacosConfig.dataId.endswith(".yml"):
            self.config = yaml.full_load(configStr)
        elif self.nacosConfig.dataId.endswith(".json"):
            self.config = json.loads(configStr)

        return self.config

    def init(self):
        """
        初始化
        :return:
        """
        # 获取client
        self.getClient(self.url, self.nacosConfig.namespace)

        # 注册实例
        self.client.add_naming_instance(
            self.nacosConfig.serviceName,
            self.nacosConfig.serviceIp,
            self.nacosConfig.servicePort,
            None, 1, None, True, True, True)

        # 发送心跳
        _thread.start_new_thread(self.sendHeartbeat, ())

    @staticmethod
    def resetConfig(obj: object, config: dict):
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

    def post(self, serviceName: str, path, json=None, data=None, files=None):
        """
        请求屏幕系统服务POST方法
        :param serviceName 服务名
        :param path 请求地址
        :param json 请求json数据
        :param data: 请求form数据
        :param files: 请求文件数据
        :return dict 返回数据
        """

        url = self.getInstanceUrl(serviceName) + path

        resp = request('post', url, json=json, data=data, files=files)

        if resp.status_code == 200 and resp.text:
            return resp.json()
        else:
            return None

    def get(self, serviceName: str, path, data=None):
        """
        请求屏幕系统服务POST方法
        :param serviceName 服务名
        :param path 请求地址
        :param data: 请求query数据
        :return dict 返回数据
        """

        url = self.getInstanceUrl(serviceName) + path

        resp = request('get', url, data=data)

        if resp.status_code == 200 and resp.text:
            return resp.json()
        else:
            return None
