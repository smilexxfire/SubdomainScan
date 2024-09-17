# -*- coding: UTF-8 -*-
'''
@Project ：subdomainMonitor 
@File    ：subdomain_producer.py
@IDE     ：PyCharm 
@Author  ：smilexxfire
@Email   : xxf.world@gmail.com
@Date    ：2024/7/29 17:44 
@Comment ： 生产者，用于产生扫描任务
'''
import json
import uuid

from common.database.producer import RabbitMQProducer
from common.database.db import conn_db
from common.utils import is_chinese
from common.task import Task

def purge_queue(queue_name):
    """
    清空队列

    :param queue_name: 队列名称
    :return:
    """
    producer = RabbitMQProducer(queue_name)
    producer.purge_queue()

def send_task(queue_name, task):
    producer = RabbitMQProducer(queue_name)
    producer.publish_message(json.dumps(task))
    # 存储任务状态为produced
    task_info = Task(task_id=task["task_id"])
    task_info.produce(task["domain"],module="subdomainscan", source=task["module_name"])

def subdomain_producer_multi(assert_name:str, module:str):
    """
    通过资产名称，定位所有主域并发送到任务队列

    :param assert_name: 资产名称
    :param module: 启动的扫描模块
    :return:
    """
    queue_name = "subdomain_custom_task"
    if module == "oneforall":
        queue_name = "subdomain_oneforall_task"

    db = conn_db("asserts")
    records = db.find({
        "assert_name": assert_name
    })

    for record in records:
        if is_chinese(record["domain"]):
            continue
        task = {
            "domain": record["domain"],
            "module_name": module
        }
        send_task(queue_name, task)

def subdomain_producer_specified(domains:list, module:str):
    '''
    发送指定的域名列表任务

    :param domains: list，需要扫描的子域名列表
    :param module: 使用的扫描模块
    :return:
    '''
    queue_name = "subdomain_custom_task"
    if module == "oneforall":
        queue_name = "subdomain_oneforall_task"

    for domain in domains:
        if is_chinese(domain):
            continue
        task = {
            "domain": domain,
            "module_name": module,
            "task_id": str(uuid.uuid4())
        }
        send_task(queue_name, task)


if __name__ == '__main__':
    # subdomain_producer_multi("百度", module="oneforall")
    # subdomain_producer_multi("百度", module="subfinder")
    # subdomain_producer_multi("字节跳动", module="oneforall")
    # subdomain_producer_multi("字节跳动", module="subfinder")
    # for _ in range(100):
    #     subdomain_producer_specified(["baidu.com"], "subfinder")
    subdomain_producer_specified(["cee.edu.cn"], "subfinder")
