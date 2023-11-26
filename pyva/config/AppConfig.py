import os


class AppConfig:
    """
    pyva AppConfig 应用配置类

    :version: 3.0.1
    :createdDate: 2020-02-11
    :updatedDate: 2022-10-03
    """

    # 应用名，即服务注册名
    name: str = "pava-demo"
    # 应用标题
    title: str = "pyva Demo"
    # 应用描述
    description: str = "PyVa项目示例，基于FastAPI。"
    # 应用版本
    version: str = "1.0.1"
    # 应用根目录
    rootPath: str = ""
    # 应用代码目录
    srcPath: str = ""
    # 应用端口
    port: int = 9000
    # 运行环境：prod、pre、test、dev、local
    env: str = os.getenv("ENV", "dev")
    # 运行模式：是否Debug模式
    debug: bool = False
    # 运行进程数：debug模式则默认为1，非debug模式按照配置进行启动
    workers: int = 2
    # token有效秒数
    tokenExpire: int = 86400
    # log输出至钉钉
    log2dingtalk: bool = False
    # 安全模式：是否启用HTTPS
    https = False
