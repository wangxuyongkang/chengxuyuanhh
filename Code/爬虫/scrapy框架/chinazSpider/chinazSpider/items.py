# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ChinazspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    coverImage = scrapy.Field()
    title = scrapy.Field()
    domains = scrapy.Field()
    context = scrapy.Field()
    score = scrapy.Field()

    def get_sql_insertdata(self,dataDict):

        sql,data = get_sql_info('china',dataDict)
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
