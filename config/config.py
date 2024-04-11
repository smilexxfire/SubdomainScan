import os
import platform

from modules.logger import Logger
from modules.notifier import Notifier
from utils.tools import read_ini_config

# 是否开启消息通知
NOTICE_SWITCH = True if read_ini_config("notifier", "switch") == "on" else False
NOTIFIER = None
if NOTICE_SWITCH == True:
    NOTIFIER = Notifier.get_notifier()  # 全局的NOTIFIER
NOTICE_KEYWORD = read_ini_config("notifier", "keyword")
NOTICE_TIME = read_ini_config("notifier", "scan_and_notice_time")
#项目绝对路径
PROJECT_DIRECTORY = os.path.dirname(os.path.abspath(__file__)) + "/../"
# Windows/Linux
PLATFORM = platform.system()
# 子域名模块相关记录
SUBDOMAIN_MODULE = read_ini_config("subdomain", "module")
SUBDOMAIN_ASSERT_NAME = read_ini_config("subdomain", "assert_name")
# 全局的日志
logger = Logger()