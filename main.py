from config.log import logger
import os
import sys
from modules.database.db import conn_db
import pymongo

def check_dep():

    # 检查配置文件是否存在
    logger.log("INFO","检查配置文件是否存在...")
    logger.log("INFO","检查配置文件是否存在...")
    if not os.path.exists("config/default.ini"):
        logger.log("ERROR", "配置文件不存在，请编写config/default.ini文件")
        sys.exit(1)
    # 检查数据库连接是否正常
    logger.log("INFO", "检查数据库连接...")
    db = conn_db("subdomain")

def create_index():
    # 为数据库创建索引
    db = conn_db("subdomain")
    try:
        # 创建索引
        db.create_index([("subdomain", pymongo.ASCENDING)])
        logger.log("INFO", "创建索引...")
    except pymongo.errors.OperationFailure as e:
        # 检查错误消息是否为索引已存在的错误
        if "An existing index has the same name as the requested index" in str(e):
            logger.log("INFO", "索引已存在...")
        else:
            # 如果错误消息不是索引已存在的错误，则重新引发异常
            raise e
    logger.log("INFO", "检查通过 enjoy it...")

if __name__ == '__main__':
    check_dep()
    create_index()