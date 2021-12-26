# -*- coding: utf-8 -*-
# ProjectName:  ZhiHu-Spider
# FileName:     web_request
# Description:  
# CreateDate:   2021/12/25

import time
import random

import requests
from lxml import etree

from util import USER_AGENT_POOL
from handler import ProxyHandler
from handler import ConfigHandler
from handler import LogHandler


class WebRequest(object):

    def __init__(self):
        self.conf = ConfigHandler()
        self.response = requests.Response
        self.log = LogHandler('web_request')

    def get(self, url, proxy=None, cookie=None, *args, **kwargs):
        api_proxy = None
        while True:
            try:
                time.sleep(self.conf.interval_time)
                if isinstance(cookie, dict):
                    cookies = cookie
                else:
                    cookies = self.cookies
                if proxy:
                    proxies = self.set_proxies(proxy)
                else:
                    api_proxy = self.proxy
                    proxies = self.set_proxies(api_proxy)
                self.response = requests.get(url=url, headers=self.headers, proxies=proxies, cookies=cookies,
                                             timeout=self.conf.timeout,
                                             allow_redirects=False,
                                             *args,
                                             **kwargs)
                if self.response.status_code == 200:
                    return self
                else:
                    self.log.warning('访问 {} 失败，返回 {} 提示，正在重新连接！'.format(url, self.response.status_code))
                    if api_proxy:
                        ProxyHandler().delete(api_proxy)
                    self.get(url)
            except Exception:
                self.log.warning('访问 {} 发生未知错误，正在重新连接！'.format(url))
                if api_proxy:
                    ProxyHandler().delete(api_proxy)

    @property
    def user_agent(self):
        return random.choice(USER_AGENT_POOL)

    @property
    def cookies(self):
        my_time = int(time.time())
        str_list = []
        for i in range(32):
            temp = str(hex(random.randint(0, 15)))[2:]
            str_list.append(temp)
        str_value = ''.join(str_list)
        return {
            'KLBRSID': '{}|{}|{}'.format(str_value, my_time, my_time)
        }

    @property
    def headers(self):
        return {
            'User-Agent': self.user_agent,
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'Accept-Language': 'zh-CN,zh;q=0.8'
        }

    @property
    def proxy(self):
        if self.conf.use_proxy == 1:
            return ProxyHandler().get()
        else:
            return None

    @staticmethod
    def set_proxies(proxy):
        if proxy:
            return {
                'http': 'http://{proxy}'.format(proxy=proxy),
                'https': 'https://{proxy}'.format(proxy=proxy)
            }
        else:
            return None

    @property
    def text(self):
        return self.response.text

    @property
    def tree(self):
        return etree.HTML(self.response.content)

    @property
    def json(self):
        return self.response.json()


if __name__ == '__main__':
    pass
