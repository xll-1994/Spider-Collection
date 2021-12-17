# -*- coding: utf-8 -*-
# ProjectName:  ZhiHuSpider
# FileName:     proxy_pool
# Description:  
# CreateDate:   2021/12/16

import os

# use_proxy = 1 ，代表开启代理池，需要配置代理池的 host 和 port 信息
# use_proxy = 0 ，代表关闭代理池
use_proxy = 1

# 有关proxy_pool的信息
PROXY_POOL_HOST = os.environ.get('PROXY_POOL_HOST', '127.0.0.1')
PROXY_POOL_PORT = int(os.environ.get('PROXY_POOL_PORT', 5010))

if use_proxy == 1:
    proxy_pool_url = "http://{}:{}/get/".format(PROXY_POOL_HOST, PROXY_POOL_PORT)
else:
    proxy_pool_url = None
