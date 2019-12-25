# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QidianNovalItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 封面
    coverImage = scrapy.Field()
    #标题
    title = scrapy.Field()
    #作者
    author = scrapy.Field()
    #分类
    category = scrapy.Field()
    #状态
    status = scrapy.Field()
    #简介
    content = scrapy.Field()

    def get_sql_insertdata(self,dataDict):
        sql, data = get_sql_info('qdnoval',dataDict)
        return sql, data



class QidianChpaterItem(scrapy.Item):
    # 章节名称
    chpaterName = scrapy.Field()
    # 书籍名称
    novalName = scrapy.Field()
    # 内容
    content = scrapy.Field()
    # 作者
    author = scrapy.Field()
    # 字数
    sizeNum = scrapy.Field()
    # 发布时间
    publishTime = scrapy.Field()


    def get_sql_insertdata(self, dataDict):

        sql,data = get_sql_info('qdchpater', dataDict)

        return sql,data



def get_sql_info(tablename,dataDict):

    """
    dataDict:是一个字典，里面存放着要出入的数据
    返回sql语句和要插入表的数据
    :param dataDict:
    :return:
    """
    insertSql = """
            INSERT INTO %s (%s)
            VALUES (%s)
            """ % (
        tablename,
        ','.join(dataDict.keys()),
        ','.join(['%s'] * len(dataDict))
    )

    data = list(dataDict.values())

    return insertSql, data
