from fastapi.responses import ORJSONResponse


class FastapiConfig:
    """
    Fastapi配置

    :version: 3.0
    :createdDate: 2020-02-28
    :updatedDate: 2022-10-03
    """

    name: str = None
    title: str = None
    description: str = None
    version: str = None
    debug: bool = True
    openapi_url: str = "/openapi.json"
    openapi_prefix: str = None
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"
    default_response_class: ORJSONResponse
    # 是否支持跨域
    allowCors: bool = False
    # CORS配置
    corsOrigins: list = [
        "http://localhost",
        "http://localhost:8080",
    ]
    # 应用端口
    port: int = 9000
    # 安全模式：是否启用HTTPS
    https = False
