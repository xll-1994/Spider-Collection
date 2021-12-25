# -*- coding: utf-8 -*-
# ProjectName:  ZhiHu-Spider
# FileName:     proxy_handler
# Description:  
# CreateDate:   2021/12/25

import requests

from handler import ConfigHandler


class ProxyHandler(object):
    """
    获取代理、删除代理
    """

    def __init__(self):
        conf = ConfigHandler()
        self.host = conf.proxy_host
        self.port = conf.proxy_port

    def get(self):
        """
        返回代理IP与PORT的组合
        for example: 8.217.112.99:59394
        """
        api_url = "http://{host}:{port}/get".format(host=self.host, port=self.port)
        try:
            proxy = requests.get(api_url).json()['proxy']
            return proxy
        except Exception as e:
            print(e)

    def delete(self, proxy):
        """
        输入需要删除的IP与PORT的组合
        for example: 8.217.112.99:59394
        """
        api_url = "http://{host}:{port}/delete/?proxy={proxy}".format(host=self.host, port=self.port, proxy=proxy)
        try:
            result = requests.get(api_url).json()['code']
            if result:
                print("代理已成功删除！")
            else:
                print("代理不存在！")
        except Exception as e:
            print(e)
