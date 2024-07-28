from modules.database.db import conn_db
from config import settings

if __name__ == '__main__':
    # 获取需要扫描的资产数据
    query = {}
    if settings.SUBDOMAIN_ASSERT_NAME != "all":
        assert_names = settings.SUBDOMAIN_ASSERT_NAME.split(",")
        query = {"assert_name": {"$in": assert_names}}
    collection = conn_db("asserts")
    records = collection.find(query)
    datas = list()
    for record in records:
        datas.append(record)

    # 获取启用的扫描模块
    scan_modules = settings.SUBDOMAIN_MODULE.split(",")
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