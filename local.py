from modules.database import conn_db
from config.config import SUBDOMAIN_MODULE, SUBDOMAIN_ASSERT_NAME
from modules.subdomain import Subdomain

if __name__ == '__main__':
    # 获取需要扫描的资产名称
    query = {}
    if SUBDOMAIN_ASSERT_NAME != "all":
        assert_names = SUBDOMAIN_ASSERT_NAME.split(",")
        query = {"assert_name": {"$in": assert_names}}
    collection = conn_db("asserts")
    records = collection.find(query)
    datas = list()
    for record in records:
        datas.append(record)

    # 获取启用的扫描模块
    scan_modules = SUBDOMAIN_MODULE.split(",")
    scan_modules = list(map(str.strip, scan_modules))  # 消除无效字符

    # 开始扫描
    for data in datas:
        for module_name in scan_modules:
            task = {
                "assert_name": data["assert_name"],
                "domain": data["domain"],
                "module_name": module_name
            }
            Subdomain.start(task)