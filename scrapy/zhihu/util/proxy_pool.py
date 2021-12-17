# -*- coding: utf-8 -*-
# ProjectName:  ZhiHuSpider
# FileName:     proxy_pool
# Description:  
# CreateDate:   2021/12/16

import os
import requests

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


class ProxyPool(object):

    def __init__(self):
        self.host = PROXY_POOL_HOST
        self.port = PROXY_POOL_PORT

    def get_proxy(self):
        return requests.get("http://{}:{}/get/".format(self.host, self.port)).json()

    def delete_proxy(self, proxy):
        res = requests.get("http://{}:{}/delete/?proxy={}".format(self.host, self.port, proxy))
        if res.status_code == 200:
            return "代理 {} 已成功删除".format(proxy)
        else:
            return "代理删除失败！"

    def get_response(self, url, headers, params=None, retry_count=5):
        proxy = self.get_proxy().get('proxy')
        while retry_count > 0:
            try:
                response = requests.get(
                    url=url,
                    headers=headers,
                    params=params,
                    proxies={"http": "http://{}".format(proxy)},
                    timeout=5
                )
                return response
            except Exception:
                retry_count -= 1
        self.delete_proxy(proxy)
        return "代理 {} 已成功删除".format(proxy)
