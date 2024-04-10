# subdomainMonitor
子域名监控子系统
## 概述
定时对指定域名进行子域名扫描，并将结果存入数据库，同时对变化内容进行消息推送，支持多种子域名扫描工具，支持分布式运行即多个consumer。


## 项目依赖
- mongo
- rabbitmq
- [资产管理子系统部署](https://github.com/smilexxfire/assertManager)
- subdomain扫描工具
  - subfinder：环境变量中配置好即可
  - xray：需在modules/subdomain.py中修改xray_scan方法的bin_directory变量为xray所在目录（仅xray高级版支持子域名扫描

平台支持
- Linux
## 使用
1. `pip install -r requirements.txt`
2. 修改配置文件default.ini.sample，并重命名为default.ini
3. `python3 main.py` 检查环境，自动创建数据库索引
4. 生产者：运行`python3 producer.py`会自动查询数据库获取主域名，接着将任务发布到rabbitmq
5. 消费者：运行`python3 consumer.py`会自动在mq中取出消息并执行，支持多个consumer

