import scrapy

class SpiderUsedSpider(scrapy.Spider):
    name = 'spdier_used'
    allowed_domains = ['baidu.com']
    start_urls = ['http://baidu.com/']

    #