# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
class QidianPipeline(object):

    def __init__(self,host,user,pwd,port,dbname):
        self.mysql_client = pymysql.Connect(
            host,user,pwd,
            dbname,
            port=port,charset='utf8'
        )
        #创建游标
        self.cursor = self.mysql_client.cursor()


    @classmethod
    #def from_crawler(cls,crawler):
    def from_settings(cls,settings):
        host = settings['MYSQL_HOST']
        user = settings['MYSQL_USER']
        pwd = settings['MYSQL_PWD']
        port = settings['MYSQL_PORT']
        dbname =settings['MYSQL_DB']

        return cls(host,user,pwd,port,dbname)

    def process_item(self, item, spider):

        """
        在这里执行数据的过滤和插入
        :param item:
        :param spider:
        :return:
        """
        item_dict = dict(item)

        insertSql,data = item.mysql_db(item_dict)

        print('222222',insertSql,data)

        try:
            self.cursor.execute(insertSql,data)
            self.mysql_client.commit()
            print('11111,插入成功')
        except Exception as err:
            self.mysql_client.rollback()
            print('11111,插入失败',err)

        return item

    def close_spider(self,spider):
        #关闭游标和数据库连接
        self.cursor.close()
        self.mysql_client.close()

# from twisted.enterprise import adbapi
# import json
# class QidianPipeline(object):
#
#     def __init__(self,dbpool):
#         self.dbpool = dbpool
#         self.file = open('insertFaild.json','a')
#
#     #数据库的异步插入
#     @classmethod
#     def from_settings(cls,settings):
#         #
#         # MYSQL_HOST = '127.0.0.1'
#         # MYSQL_USER = 'root'
#         # MYSQL_PWD = '123456'
#         # MYSQL_PORT = 3306
#         # MYSQL_DB = 'class1808'
#         parmas = {
#             'host' : settings['MYSQL_HOST'],
#             'user' : settings['MYSQL_USER'],
#             'pwd' :settings['MYSQL_PWD'],
#             'port' : settings['MYSQL_PORT'],
#             'dbname' :settings['MYSQL_DB'],
#             'charset':'utf8',
#         }
#         #创建池子
#         dbpool = adbapi.ConnectionPool(
#             'pymysql',
#             **parmas,
#          )
#
#         return cls(dbpool)
#     def process_item(self, item, spider):
#         #往池子中添加任务
#         result = self.dbpool.runInteraction(
#             self.insert_data_to_db,
#             item
#         )
#         result.addErrback(
#             self.insert_faild,
#             item
#         )
#         return item
#
#     def insert_data_to_db(self,cursor,item):
#         # 将数据插入到数据库
#         dataDict  = dict(item)
#         sql,data = item.get_sql_info(dataDict)
#         cursor.execute(sql,data)
#         print('插入成功')
#
#     def insert_faild(self,failure,itme):
#         #一部插入失败回调这个方法
#         #数据插入失败，可以将失败的数据，存一份写到本地
#         print(failure,itme)
#         dataDict = dict(itme)
#         dataJson = json.dumps(dataDict,ensure_ascii=False)
#         self.file.write(dataJson+'\n')
#     def close_spider(self,spider):
#         self.dbpool.close()
#         self.file.close()
#
