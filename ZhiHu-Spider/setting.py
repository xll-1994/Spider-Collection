# -*- coding: utf-8 -*-
# ProjectName:  ZhiHu-Spider
# FileName:     setting
# Description:  
# CreateDate:   2021/12/25

# ---------- SPIDER INFO ---------- #
VERSION = '1.0.1'
# ---------- SPIDER INFO ---------- #

# ---------- EXPORT INFO ---------- #
USE_MYSQL = 1
USE_MONGO = 0
USE_XLS = 0
# ---------- EXPORT INFO ---------- #

# ---------- MYSQL CONFIG ---------- #
MYSQL_HOST = '127.0.0.1'
MYSQL_PORT = 3306
MYSQL_USERNAME = 'username'
MYSQL_PASSWORD = 'password'
MYSQL_DATABASE = 'zhi_hu_db'
# ---------- MYSQL CONFIG ---------- #

# ---------- MYSQL CONFIG ---------- #
MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27017
MONGO_USERNAME = 'username'
MONGO_PASSWORD = 'password'
MONGO_DATABASE = 'zhi_hu_db'
# ---------- MYSQL CONFIG ---------- #

# ---------- REDIS CONFIG ---------- #
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_PASSWORD = 'password'
REDIS_DB = 1
CRAWLING_TABLE = 'crawling_table'
CRAWLED_TABLE = 'crawled_table'
CRAWLING_ANSWER = 'crawling_answer'
# ---------- REDIS CONFIG ---------- #

# ---------- PROXY CONFIG ---------- #
PROXY_HOST = '127.0.0.1'
PROXY_PORT = 5010
# ---------- PROXY CONFIG ---------- #

# ---------- REQUEST CONFIG ---------- #
RETRY_TIME = 3
RETRY_INTERVAL = 2
TIMEOUT = 5
# ---------- REQUEST CONFIG ---------- #
