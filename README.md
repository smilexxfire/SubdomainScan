# SubdomainScan
子域名扫描子系统
## 概述
SubdomainScan是一款分布式子域名扫描系统，允许轻松集成多种子域名扫描工具，目前支持subfinder、amass、oneforall

## 项目依赖
- mongo（**必须**，数据库，存放扫描结果）
- rabbitmq（**必须**，消息队列，用于存放、消费扫描任务）
- [heartbeat](https://github.com/smilexxfire/FlaskHeartBeat)（可选，心跳监控，定时发送udp心跳，需部署安装服务端）
- fluentd（可选，控制台日志同步给fluentd处理）

## 支持平台/语言
Windows/Linux

建议使用python3.8及以上
## 使用
### 扫描节点(消费者)部署
推荐使用docker部署运行
```shell
docker run -d \
  --name subdomainscan \
  --restart=always \
  -e rabbitmq_host=xxx \
  -e rabbitmq_port=5672 \
  -e rabbitmq_username=xxx \
  -e rabbitmq_password=xxx \
  -e rabbitmq_queue_name=subdomain \
  -e mongo_host=xxx \
  -e mongo_port=27017 \
  -e mongo_username=xxx \
  -e mongo_password=xxx \
  -e mongo_database=src \
  smilexxfire/subdomainscan
```
若部署了可选配置，添加以下环境变量
```shell
  -e heartbeat_open=true \
  -e heartbeat_host=xxx \
  -e heartbeat_port=5006 \
  -e fluentd_open=true \
  -e fluentd_host=xxxx \
  -e fluentd_port=24224 \
  -e fluentd_match=secret_subdomainscan
```
通过源代码
```shell
git clone https://github.com/smilexxfire/SubdomainScan.git
pip install -r requirements.txt
# linux需要添加可执行权限
chmod +x thirdparty/*
```
修改`config/default.ini`配置文件，填入对应配置值

接着运行`python subdomain_worker.py`即可开启监听，等待任务发布
#### oneforall
oneforall扫描节点需单独部署：[文档](https://github.com/smilexxfire/OneForallForMe)

### 生产者(发布扫描任务)部署
目前仅提供源代码的方式部署
```shell
git clone https://github.com/smilexxfire/SubdomainScan.git
pip install -r requirements.txt
```
修改`producer.py`文件

接着运行`python producer.py`即可发布扫描任务，若需要通过资产名称一键发送多个任务，需部署[资产管理子系统](https://github.com/smilexxfire/AssertManager)
