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
    #本地图片存储路径
    image_paths = scrapy.Field()


    def insert_data(self,data):
        """
        1.返回一个sql语句，
        2.返回要插入表的字段
        :param data: 是个字典，就是item里面存放的🈯️
        :return:
        """

        sql = """
        INSERT INTO jobbole (%s)
        VALUES (%s)
        """ % (
            ','.join(data.keys()),
            ','.join(["%s"]*len(data))
        )

        insertData = list(data.values())

        return sql,insertData


class JobboleDetailItem(scrapy.Item):
    title = scrapy.Field()

    def insert_data(self, data):
        """
        1.返回一个sql语句，
        2.返回要插入表的字段
        :param data: 是个字典，就是item里面存放的🈯️
        :return:
        """

        sql = """
        INSERT INTO jobboledetail (%s)
        VALUES (%s)
        """ % (
            ','.join(data.keys()),
            ','.join(["%s"] * len(data))
        )

        insertData = list(data.values())

        return sql, insertData





