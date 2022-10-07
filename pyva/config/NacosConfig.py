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
    ssl: bool = False
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
    # 配置ID
    dataId: str
    # 心跳频率，单位秒
    heartInterval: int = 5
