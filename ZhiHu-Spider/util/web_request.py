# -*- coding: utf-8 -*-
# ProjectName:  ZhiHu-Spider
# FileName:     web_request
# Description:  
# CreateDate:   2021/12/25

import time
import random
import re

import requests
from lxml import etree

from util import USER_AGENT_POOL
from util import COOKIES_POOL
from handler import ProxyHandler
from handler import ConfigHandler


class WebRequest(object):

    def __init__(self):
        self.conf = ConfigHandler()
        self.response = requests.Response

    def get(self, url, proxy=None, cookie=None, *args, **kwargs):
        api_proxy = ''
        while True:
            try:
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
                    ProxyHandler().delete(api_proxy)
                    time.sleep(0.5)
                    self.get(url)
            except Exception as e:
                ProxyHandler().delete(api_proxy)
                print(e)
                time.sleep(0.5)

    @property
    def user_agent(self):
        return random.choice(USER_AGENT_POOL)

    @property
    def cookies(self):
        return random.choice(COOKIES_POOL)

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
        return ProxyHandler().get()

    @staticmethod
    def set_proxies(proxy):
        return {
            'http': 'http://{proxy}'.format(proxy=proxy),
            'https': 'https://{proxy}'.format(proxy=proxy)
        }

    @property
    def set_cookies(self):
        cookies = self.response.headers['set-cookie']
        regex = r'KLBRSID=([^;]+);'
        value = re.findall(regex, cookies)[0]
        return {
            'KLBRSID': value
        }

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
