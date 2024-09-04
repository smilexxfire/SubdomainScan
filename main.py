# -*- coding: UTF-8 -*-
'''
@Project ：subdomainMonitor 
@File    ：main.py
@IDE     ：PyCharm 
@Author  ：smilexxfire
@Email   : xxf.world@gmail.com
@Date    ：2024/9/3 9:18 
@Comment ： 环境检查、数据库索引创建
'''
from config.log import logger
import os
import sys
from common.database.db import conn_db
import pymongo

def check_dep():

    # 检查配置文件是否存在
    logger.log("INFO","检查配置文件是否存在...")
    if not os.path.exists("config/default.ini"):
        logger.log("ERROR", "配置文件不存在，请编写config/default.ini文件")
        sys.exit(1)
    # 检查数据库连接是否正常
    logger.log("INFO", "检查数据库连接...")
    db = conn_db("subdomain")

def create_index(collection, field_name):
    # 为数据库创建索引
    db = conn_db(collection)
    try:
        # 创建索引
        db.create_index([(field_name, pymongo.ASCENDING)], unique=True)
        logger.log("INFO", f"创建{collection}库{field_name}字段索引...")
    except pymongo.errors.OperationFailure as e:
        # 检查错误消息是否为索引已存在的错误
        if "An existing index has the same name as the requested index" in str(e):
            logger.log("INFO", f"{field_name}索引已存在...")
        else:
            # 如果错误消息不是索引已存在的错误，则重新引发异常
            raise e


if __name__ == '__main__':
    check_dep()
    create_index("asserts", "domain")
    create_index("comments", "assert_name")
    create_index("subdomain", "subdomain")
    create_index("dns_record", "host")
    create_index("waf_detect", "ip")
