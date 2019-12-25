# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Response

class JobboleSpider(scrapy.Spider):
    #爬虫文件的名称
    name = 'jobbole'
    #设置爬虫允许爬取的域，可以设置多个 （是一个list）
    allowed_domains = ['jobbole.com']
    #设置起始的url地址，可以设置多个（是一个list）
    start_urls = ['http://blog.jobbole.com/all-posts/']

    #parse,获取响应结果的回调方法
    def parse(self, response):
        """
        :param response: 请求的响应结果
        :return:
        """
        print('请求成功，获取到了页面源码')
        #获取响应的状态码
        code = response.status
        #获取响应的二进制数据
        b_html = response.body
        #获取响应的页面源码
        html = response.text
        #获取当前请求的url地址
        url = response.url
        #获取响应头
        response_headers = response.headers
        #获取当前请求的request对想
        request = response.request
        #获请求的请求头
        request_headers = response.request.headers

        print(code,url)

