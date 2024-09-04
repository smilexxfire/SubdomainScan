"""
Module base class
"""

import time
import pymongo

from common.database.db import conn_db
from common.utils import delete_file_if_exists
from config import settings
from config.log import logger

class Module(object):
    def __init__(self, target:str=None, targets:list=None):
        self.results = list()  # 存放模块结果
        self.targets = self.get_targets(target, targets)    # 存放所有模板
        if self.targets is None:
            raise ValueError("domains cannot be None. Initialization failed.")

        self.start = time.time()  # 模块开始执行时间
        self.end = None  # 模块结束执行时间
        self.elapse = None  # 模块执行耗时

        self.targets_file = str(settings.result_save_dir.joinpath("targets.temp.txt"))
        self.result_file = str(settings.result_save_dir.joinpath("result.temp.json"))
        self.set_execute_path()

    def begin(self):
        """
        begin log
        """
        logger.log('INFOR', f'Start {self.source} module')

    def get_targets(self, target: str = None, targets: list = None):
        if target is None and targets is None:
            return None
        result = []
        if target is not None:
            result.append(target)
        if targets is not None:
            result.extend(targets)
        return result

    def finish(self):
        """
        finish log
        """
        self.end = time.time()
        self.elapse = round(self.end - self.start, 1)
        logger.log('INFOR', f'Finished {self.source} module took {self.elapse} seconds find {len(self.results)} subdomains'
                            f' of {self.domain}')

    def delete_temp(self):
        delete_file_if_exists(self.result_file)
        delete_file_if_exists(self.targets_file)

    def set_execute_path(self):
        if settings.PLATFORM == "Linux":
            self.execute_path = str(settings.third_party_dir.joinpath(self.source))
        elif settings.PLATFORM == "Windows":
            self.execute_path = str(settings.third_party_dir.joinpath(self.source + ".exe"))
    def save_targets(self):
        with open(self.targets_file, "w") as f:
            for domain in self.targets:
                f.write(domain.strip() + "\n")

    def save_db(self, collection):
        """
        Save module results into the database
        """
        logger.log('INFOR', f'Start save db results')
        if len(self.results) == 0:
            return

        while True:
            # 存入数据库
            try:
                db = conn_db(collection)
                db.insert_many(self.results, ordered=False)
                return
            except pymongo.errors.BulkWriteError as e:
                for error in e.details['writeErrors']:
                    if error['code'] == 11000:  # E11000 duplicate key error collection，忽略重复主键错误
                        return
                        # print(f"Ignoring duplicate key error for document with _id {error['op']['_id']}")
                    else:
                        logger.log("ERROR",f"{error['code']}: {error['message']}")
                        logger.log("INFOR", "尝试重新save_db....")
            except Exception as e:
                logger.log("ERROR", f"error：{e}")
                logger.log("INFOR", "尝试重新save_db....")