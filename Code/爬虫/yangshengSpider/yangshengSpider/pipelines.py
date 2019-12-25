# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
# import pymongo
class YangshengspiderPipeline(object):
    def __init__(self,host,user,pwd,port,dbname):
        #创建数据库连接
        self.mysql_con = pymysql.Connect(
            host,user,pwd,dbname,port=port,charset='utf8'
        )
        #创建游标
        self.cursor = self.mysql_con.cursor()
    @classmethod
    def from_settings(cls,settings):
        host = settings['MYSQL_HOST']
        user = settings['MYSQL_USER']
        pwd  = settings['MYSQL_PWD']
        port = settings['MYSQL_PORT']
        dbname = settings['MYSQL_DB']

        return cls(host,user,pwd,port,dbname)

    def process_item(self, item, spider):
        item_dict = dict(item)
        sql,data = item.get_sql_insertdata(item_dict)
        print('***********',sql,data)
        try:
            self.cursor.execute(sql,data)
            self.mysql_con.commit()
            print('66666666666666666666插入成功')
        except Exception as err:
            self.mysql_con.rollback()
            print('%%%%%%%%%,插入失败',err)
        return item
    def close_spider(self,spider):
        self.cursor.close()
        self.mysql_con.close()


# class YangshengspiderPipeline_mongodb(object):
#     def __init__(self,host,port,dbname):
#         #创建mongodb的数据库连接
#         self.mongoClient = pymongo.MongoClient(host,port)
#         #获取到数据库
#         self.db = self.mongoClient[dbname]
#
#     @classmethod
#     def from_crawler(cls,crawler):
#         host = crawler.settings['MONGO_HOST']
#         port = crawler.settings['MONGO_PORT']
#         dbname = crawler.settings['MONGO_DB']
#
#         return cls(host,port,dbname)

    # def process_item(self, item, spider):
    #
    #     #数据的存储
    #     col_name = item.get_collection_name()
    #
    #     print('集合名称：',col_name)
    #
    #     try:
    #         self.db[col_name].insert(dict(item))
    #         print('插入成功')
    #     except Exception as err:
    #         print(err,'插入失败')
    #
    #     return item

    def close_spider(self,spider):

        self.mongoClient.close()
