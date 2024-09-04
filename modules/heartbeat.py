# -*- coding: UTF-8 -*-
'''
@Project ：subdomainMonitor 
@File    ：heartbeat.py
@IDE     ：PyCharm 
@Author  ：smilexxfire
@Email   : xxf.world@gmail.com
@Date    ：2024/8/25 17:12 
@Comment ： 通过udp推送心跳信息
'''
import datetime
import json
import threading
import socket
import time
from config import settings

class Heartbeat(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.start_time = datetime.datetime.now()
        # 推送到的地址、端口
        self.host = settings.HEARTBEAT_HOST
        self.port = settings.HEARTBEAT_PORT

    def send_heart_beat(self, data:str):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 发送数据:
        s.sendto(data.encode("utf8"), (self.host, int(self.port)))
        s.close()

    def format_duration(self, start_time, end_time):
        duration = end_time - start_time
        hours, remainder = divmod(duration.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours)}小时{int(minutes)}分钟{int(seconds)}秒"


    def run(self):
        while True:
            time.sleep(3)
            self.current_time = datetime.datetime.now()
            message = {
                "hostname": socket.gethostname(),
                "duration": self.format_duration(self.start_time, self.current_time)
            }
            self.send_heart_beat(json.dumps(message))

def main():
    # 创建并启动子线程
    thread1 = Heartbeat(name="线程1")
    thread1.start()

    # 主线程继续执行其他任务
    print("主线程继续执行其他任务")
    for i in range(3):
        print(f"主线程正在做其他事情... {i}")
        time.sleep(2)

    # 等待子线程完成
    thread1.join()
    print("子线程已结束，主线程结束")


if __name__ == "__main__":
    main()