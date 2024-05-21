from pyva.entity.HumpEntity import *


class GeneralHumpEntity(HumpEntity):
    """通用驼峰Entity"""

    # 开启继承
    __abstract__ = True

    id = Column(BIGINT(20, unsigned=True), nullable=False, primary_key=True, comment="主键")
    createdTime = Column(DATETIME, nullable=False, server_default=text("current_timestamp()"), comment="创建时间")
    createdBy = Column(BIGINT(20, unsigned=True), nullable=False, server_default=text("0"), comment="创建人ID")
    createdByName = Column(VARCHAR(50), nullable=False, server_default=text("''"), comment="创建人名称")
    updatedTime = Column(DATETIME, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"), comment="修改时间")
    updatedBy = Column(BIGINT(20, unsigned=True), nullable=False, server_default=text("0"), comment="修改人ID")
    updatedByName = Column(VARCHAR(50), nullable=False, server_default=text("''"), comment="修改人名称")
    deleted = Column(BOOLEAN, nullable=False, server_default=text("0"), comment="是否删除：1是、0否")
