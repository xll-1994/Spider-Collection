# -*- coding: utf-8 -*-
# ProjectName:  LianJiaZuFangSpider
# FileName:     proxy_pool
# Description:  对IP代理池进行封装
# CreateDate:   2021/12/11

import requests
from setting import PROXY_POOL_HOST, PROXY_POOL_PORT


class ProxyPool:
    def __init__(self):
        self.host = PROXY_POOL_HOST
        self.port = PROXY_POOL_PORT

    def get_proxy(self):
        return requests.get("http://{}:{}/get/".format(self.host, self.port)).json()

    def delete_proxy(self, proxy):
        return requests.get("http://{}:{}/delete/?proxy={}".format(self.host, self.port, proxy))

    def get_response(self, url, headers, params=None, retry_count=5, city_id=None):
        proxy = self.get_proxy().get('proxy')
        while retry_count > 0:
            try:
                response = requests.get(
                    url=url,
                    headers=headers,
                    params=params,
                    proxies={"http": "http://{}".format(proxy)},
                    cookies={
                        'select_city': city_id
                    },
                    timeout=10
                )
                return response
            except Exception:
                retry_count -= 1
        self.delete_proxy(proxy)
        return None
