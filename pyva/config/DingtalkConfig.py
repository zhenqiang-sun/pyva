# 配置文件：dingtalk
class DingtalkConfig:
    """
    钉钉应用配置

    :version: 1.0
    :createdDate: 2020-02-28
    :updatedDate: 2022-10-03
    """

    # 应用Key
    appKey: str = ""
    # 应用秘钥
    appSecret: str = ""
    # 默认接口调用操作钉钉用户ID
    operationUserId: str = ""
    # 默认宜搭表单创建钉钉用户ID
    workOrderUserId: str = ""
    # 宜搭应用配置：AppType
    yiDaOpsAppType: str = ""
    # 宜搭应用配置：Token
    yiDaOpsSystemToken: str = ""
