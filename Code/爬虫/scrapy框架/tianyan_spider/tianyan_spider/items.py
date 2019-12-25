# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TianyanSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()

    href = scrapy.Field()

    #唯一
    only = scrapy.Field()


class TianyanSpider_url(scrapy.Item):

    url = scrapy.Field()

    title = scrapy.Field()

    phone = scrapy.Field()

    email = scrapy.Field()

    views = scrapy.Field()

    tiems = scrapy.Field()
#表单数据的结构
# class Table_data(scrapy.Item):
#
#     man = scrapy.Field()
#     capital =scrapy.Field()
#     date = scrapy.Field()
