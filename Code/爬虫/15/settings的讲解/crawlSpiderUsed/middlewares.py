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
        #return None :如果返回None，继续处理这个request请求，（
        # 如果有其他的下载中间件，则继续处理请求）
        # - return None: continue processing this request
        #return a Response object:其他的process_request方法就不再执行了，
        # 就会调用process_response方法处理请求的响应结果
        # - or return a Response object
        #return a Request object:其他的process_request方法就不再执行了,
        #Request将作为一个新的请求交给下载器，等待下一次被调度
        # - or return a Request object
        #raise IgnoreRequest:如果出现了异常，则process_exception会被调用，
        #如果没有捕获这个异常，则Request的errback回调将会被调用，处理这个异常，
        #如果两个都没有捕获异常（处理异常），这个异常就会被忽略
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object:更低级别的下载中间件，
        # 将继续处理这个响应结果
        # - return a Request object：更低级别的下载中间件，
        # 不会在执行process_response，Request将会作为一个
        # 新的请求交给调度器等待调度
        # - or raise IgnoreRequest：如果请求出现了异常我们会回调
        #errback设置的回调函数处理，如果没有设置回调函数处理，则忽略且不
        # 记录这个异常
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

import random
#from fake_useragent import UserAgent

class UserAgentDownloadMiddler(object):

    def __init__(self):
        # self.userAgent = UserAgent()
        pass

    def process_request(self,request,spider):
        #从setting获取一个USERAGENTS列表（USERAGENTS池）
        userAgents = spider.settings['USERAGENTS']
        #随机获取一个User-Agent
        randomUa = random.choice(userAgents)

        # print('设置了随机的Useragent:',randomUa)
        print('设置了随机的Useragent:')

        # #随机获取一个User-Agent
        # randomUa = random.choice(userAgents)
        # randomUa = self.userAgent.random

        if randomUa:
            #两种方式
            request.headers['User-Agent'] = randomUa
            request.headers.setdefault(b'User-Agent',randomUa)
            # request.headers.setdefault(b'User-Agent', self.user_agent)


#代理的下载中间件
import base64

class ProxyDownloadMiddler(object):

    def process_request(self,request,spider):

        proxies = spider.settings['PROXIES']

        randomProxy = random.choice(proxies)

        if randomProxy:
            if randomProxy['user_pwd']:
                print('当前代理需要账号密码信息')
                #注意：如果使用的是私密代理
                # 1.将账号密码经过base64编码，
                base64_pwd = base64.b64encode(randomProxy['user_pwd'].encode('utf-8')).decode('utf-8')
                #request.headers['']
                #2设置信令
                request.headers['Proxy-Authorization'] = 'Basic ' + base64_pwd
                request.meta['proxy'] = randomProxy['ip_port']

            else:
                print('当前代理是公开代理')
                request.meta['proxy'] = randomProxy['ip_port']


# cookies 下载中间件
class CooikesDownloadMiddlerWare(object):

    def process_request(self,request,spider):

        #获取cookies
        cookies_list = spider.settings['COOKIES']
        randomCookies = random.choice(cookies_list)

        if randomCookies:
            cookies_dict = {
                cookie_str.split('=')[0]:cookie_str.split('=')[1]
                for cookie_str in randomCookies.split('; ')
            }
            #将cookies_dict 信息赋值给request.cookies参数
            request.cookies = cookies_dict

#遇到js动态加载的数据,不能通过请求直接获取的数据
#这是我们需要在 下载中间件中的做拦截，使用的selenium
#进行请求

from selenium import webdriver

from scrapy.http import HtmlResponse

class SeleniumDownloadMiddlerware(object):

    def __init__(self):
        # 创建浏览器驱动
        self.brower = webdriver.Chrome(
            executable_path='/Users/ljh/Desktop/1808爬虫/chromedriver'
        )
        self.brower.set_page_load_timeout(10)

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        # 监控信号，当爬虫结束的时候调用spider_closed方法
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s

    def process_request(self,request,spider):
        # 所有的请求都会经过这个方法

        url = request.url
        try:
            self.brower.get(url)
            if self.brower.page_source:
                response = HtmlResponse(
                    url,
                    status=200,
                    body=self.brower.page_source.encode('utf-8'),
                    request=request
                )

                return response

        except Exception as err:
            print('请求失败')
            response = HtmlResponse(
                url,
                status=404,
                body=b'',
                request=request
            )

            return response

    def spider_closed(self, spider):

        self.brower.quit()



