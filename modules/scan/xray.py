import datetime
import json
import subprocess
import pymongo
from common.module import Module
from common.utils import delete_file_if_exists
from config import settings
from modules.database.db import conn_db

class XRAY(Module):
    def __init__(self, task:dict):
        """

        @param task: dict,必须包含domain, assert_name字段
        """
        Module.__init__(self)
        self.source = "xray_module"
        self.domain = task["domain"]
        self.assert_name = task["assert_name"]

        self.result_file = str(settings.result_save_dir.joinpath("xray.temp.json"))
        if settings.PLATFORM == "Linux":
            self.execute_path = str(settings.third_party_dir.joinpath("xray"))
        elif settings.PLATFORM == "Windows":
            self.execute_path = str(settings.third_party_dir.joinpath("xray.exe"))


    def do_scan(self):
        """
        执行扫描任务

        @return:
        """
        cmd = [self.execute_path, "subdomain", "--target",
               self.domain, "--json-output", self.result_file]
        subprocess.run(cmd)

    def deal_data(self):
        """
        处理扫描结果, 提取出所有子域

        @return:
        """
        # 从文件中读取数据
        with open(self.result_file, "r") as f:
            datas = f.readlines()
            for data in datas:
                data = data.strip().strip(",")  # 去除干扰字符
                try:
                    data = json.loads(data)
                    self.subdomains.add(data["domain"])
                except:
                    pass
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
        # self.do_scan()
        self.deal_data()
        self.save_db()
        self.finish()
        self.delete_temp(self.result_file)

def run(task: dict):
    """
    类调用统一入口

    @return:
    """
    xray = XRAY(task)
    xray.run()


if __name__ == '__main__':
    run({"domain": "xxf.world", "assert_name": "测试"})

