# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DemoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #小说名称
    name = scrapy.Field()
    #点击量
    point_nums = scrapy.Field()
    #category分类
    category = scrapy.Field()
    #字数
    size = scrapy.Field()
    #其他
    other = scrapy.Field()
    #简介
    content = scrapy.Field()
    #tags
    tags = scrapy.Field()
    #url
    url = scrapy.Field()
    #书籍图片
    book_image = scrapy.Field()
    #本地图片存储地址
    local_image_path = scrapy.Field()

    def get_sql_str(self,data):

        sql = """
        INSERT INTO book (%s)
        VALUES (%s)
        """ % (
            ','.join(data.keys()),
            ','.join(['%s']*len(data))
        )

        return sql

