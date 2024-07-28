import json

from modules.database.db import conn_db
from modules.database.producer import RabbitMQProducer
from config import settings

def publish_subdomain_task():
    # 获取启用的扫描模块
    scan_modules = settings.SUBDOMAIN_MODULE.split(",")
    scan_modules = list(map(str.strip, scan_modules))  # 消除无效字符

    # 获取需要扫描的资产名称
    query = {}
    if settings.SUBDOMAIN_ASSERT_NAME != "all":
        assert_names = settings.SUBDOMAIN_ASSERT_NAME.split(",")
        query = {"assert_name": {"$in": assert_names}}
    collection = conn_db("asserts")
    records = collection.find(query)
    datas = list()
    for record in records:
        datas.append(record)


    # 发布扫描任务
    producer = RabbitMQProducer("subdomain")
    for data in datas:
        for module_name in scan_modules:
            task = {
                "assert_name": data["assert_name"],
                "domain": data["domain"],
                "module_name": module_name
            }
            producer.publish_message(json.dumps(task))

def purge_subdomain_queue():
    """
    清空子域名队列

    @return:
    """
    producer = RabbitMQProducer("subdomain")
    producer.purge_queue()

if __name__ == '__main__':
    # publish_subdomain_task()
    purge_subdomain_queue()