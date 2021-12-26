## 链家租房爬虫
#### 你可以通过它获取链家网上的房屋出租信息，包括城市、区县、商圈、小区、经纬度、楼层、面积、朝向、月租金等字段，并将数据存入自己的数据库中。
### 涉及技术
##### 编程语言：Python
##### 存储容器：MongoDB
##### 访问伪装：IP代理池
### 关于IP代理池
##### 我用到的IP代理池来源于下面这个项目，大家可以自行阅读文档进行搭建。
##### https://github.com/jhao104/proxy_pool
### 下载代码
```
git clone https://github.com/xll-1994/LianJiaZuFangSpider.git
```
### 安装依赖
```
pip3 install -r requirements.txt
```
### 配置信息
##### 修改 config 目录下的 config.ini 可以配置对IP代理池的调用和数据库的连接。
```
[proxy_pool_config]
host = 127.0.0.1
port = 5010

[mongo_db_config]
host = 127.0.0.1
port = 27017
user = username
password = password
database = lian_jia
collection = zu_fang

[spider_config]
interval_min_time = 1
interval_max_time = 5
rest_min_time = 2
rest_max_time = 5
```
##### 程序默认爬取的是【杭州】的房屋出租信息，如果想要爬取其它城市的信息或全国范围内的信息，可以在 main.py 中修改。
### 运行程序
```
python3 main.py
```
### 问题反馈
##### 涉及该程序的任何问题，欢迎大家在 [Issues](https://github.com/xll-1994/Spider-Collection/issues) 中进行反馈。