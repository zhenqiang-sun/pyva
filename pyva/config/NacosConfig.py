from pyva.util.IpUtil import IpUtil


class NacosConfig:
    """
    Nacos配置

    :version: 3.0
    :createdDate: 2020-02-28
    :updatedDate: 2022-10-03
    """

    # 主机
    host: str = "localhost"
    # 端口
    port: int = 8848
    # 安全证书
    ssl: bool = True
    # 命名空间
    namespace: str = "public"
    # 配置组
    group: str = "DEFAULT_GROUP"
    # 运行环境
    env: str = "dev"
    # 注册服务名
    serviceName: str
    # 注册服务端口
    servicePort: int
    # 注册服务IP
    serviceIp = IpUtil.getHostIp()
    # 注册服开启状态
    serviceEnabled: bool = True
    # 配置ID
    dataId: str
    # 配置ID组，优先级高于dataId
    dataIdList = []
    # 心跳频率，单位秒
    heartInterval: int = 5
    clusterName = None
    weight = 1.0
    metadata = None
    enable = True
    healthy = True
    ephemeral = True
