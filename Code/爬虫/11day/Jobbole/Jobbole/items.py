# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

#在这里定义想要获取的字段（类似model的作用）
class JobboleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #title(标题)
    title = scrapy.Field()
    #source（来源）
    source = scrapy.Field()
    #内容
    content = scrapy.Field()
    #点赞量
    zanNum = scrapy.Field()
    #评论量
    commentNum = scrapy.Field()
    #收藏
    markNum = scrapy.Field()
    #封面图
    coverImage = scrapy.Field()
    #发布时间
    publishTime = scrapy.Field()

