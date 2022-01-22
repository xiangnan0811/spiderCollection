import json
import random
import requests
from fangtianxia.models import ProxyModel
from fangtianxia.settings import PROXY_URL
from twisted.internet.defer import DeferredLock
from scrapy import signals


class FangtianxiaSpiderMiddleware(object):
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

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
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


class FangtianxiaDownloaderMiddleware(object):
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


class UserAgentDownloadMiddleware:
    """修改UserAgent下载中间件."""
    # 有了scrapy_fake_useragent后，此处意义不大
    USER_AGENTS = []

    def process_request(self, request, spider):
        user_agent = random.choice(self.USER_AGENTS)
        request.headers['User-Agent'] = user_agent
        return request


class IPProxyDownloadMiddleware:
    """设置IP代理下载中间件."""

    def __init__(self):
        super(IPProxyDownloadMiddleware, self).__init__()
        self.current_proxy = None
        self.lock = DeferredLock()

    def process_request(self, request, spider):
        if 'proxy' not in request.meta or self.current_proxy.is_expired:
            # 请求代理
            self.updata_proxy()

        request.meta['proxy'] = self.current_proxy.proxy

    def process_response(self, request, response, spider):
        if response.status != 200 or 'captcha' in response.url:
            if not self.current_proxy.balcked:
                self.current_proxy.balcked = True
            self.updata_proxy()
            # 该请求上一次请求时被禁，所以将之返回，并重新请求一次
            return request
        # 该请求没被禁的话，就将其返回
        return response

    def updata_proxy(self):
        """更新代理."""
        # scrapy底层为twisted异步框架，更新IP代理时设置锁，防止浪费IP代理
        self.lock.acquire()
        if not self.current_proxy or self.current_proxy.is_expired or self.current_proxy.balcked:
            text = requests.get(url=PROXY_URL).text
            result = json.loads(text)
            if result['data']:
                data = result['data'][0]
                proxy_model = ProxyModel(data)
                self.current_proxy = proxy_model

        # 更新IP代理之后释放锁
        self.lock.release()
