# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QidianNovalItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #封面图片
    coverImage = scrapy.Field()
    #小说名称
    novalTitle = scrapy.Field()
    #作者
    author = scrapy.Field()
    #分类
    category = scrapy.Field()
    #连载状态
    status = scrapy.Field()
    #简介
    content = scrapy.Field()

    def get_collection_name(self):

        return 'novals'

class QidianChpaterItem(scrapy.Item):
    #小说的标题
    novalTitle = scrapy.Field()
    #章节的标题
    chpaterTitle = scrapy.Field()
    #章节的字数
    chpaterSize = scrapy.Field()
    #章节的内容
    chpaterContent = scrapy.Field()
    #发布时间
    publishTime = scrapy.Field()

    def get_collection_name(self):

        return 'chpaters'