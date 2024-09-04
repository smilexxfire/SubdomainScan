import sys
import pathlib

from loguru import logger
from fluent import sender

from config.settings import FLUENTD_HOST, FLUENTD_PORT, FLUENTD_OPEN
from common.utils import get_external_ip,get_hostname
# 路径设置
relative_directory = pathlib.Path(__file__).parent.parent  # 代码相对路径
result_save_dir = relative_directory.joinpath('result')  # 结果保存目录
log_path = result_save_dir.joinpath('app.log')  # 日志保存路径

# 日志配置
# 终端日志输出格式
stdout_fmt = '<cyan>{time:HH:mm:ss,SSS}</cyan> ' \
             '[<level>{level: <5}</level>] ' \
             '<blue>{module}</blue>:<cyan>{line}</cyan> - ' \
             '<level>{message}</level>'
# 日志文件记录格式
logfile_fmt = '<light-green>{time:YYYY-MM-DD HH:mm:ss,SSS}</light-green> ' \
              '[<level>{level: <5}</level>] ' \
              '<cyan>{process.name}({process.id})</cyan>:' \
              '<cyan>{thread.name: <18}({thread.id: <5})</cyan> | ' \
              '<blue>{module}</blue>.<blue>{function}</blue>:' \
              '<blue>{line}</blue> - <level>{message}</level>'

logger.remove()
logger.level(name='TRACE', color='<cyan><bold>')
logger.level(name='DEBUG', color='<blue><bold>')
logger.level(name='INFOR', no=20, color='<green><bold>')
logger.level(name='QUITE', no=25, color='<green><bold>')
logger.level(name='ALERT', no=30, color='<yellow><bold>')
logger.level(name='ERROR', color='<red><bold>')
logger.level(name='FATAL', no=50, color='<RED><bold>')

# 如果你想在命令终端静默运行，可以将以下一行中的level设置为QUITE
# 命令终端日志级别默认为INFOR
logger.add(sys.stderr, level='INFOR', format=stdout_fmt, enqueue=True)
# 日志文件默认为级别为DEBUG
logger.add(log_path, level='DEBUG', format=logfile_fmt, enqueue=True, encoding='utf-8')

if FLUENTD_OPEN == "true":
    # 配置Fluentd
    fluent_sender = sender.FluentSender('secret_fluentd', host=FLUENTD_HOST, port=int(FLUENTD_PORT))
    # 创建一个自定义的Loguru处理器
    class FluentdHandler:
        def __init__(self):
            logger.log("INFOR", "Start getting public ip address")
            while True:
                self.ip = get_external_ip()
                if self.ip is not None:
                    logger.log("INFOR", f"Get the public ip address is {self.ip}")
                    break

            self.hostname = get_hostname()
        def write(self, message):
            # 解析Loguru日志消息
            log_message = message.strip()
            # 将日志消息发送到Fluentd
            fluent_sender.emit('log', {'message': log_message, "ip": self.ip, "hostname": self.hostname})

    # 添加自定义处理器到Loguru
    logger.add(FluentdHandler(), level="INFOR")
