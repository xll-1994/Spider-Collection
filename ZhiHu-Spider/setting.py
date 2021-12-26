# -*- coding: utf-8 -*-
# ProjectName:  ZhiHu-Spider
# FileName:     setting
# Description:  
# CreateDate:   2021/12/25

# ---------- SPIDER INFO ---------- #
VERSION = '1.0.1'
# ---------- SPIDER INFO ---------- #

# ---------- SPIDER CONFIG ---------- #
# 默认线程数为1个
THREAD_NUM = 2
# 默认每个请求发起前睡眠1秒
INTERVAL_TIME = 1
# ---------- SPIDER CONFIG ---------- #

# ---------- EXPORT INFO ---------- #
# 默认使用.xls文件存储导出的数据
USE_MYSQL = 0
USE_MONGO = 0
USE_XLS = 1
# ---------- EXPORT INFO ---------- #

# ---------- MYSQL CONFIG ---------- #
# 当使用mysql存储导出的数据时，需要配置
MYSQL_HOST = '127.0.0.1'
MYSQL_PORT = 3306
MYSQL_USERNAME = 'username'
MYSQL_PASSWORD = 'password'
MYSQL_DATABASE = 'zhi_hu_db'
# ---------- MYSQL CONFIG ---------- #

# ---------- MONGO CONFIG ---------- #
# 当使用mysql存储导出的数据时，需要配置
MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27017
MONGO_USERNAME = 'username'
MONGO_PASSWORD = 'password'
MONGO_DATABASE = 'zhi_hu_db'
# ---------- MONGO CONFIG ---------- #

# ---------- REDIS CONFIG ---------- #
# 默认不开启REDIS存储爬取过程中的数据
USE_REDIS = 0
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_PASSWORD = 'password'
REDIS_DB = 1
CRAWLING_TABLE = 'crawling_table'
CRAWLED_TABLE = 'crawled_table'
CRAWLING_ANSWER = 'crawling_answer'
# ---------- REDIS CONFIG ---------- #

# ---------- PROXY CONFIG ---------- #
# 启用代理进行访问时，需保证已配置对应的API访问接口
USE_PROXY = 0
PROXY_HOST = '127.0.0.1'
PROXY_PORT = 5010
# ---------- PROXY CONFIG ---------- #

# ---------- REQUEST CONFIG ---------- #
RETRY_TIME = 3
RETRY_INTERVAL = 2
TIMEOUT = 5
# ---------- REQUEST CONFIG ---------- #
