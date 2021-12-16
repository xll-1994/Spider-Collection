# -*- coding: utf-8 -*-
# ProjectName:  ZhiHuSpider
# FileName:     proxy_pool
# Description:  
# CreateDate:   2021/12/16

# use_proxy = 1 ，代表开启代理池，需要配置代理池的 host 和 port 信息
# use_proxy = 0 ，代表关闭代理池
use_proxy = 1

# 配置代理的 host 和 port 信息
host = '81.70.54.179'
port = 5010

if use_proxy == 1:
    proxy_pool_url = "http://{}:{}/get/".format(host, port)
else:
    proxy_pool_url = None
