import time
import random

from zhihu.util.proxy_pool import proxy_pool_url
from scrapy.spiders import Spider
import requests


class TestSpider(Spider):
    name = 'test_spider'
    allowed_domains = ['icanhazip.com']
    start_urls = ['http://icanhazip.com/']
    url = 'http://icanhazip.com/'

    def parse(self, response):
        # 在配置代理的情况下，使用Request向目标网页发起请求
        # 理论上应该返回代理地址
        print(response.text)
        time.sleep(1)

        # 在不配置代理的情况下，使用requests模块向目标网页发起请求
        res = requests.get(
            url=self.url,
            headers={'User-Agent': random.choice(proxy_pool_url)}
        )
        # 理论上应该返回本机地址
        print(res.text)
        time.sleep(1)

        # 获取代理的ip和port
        proxy = requests.get(proxy_pool_url).json()['data']
        ip = proxy[0]['ip']
        port = proxy[0]['port']
        # 在配置代理的情况下，使用requests模块向目标网页发起请求
        res = requests.get(
            url=self.url,
            proxies={"http": "http://{}:{}".format(ip, port)},
            headers={"User-Agent": random.choice(proxy_pool_url)}
        )
        # 理论上应该返回代理地址
        print(res.text)
        return None
