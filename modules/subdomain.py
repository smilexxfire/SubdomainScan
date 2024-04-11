import datetime
import json
import os

import pymongo

from config.config import PROJECT_DIRECTORY
import subprocess
from config.config import logger
from modules.database import conn_db
from utils.tools import rename_dict_key, delete_file_if_exists
from utils.tools import read_ini_config


class Subdomain(object):
    DB_COLLECTION = "subdomain"
    PREFIX = "[subdomain]"  # 日志前缀
    def __init__(self):
        pass

    @classmethod
    def data_deal(cls, source: str, filename: str, input):
        """用于扫描结果数据的整合、插入数据库

        :param source: 数据来源: xray/subfiner/xxx
        :param filename: 扫描结果保存的位置
        :param input: 任务接收的输入
        :return:
        """
        db = conn_db(cls.DB_COLLECTION)
        logger.info(f"{cls.PREFIX}数据入库中....")
        if not os.path.isfile(filename):  # 扫描结果为空的情况
            return
        insert_data_list = list()
        # 打开文件并读取内容
        with open(filename, 'r', encoding="utf8") as f:
            if source == "xray":
                datas = f.readlines()
                for data in datas:
                    data = data.strip().strip(",")  # 去除干扰字符
                    try:
                        data = json.loads(data)
                        # 新增一个插入时间字段
                        data["insert_time"] = datetime.datetime.now()
                        # 新增扫描源
                        data["scan_from"] = "xray"
                        # 新增归属资产名称
                        data["assert_name"] = input["assert_name"]
                        # 删除无关项
                        del data["cname"]
                        del data["ip"]
                        del data["web"]
                        del data["extra"]
                        del data["verbose_name"]
                        rename_dict_key(data, "domain", "subdomain")
                        rename_dict_key(data, "parent", "domain")
                        # 添加到插入记录列表
                        insert_data_list.append(data)
                    except:
                        pass
            elif source == "subfinder":
                # 从文件中读取数据
                datas = f.readlines()
                json_list = [json.loads(data) for data in datas]
                for data in json_list:
                    del data["source"]
                    # 新增一个插入时间字段
                    data["insert_time"] = datetime.datetime.now()
                    # 新增源信息
                    data["scan_from"] = "subfinder"
                    # 新增归属资产名称
                    data["assert_name"] = input["assert_name"]
                    # 统一字段名
                    rename_dict_key(data, "host", "subdomain")
                    rename_dict_key(data, "input", "domain")
                    # 插入记录，已有记录则忽略
                    insert_data_list.append(data)
        # 插入记录
        if not insert_data_list:
            return
        try:
            db = conn_db("subdomain")
            db.insert_many(insert_data_list, ordered=False)
        except pymongo.errors.BulkWriteError as e:
            for error in e.details['writeErrors']:
                if error['code'] == 11000:  # E11000 duplicate key error collection，忽略重复主键错误
                    pass
                    # print(f"Ignoring duplicate key error for document with _id {error['op']['_id']}")
                else:
                    raise  # 如果不是重复主键错误，重新抛出异常
        # 删除文件
        delete_file_if_exists(filename)

    @classmethod
    def subfinder_scan(cls, data):
        """subfinder工具扫描逻辑

        Args:
            target (_type_): 主域
        """
        # 初始化目录
        output_directory = PROJECT_DIRECTORY + "/result/"
        output_filename = output_directory + "/subdomain/" + data["domain"] + ".subfinder.json"
        # 执行命令
        cmd = ["subfinder", "-d", data["domain"], "-oJ", "-o", output_filename]
        logger.info(f"{cls.PREFIX}启动subfinder进行子域名扫描: {cmd}")
        subprocess.run(cmd)
        logger.info(f"{cls.PREFIX}结束subfinder扫描")
        # 结果处理
        cls.data_deal("subfinder", output_filename, data)
        logger.info(f"{cls.PREFIX}subfinder子域名扫描完成, 结果已入库")

    @classmethod
    def xray_scan(cls, data):
        # 初始化目录
        bin_directory = "/Users/xxf/tools/xray/"
        output_directory = PROJECT_DIRECTORY + "/result/"
        output_filename = output_directory + "subdomain/" + data["domain"] + ".xray.json"
        # 已存在则删除
        if os.path.exists(output_filename):
            os.remove(output_filename)
        # 进入xray可执行文件的目录
        os.chdir(bin_directory)
        # 执行命令
        cmd = ["./xray", "subdomain", "--target",
               data["domain"], "--json-output", output_filename]
        logger.info(f"{cls.PREFIX}启动xray进行子域名扫描: {cmd}")
        subprocess.run(cmd)
        logger.info(f"{cls.PREFIX}结束xray扫描")
        # 结果处理
        cls.data_deal("xray", output_filename, data)
        logger.info(f"{cls.PREFIX}xray子域名扫描完成, 结果已入库")

    @classmethod
    def start(cls, data: dict):
        """子域名扫描入口函数

        :param data: 待扫描任务字典，assert_name、domain、module_name
        :return:
        """
        logger.info(f"{cls.PREFIX}子域名模块启动.......")
        try:
            method = getattr(cls, data['module_name'] + "_scan")
            logger.info(f"{cls.PREFIX}启用{data['module_name']}扫描...")
            print(data)
            method(data)
            logger.info(f"{cls.PREFIX}{data['module_name']}扫描结束...")
        except Exception as e:
            logger.error(f"{cls.PREFIX}扫描出错...")
            raise e