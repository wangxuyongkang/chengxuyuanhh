# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals


class DemoSpiderMiddleware(object):
    #爬虫中间件
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


class DemoDownloaderMiddleware(object):
    ##下载中间件
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
        #拦截Request对象
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
            #继续执行其他下载中间件的process_request方法处理Request对像
        # - or return a Response object
            #返回Response对象，其他下载中间件的process_request方法不再执行，
            #会执行process_response方法
        # - or return a Request object
            #如果返回的是Request对像, 这个Request对像会重新交给调度器，等待下一次被调度
        # - or raise IgnoreRequest: process_exception() methods of
            #异常处理，执行process_exception
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        """拦截Response请求的响应结果"""
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        """请求异常的情况，会执行之歌方法"""
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

#自定义一个User-Agnet的下载中间件
import random
class CustomUADownloadMiddlerWare(object):

    def process_request(self, request, spider):
        #获取settings.py文件中的USER_AGENTS
        USER_AGENTS = spider.settings['USER_AGENTS']
        random_ua = random.choice(USER_AGENTS)
        if random_ua:
            print('执行了下载中间件')
            request.headers['User-Agent'] = random_ua
            # request.headers.setdefault(
            # b'User-Agent', random_ua
            # )


import random
import base64

#定义一个代理的中间件
import base64
class RandomProxyMiddleware(object):

    def process_request(self, request, spider):

        proxies = spider.settings['PROXIES']
        #随机获取一个代理
        proxy = random.choice(proxies)
        if proxy['user_pwd'] is None:
            # 没有代理账户验证的代理使用方式
            request.meta['proxy'] = proxy['ip_port']
        else:
            #对账户密码进行base64编码
            user_pwd = base64.b64encode(proxy['user_pwd'].encode('utf-8')).decode('utf-8')
            #对应到代理服务器的信令格式里
            request.headers['Proxy-Authorization'] = 'Basic ' + user_pwd
            request.meta['proxy'] = proxy['ip_port']

import random
class RandomCookiesMiddleware(object):

    def process_request(self, request, spider):
        cookies = spider.settings['COOKIES']
        # 随机获取一个cookies
        cookie = random.choice(cookies)
        if cookie:
            cookies_dict= {cookie.split('=')[0]:cookie.split('=')[1] for cookie in cookie.split('; ')}
            request.cookies = cookies_dict


#selenium下载中间件
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from scrapy.http import HtmlResponse

class SeleniumMiddleware(object):

    def __init__(self):
        self.drive = webdriver.Chrome(executable_path='/Users/ljh/Desktop/driver/chromedriver')
        self.drive.set_page_load_timeout(10)

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        #监控爬虫结束的信号量spider_closed，执行spider_closed（自己定义的方法）
        crawler.signals.connect(s.spider_close, signal=signals.spider_closed)
        return s

    def process_request(self,request,spider):
        try:
            url = request.url
            self.drive.get(url)
            if self.drive.page_source:
                return HtmlResponse(url=url,body=self.drive.page_source.encode('utf-8'),status=200,encoding='utf-8',request=request)
        except TimeoutException:
            print('请求超时')
            return HtmlResponse(url=url,body=None,status=500)

    def spider_close(self, spider):
        print('爬虫结束')
        self.drive.quit()