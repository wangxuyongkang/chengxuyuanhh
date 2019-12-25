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
    status_a = scrapy.Field()
    #简介
    content = scrapy.Field()


    def mysql_db(self,dataDict):
        sql, data = get_sql_info('qidian', dataDict)
        return sql, data




class qidianItem(scrapy.Item):
    #标题
    title = scrapy.Field()
    #作者
    author = scrapy.Field()
    #内容
    context = scrapy.Field()
    def mysql_db(self,dataDict):
        sql, data = get_sql_info('qidian_data', dataDict)

        return sql, data

        #return sql,insertData
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