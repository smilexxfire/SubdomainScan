# -*- coding: UTF-8 -*-
'''
@Project ：subdomainMonitor 
@File    ：amass.py
@IDE     ：PyCharm 
@Author  ：smilexxfire
@Email   : xxf.world@gmail.com
@Date    ：2024/8/25 13:04 
@Comment ： 
'''
import json
import os
import subprocess
from common.module import Module
from common.task import Task
from config.log import logger

class Amass(Module, Task):
    def __init__(self, domain: str, task_id):
        """

        @param task: dict,必须包含domain, assert_name字段
        """
        self.module = "subdomainscan"
        self.source = "amass"
        self.collection = "subdomain"
        self.domain = domain
        Module.__init__(self)
        Task.__init__(self, task_id)

    def do_scan(self):
        """
        执行扫描任务

        @return:
        """
        cmd = [self.execute_path, "enum", "-d", self.domain, "-json", self.result_file]
        subprocess.run(cmd)

    def deal_data(self):
        """
        处理扫描结果, 提取出所有子域

        @return:
        """
        if not os.path.exists(self.result_file):
            logger.log("ERROR", "扫描结果文件不存在")
        res_list = list()
        # 从文件中读取数据
        with open(self.result_file, "r") as f:
            datas = f.readlines()
            json_list = [json.loads(data) for data in datas]
            for data in json_list:
                res_list.append({
                    "domain": data["domain"],
                    "subdomain": data["name"],
                })
        self.results = res_list

    def save_db(self):
        super().save_db()

    def run(self):
        """
        入口执行函数

        @return:
        """
        self.receive_task()
        self.begin()
        self.do_scan()
        self.deal_data()
        self.save_db()
        self.finish()
        self.delete_temp()
        self.finnish_task(time_escape=self.elapse, lens=len(self.results))


def run(target: str, task_id: str):
    """
    类调用统一入口

    @return:
    """
    amass = Amass(target, task_id)
    amass.run()


if __name__ == '__main__':
    run(target="xxf.world", task_id="123213043-432432")
    # run(targets=["r3col.top", "boc-samsunglife.cn"])
