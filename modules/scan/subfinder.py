import datetime
import json
import subprocess

import pymongo

from common.module import Module
from config import settings
from modules.database.db import conn_db
from common.utils import delete_file_if_exists

class Subfinder(Module):
    def __init__(self, task:dict):
        """

        @param task: dict,必须包含domain, assert_name字段
        """
        Module.__init__(self)
        self.source = "subfinder_module"
        self.domain = task["domain"]
        self.assert_name = task["assert_name"]

        self.result_file = str(settings.result_save_dir.joinpath("subfinder.temp.json"))
        if settings.PLATFORM == "Linux":
            self.execute_path = str(settings.third_party_dir.joinpath("subfinder"))
        elif settings.PLATFORM == "Windows":
            self.execute_path = str(settings.third_party_dir.joinpath("subfinder.exe"))


    def do_scan(self):
        """
        执行扫描任务

        @return:
        """
        cmd = [self.execute_path, "-d", self.domain, "-oJ", "-o", self.result_file]
        subprocess.run(cmd)

    def deal_data(self):
        """
        处理扫描结果, 提取出所有子域

        @return:
        """
        # 从文件中读取数据
        with open(self.result_file, "r") as f:
            datas = f.readlines()
            json_list = [json.loads(data) for data in datas]
            for data in json_list:
                self.subdomains.add(data["host"])
        # 格式化子域
        for subdomain in self.subdomains:
            data = {
                "subdomain": subdomain,
                "domain": self.domain,
                "insert_time": datetime.datetime.now(),
                "scan_from": self.source,
                "assert_name": self.assert_name
            }
            self.results.append(data)

    def save_db(self):
        if len(self.results) == 0:
            return
        # 存入数据库
        try:
            db = conn_db("subdomain")
            db.insert_many(self.results, ordered=False)
        except pymongo.errors.BulkWriteError as e:
            for error in e.details['writeErrors']:
                if error['code'] == 11000:  # E11000 duplicate key error collection，忽略重复主键错误
                    pass
                    # print(f"Ignoring duplicate key error for document with _id {error['op']['_id']}")
                else:
                    raise  # 如果不是重复主键错误，重新抛出异常
    def delete_temp(self):
        delete_file_if_exists(self.result_file)

    def run(self):
        """
        入口执行函数

        @return:
        """
        self.begin()
        self.do_scan()
        self.deal_data()
        self.save_db()
        self.finish()
        self.delete_temp()

def run(task: dict):
    """
    类调用统一入口
    
    @return: 
    """
    subfinder = Subfinder(task)
    subfinder.run()

if __name__ == '__main__':
    run({"domain": "xxf.world", "assert_name": "测试"})