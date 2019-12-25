# -*- coding: utf-8 -*-
import scrapy
import re
import random
from tianyan_spider.items import TianyanSpiderItem,TianyanSpider_url
class TianyanSpider(scrapy.Spider):
    name = 'tianyan'
    allowed_domains = ['tianyancha.com']
    start_urls = ['http://tianyancha.com/']

    def parse(self, response):
        html_data = response.xpath('//div[@class="right -scroll js-industry-container"]//a')
        print(len(html_data))
        for info in html_data:
            data = TianyanSpiderItem()
            data['title'] = info.xpath('.//text()').extract_first('')
            data['href'] = info.xpath('.//@href').extract_first('')
            data['only'] = re.findall('.*?=(\w+)',data['href'])
            print(data)
            yield data
            start_url = data['href']
            yield scrapy.Request(url=start_url,callback=self.parse_url)
    def parse_url(self,response):
        html_ls = response.xpath('//div[@class="content"]/div')
        for info in html_ls:
            start_url = TianyanSpider_url()
            start_url['url'] = info.xpath('.//a[@class="name"]/@href').extract_first('')
            print(start_url)
            start_url_response = start_url['url']
            yield scrapy.Request(url=start_url_response,callback='')
    def parse_data(self,response):
        html_div = response.xpath('//div[@class="box -company-box "]/div')
        print(len(html_div))
        for info_s in html_div:
            html_ls = TianyanSpider_url()
            html_ls['views'] = info_s.xpath('.//div[@class="pv"]/span/text()').extract_first('')
            html_ls['title'] = info_s.xpath('.//h1[@class="name"]/text').extract_first('')
            html_ls['phone'] = info_s.xpath('.//span[@class="label"]/text').extract_first('')
            html_ls['email'] = info_s.xpath('.//span[@class="label"]/text').extract_first('')
            html_ls['times'] = info_s.xpath('//span[@class="updatetimeComBox"]/text').extract_first('')
            print(html_ls)


           # yield  数据返回给管道