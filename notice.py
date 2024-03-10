from collections import defaultdict
from datetime import datetime

from modules.database import conn_db
from modules.notifier import NotifierFactory
import schedule
import time
from config.config import NOTICE_KEYWORD

def notice_task():
    # 获取当前日期
    current_date = datetime.utcnow()

    # 获取今天的开始时间（凌晨）
    start_of_day = datetime(current_date.year, current_date.month, current_date.day)

    # 获取今天的结束时间（23:59:59）
    end_of_day = datetime(current_date.year, current_date.month, current_date.day, 23, 59, 59)

    # 构建查询条件
    query = {
        "insert_time": {
            "$gte": start_of_day,
            "$lte": end_of_day
        }
    }

    db = conn_db("subdomain")
    results = db.find(query)

    # 统计 assert_name 字段的值及对应记录条数
    assert_name_count = defaultdict(int)

    for result in results:
        assert_name = result.get("assert_name")
        if assert_name:
            assert_name_count[assert_name] += 1

    notifier = NotifierFactory.get_notifier()
    message = NOTICE_KEYWORD + "\n"
    if len(list(results)) == 0:
        response = notifier.send_message(message + "Count: 0")
        exit(0)
    # 打印统计结果
    for assert_name, count in assert_name_count.items():
        print(f"assert_name: {assert_name}, Count: {count}")
        message = message + f"assert_name: {assert_name}, Count: {count}\n"
    # 发送结果
    notifier.send_message(message)

# 设置每天晚上10点调用notice_task方法
schedule.every().day.at("23:09").do(notice_task)

while True:
    schedule.run_pending()
    time.sleep(30)

