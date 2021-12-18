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
from scrapy.downloadermiddlewares.retry import RetryMiddleware
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
        self._timeout = getattr(spider, 'download_timeout', 3)

    def process_request(self, request, spider):
        request.meta.setdefault('download_timeout', 3)


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
        regex = 'https:\/\/www.zhihu.com\/account\/(.*)'
        match = re.findall(regex, request.url)
        if match:
            temp = request.meta['proxy']
            regex = r'http:\/\/(.*)'
            match = re.findall(regex, temp)
            proxy = match[0]
            result = proxy_pool.delete_proxy(proxy)
            print(result)
            temp_url = request.meta['redirect_urls'][0]
            request._set_url(temp_url)
        proxy = proxy_pool.get_proxy().get('proxy')
        if proxy:
            time.sleep(0.2)
            request.meta['proxy'] = "http://{}".format(proxy)
            url = request.url
            print("\n准备使用 {proxy} 连接 {url}\n".format(proxy=proxy, url=url))
        else:
            print('爬虫系统没有开启IP代理，请注意爬取速度！')

    def process_exception(self, request, exception, spider):
        temp = request.meta['proxy']
        regex = r'http:\/\/(.*)'
        match = re.findall(regex, temp)
        proxy = match[0]
        url = request.url
        if isinstance(exception, TimeoutError):
            print("\n代理 {proxy} 连接 {url} 超时，准备删除代理后重试\n".format(proxy=proxy, url=url))
            result = proxy_pool.delete_proxy(proxy)
            print(result)
            print("正在重新匹配代理并连接 {url}".format(url=url))
            return request
        print("\n代理 {proxy} 连接 {url} 出错，准备删除代理后重试".format(proxy=proxy, url=url))
        print(exception)
        result = proxy_pool.delete_proxy(proxy)
        print("\n")
        print(result)
        print("正在重新匹配代理并连接 {url}\n".format(url=url))
        return request
