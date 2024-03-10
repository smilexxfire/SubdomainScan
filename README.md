# subdomainMonitor
子域名监控子系统
## 概述
定时对指定域名进行子域名扫描，并将结果存入数据库，同时对变化内容进行消息推送，支持多种子域名扫描工具。


项目依赖
- mongo
- rabbitmq
- [资产管理子系统部署](https://github.com/smilexxfire/assertManager)

平台支持
- Linux
## 使用
1. `pip install -r requirements.txt`
2. 修改配置文件default.ini.sample，并重命名为default.ini
3. mongodb中运行mongo.db文件内两行语句，为子域名集合创建索引
4. 生产者：运行`python producer.py`会自动查询数据库获取主域名，接着将任务发布到rabbitmq
5. 消费者：运行`python consumer.py`会自动在mq中取出消息并执行，支持多个consumer

