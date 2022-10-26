from fastapi.responses import ORJSONResponse


class FastapiConfig:
    """
    Fastapi配置

    :version: 3.0
    :createdDate: 2020-02-28
    :updatedDate: 2022-10-03
    """

    title: str = None
    description: str = None
    version: str = None
    debug: bool = True
    openapi_url: str = "/openapi.json"
    openapi_prefix: str = None
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"
    default_response_class: ORJSONResponse

    # CORS配置
    corsOrigins: list = [
        "http://localhost",
        "http://localhost:8080",
    ]
