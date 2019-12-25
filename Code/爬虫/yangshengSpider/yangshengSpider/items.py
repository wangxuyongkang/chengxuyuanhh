# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YangshengspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #图片
    coverImage = scrapy.Field()
    #标题
    title = scrapy.Field()
    #文本
    context = scrapy.Field()
    #时间
    time_data = scrapy.Field()
    def get_sql_insertdata(self,dataDict):
        sql,data = get_sql_info('yangshen',dataDict)

        return sql,data



class YangshengspiderItem_data(scrapy.Item):
    #标题
    title = scrapy.Field()
    #来源
    source = scrapy.Field()
    #作者
    author = scrapy.Field()
    #内容
    context = scrapy.Field()

    def get_sql_insertdata(self,dataDict):
        sql,data = get_sql_info('yangshen_data',dataDict)

        return sql,data

# class YangshengSpidermongo_data(scrapy.Item):
#     # 热评
#     buzz = scrapy.Field()
#     # 频道
#     channel = scrapy.Field()
#     # 热搜
#     Hotsearch = scrapy.Field()
#     # 食谱
#     Therecipe = scrapy.Field()
#     # 食库
#     Foodlibrary = scrapy.Field()
#     # 食材营养
#     Foodnutrition = scrapy.Field()
#     # 食材做法
#     practice = scrapy.Field()
#     # 百科
#     encyclopedia = scrapy.Field()
#     # 养生
#     Keeping = scrapy.Field()
#     # 焦点关注
#     focus = scrapy.Field()
#     # 都爱看
#     Lovetosee = scrapy.Field()
#     def get_collection_name(self):
#
#         return 'redian'

def get_sql_info(tablename,dataDict):
    insertSql = """
    INSERT INTO %s (%s)
    VALUES (%s)
    """%(
        tablename,
        ','.join(dataDict.keys()),
        ','.join(['%s']*len(dataDict))
    )
    data = list(dataDict.values())

    return insertSql,data










