# -*- coding: UTF-8 -*-
'''
@Project ：subdomainMonitor 
@File    ：task.py
@IDE     ：PyCharm 
@Author  ：smilexxfire
@Email   : xxf.world@gmail.com
@Date    ：2024/9/17 21:15 
@Comment ： 
'''
from datetime import datetime

from common.database.db import conn_db
from config.log import logger
from config import settings

class Task(object):
    task_collection = "task"

    def __init__(self, task_id):
        self.task_id = task_id

    def receive_task(self):
        meta = {
            "hostname": settings.HOSTNAME,
            "external_ip": settings.EXTERNAL_IP,
            "plate": settings.PLATFORM
        }
        self.update_task_state(task_state="running", meta=meta)

    def finnish_task(self, time_escape, lens):
        meta = {
            "hostname": settings.HOSTNAME,
            "external_ip": settings.EXTERNAL_IP,
            "plate": settings.PLATFORM,
            "time_escape": time_escape,
            "records_len": lens
        }
        self.update_task_state(task_state="finished", meta=meta)

    def update_task_state(self, task_state, meta=None):
        query = {"task_id": self.task_id}
        while True:
            try:
                db = conn_db(self.task_collection)
                doc = {
                    "task_id": self.task_id,
                    "state": task_state,
                    "meta": meta if meta else {},
                    "timestamp": datetime.now(),
                }
                logger.log("INFOR", "updating task state")
                result = db.update_one(query, {"$set": doc}, upsert=True)
                return
            except Exception as e:
                logger.log("ERROR", f"error：{e}")
                logger.log("INFOR", "尝试重新update_task_state....")

    def produce(self, target, module, source):
        '''
        发布者使用，发布任务后在数据库存储id及状态

        :param target:
        :param module:
        :param source:
        :return:
        '''
        query = {"task_id": self.task_id}
        while True:
            try:
                db = conn_db(self.task_collection)
                doc = {
                    "task_id": self.task_id,
                    "target": target,
                    "module": module,
                    "source": source,
                    "state": "produced",
                    "timestamp": datetime.now()
                }
                logger.log("INFOR", "updating task state")
                result = db.update_one(query, {"$set": doc}, upsert=True)
                return
            except Exception as e:
                logger.log("ERROR", f"error：{e}")
                logger.log("INFOR", "尝试重新update_task_state....")
