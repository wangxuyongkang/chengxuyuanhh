# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlspiderusedItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ChinazWebItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #封面图
    coverImage = scrapy.Field()
    #标题
    title = scrapy.Field()
    #域
    domains = scrapy.Field()
    #描述
    content = scrapy.Field()
