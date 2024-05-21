import logging

from pyva.client.dingtalk.DingtalkRobotClient import DingtalkRobotClient
from pyva.config.AppConfig import AppConfig
from pyva.util.IpUtil import IpUtil
from pyva.util.TimeUtil import TimeUtil


class LoggingHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)

    def emit(self, record):
        if AppConfig.env == "local":
            return

        if not AppConfig.log2dingtalk:
            return

        if record.levelname not in ["ERROR", "WARNING"]:
            return

        if record.filename == "DingtalkRobotClient.py":
            return

        log_message = self.format(record)
        title = "系统代码运行上报"
        text = f'''#### {title}
- 环境：{AppConfig.env}
- IP：{IpUtil.getHostIp()}
- 服务：{AppConfig.name}
- 调试：{AppConfig.debug}
- 级别：{record.levelname}
- 时间：{TimeUtil.formatTimestamp(record.created)}
- 线程：{record.thread}
- 文件：{record.filename}
- 行号：{record.lineno}
- 模块：{record.module}
- 函数：{record.funcName}
- 消息：
```
{log_message}
```
'''

        DingtalkRobotClient.sendMarkdown(
            title=title,
            text=text,
            # isAtAll=True
        )
