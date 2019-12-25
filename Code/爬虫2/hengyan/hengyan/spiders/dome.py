# -*- coding: utf-8 -*-
import scrapy


class DomeSpider(scrapy.Spider):
    name = 'dome'
    allowed_domains = ['http://all.hengyan.com/']
    start_urls = ['http://http://all.hengyan.com//']

    def parse(self, response):
        pass
