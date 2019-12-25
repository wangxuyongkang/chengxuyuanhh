# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals


class CrawlspiderusedSpiderMiddleware(object):
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

        # Should return either None or an iterable of Response, dict
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


class CrawlspiderusedDownloaderMiddleware(object):
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
from fake_useragent import UserAgent
import random
class RandomUserAgentMiddlewareTwo(object):

    def process_request(self,request,spider):
        useragents = spider.settings['USERA_GENTS']

        # 随机获取一个User-Agent
        user_agent = random.choice(useragents)
        print('执行下载中间件' + user_agent)

        if user_agent:
            # 赋值的两种方式
            request.headers.setdefault(b'User-Agent', user_agent)
        # request.headers['User-Agent'] = user_agent
#代理的下载中间件
import base64
class ProxyDownloadMiddler(object):
    def process_request(self,request,spider):
        proxies = spider.settings['PROXIES']
        randomProxy = random.choice(proxies)
        if randomProxy:
            if randomProxy['user_pwd']:
                #注意:如果使用的私密代理:1.将账号密码经过base64编码
                print('当前代理需要账号密码信息')
                base64_pwd = base64.b64encode(randomProxy['user_pwd'].encode('utf-8')).decode('utf-8')
                request.headers['Proxy-Authorization'] = b'Basic ' + base64_pwd
                request.meta['proxy'] = randomProxy['ip_port']
            else:
                print('当前是公开代理')
                request.meta['proxy'] = randomProxy['ip_port']

class CookiesDownloadMiddlerWare(object):
    def process_request(self,request,spider):
        cookies_list = spider.settings['COOKIES']
        randomCookies = random.choice(cookies_list)
        if randomCookies:
            cookies_dict = {
                cookie_str.split('=')[0] : cookie_str.split('=')[1] for cookie_str in randomCookies.split('; ')
            }
            request.cookies = cookies_dict
#遇到动态加载的数据,不能通过请求直接获取的数据
#这是我们需要在下载中间件中做拦截，使用selenium
#进行请求

class SeleniumDownloadMiddlerware(object):
    def __init__(self):
        #创建浏览器驱动
        self.brower = webdriver.Chrome
    def process_request(self,request,spider):
        pass