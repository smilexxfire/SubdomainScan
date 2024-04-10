from config.config import logger
import os
import sys
from modules.database import conn_db
import pymongo
def check():
    # 检查配置文件是否存在
    print("检查配置文件是否存在...")
    if not os.path.exists("config/default.ini"):
        logger.error("配置文件不存在，请编写config/default.ini文件")
        sys.exit(1)
    # 检查数据库连接是否正常
    print("检查数据库连接...")
    db = conn_db("subdomain")
    # 为数据库创建索引
    try:
        # 创建索引
        db.create_index([("subdomain", pymongo.ASCENDING)])
        print("创建索引...")
    except pymongo.errors.OperationFailure as e:
        # 检查错误消息是否为索引已存在的错误
        if "An existing index has the same name as the requested index" in str(e):
            print("索引已存在...")
        else:
            # 如果错误消息不是索引已存在的错误，则重新引发异常
            raise e
    print("检查通过 enjoy it...")

if __name__ == '__main__':
    check()