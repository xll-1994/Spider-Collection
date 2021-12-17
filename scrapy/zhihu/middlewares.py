# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import random
import re
import time

import requests
from zhihu.util.proxy_pool import ProxyPool

from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy.downloadermiddlewares.downloadtimeout import DownloadTimeoutMiddleware
from twisted.internet.error import TimeoutError

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

proxy_pool = ProxyPool()


class ZhihuSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ZhihuDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class CustomerDownloadTimeoutMiddleware(DownloadTimeoutMiddleware):
    def spider_opened(self, spider):
        self._timeout = getattr(spider, 'download_timeout', 5)

    def process_request(self, request, spider):
        request.meta.setdefault('download_timeout', 5)


class RandomUserAgent(UserAgentMiddleware):

    def __init__(self, user_agent_pool):
        self._user_agent_pool = user_agent_pool

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            user_agent_pool=crawler.settings.get('USER_AGENT_POOL')
        )

    def process_request(self, request, spider):
        user_agent = random.choice(self._user_agent_pool)
        request.headers["User-Agent"] = user_agent


class RandomProxy:
    def process_request(self, request, spider):
        proxy = proxy_pool.get_proxy().get('proxy')
        if proxy:
            time.sleep(0.1)
            request.meta['proxy'] = "http://{}".format(proxy)
            print("\n准备请求的页面URL：{}".format(request.url))
            print("使用的代理为：{}\n".format(proxy))
        else:
            print('爬虫系统没有开启IP代理，请注意爬取速度！')

    def process_exception(self, request, exception, spider):
        temp = request.meta['proxy']
        regex = r'http:\/\/(.*)'
        match = re.findall(regex, temp)
        proxy = match[0]
        result = proxy_pool.delete_proxy(proxy)
        print(result)
        if isinstance(exception, TimeoutError):
            return request
        print("IP Invalid: {}".format(request.meta['proxy']))
        return request
