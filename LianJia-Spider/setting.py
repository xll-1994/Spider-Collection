# -*- coding: utf-8 -*-
# ProjectName:  LianJia-Spider
# FileName:     setting
# Description:  
# CreateDate:   2021/12/17
import os

# proxy_pool的相关信息
PROXY_POOL_HOST = os.environ.get('PROXY_POOL_HOST', '127.0.0.1')
PROXY_POOL_PORT = int(os.environ.get('PROXY_POOL_PORT', 5010))

# mongodb的相关信息
MONGODB_HOST = os.environ.get('MONGODB_HOST', '127.0.0.1')
MONGODB_PORT = int(os.environ.get('MONGODB_PORT', 27017))
MONGODB_USER = os.environ.get('MONGODB_USER', 'username')
MONGODB_PASSWORD = os.environ.get('MONGODB_PASSWORD', 'password')
MONGODB_DATABASE = 'lian_jia'
MONGODB_COLLECTION = 'zu_fang_all'

# spider的相关信息
INTERVAL_MIN_TIME = 1
INTERVAL_MAX_TIME = 5
REST_MIN_TIME = 2
REST_MAX_TIME = 5
