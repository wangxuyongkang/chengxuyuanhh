# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql

# class QidianPipeline(object):
#
#
#     def __init__(self,host,user,pwd,port,dbname):
#
#         #创建数据库连接
# #         self.mysql_con = pymysql.Connect(
# #             host,user,pwd,
# #             dbname,port=port,charset='utf8'
# #         )
# #         #创建游标
# #         self.cursor = self.mysql_con.cursor()
#
#     @classmethod
#     # def from_crawler(cls,crawler):
#     def from_settings(cls,settings):
#         host = settings['MYSQL_HOST']
#         user = settings['MYSQL_USER']
#         pwd = settings['MYSQL_PWD']
#         port = settings['MYSQL_PORT']
#         dbname = settings['MYSQL_DB']
#
#         return cls(host,user,pwd,port,dbname)
#
#
#     def process_item(self, item, spider):
#         """
#         在这里执行数据的过滤和插入
#         :param item:
#         :param spider:
#         :return:
#         """
#         item_dict = dict(item)
#
#         insertSql,data = item.get_sql_insertdata(item_dict)
#
#         print('222222',insertSql,data)
#
#         try:
#             self.cursor.execute(insertSql,data)
#             self.mysql_con.commit()
#             print('11111,插入成功')
#         except Exception as err:
#             self.mysql_con.rollback()
#             print('11111,插入失败',err)
#
#         return item
#
#     def close_spider(self,spider):
#         #关闭游标和数据库连接
#         self.cursor.close()
#         self.mysql_con.close()


#数据库的异步插入

#adbapi:里面的子线程会去执行数据库的阻塞操作，
#当一个线程执行完毕之后，同时，原始线程能继续
#进行正常的工作，服务其他请求
from twisted.enterprise import adbapi
import json

class QidianPipeline(object):

    def __init__(self,dbpool):
        self.dbpool = dbpool
        self.file = open('insertFaild.json','a')

    @classmethod
    def from_settings(cls,settings):
        """
        MYSQL_HOST = '127.0.0.1'
        MYSQL_USER = 'root'
        MYSQL_PWD = 'ljh1314'
        MYSQL_PORT = 3306
        MYSQL_DB = 'class1808'
        :param settings:
        :return:
        """
        parmas = {
            'host':settings['MYSQL_HOST'],
            'user':settings['MYSQL_USER'],
            'passwd':settings['MYSQL_PWD'],
            'db':settings['MYSQL_DB'],
            'port':settings['MYSQL_PORT'],
            'charset':'utf8',
        }
        #创建连接池
        dbpool = adbapi.ConnectionPool(
            'pymysql',
            **parmas,
        )

        return cls(dbpool)



    def process_item(self, item, spider):
        #往连接池中添加任务
        result = self.dbpool.runInteraction(
           self.insert_data_to_db,
            item
        )
        result.addErrback(
            self.insert_faild,
            item
        )
        return item

    def insert_data_to_db(self,cursor,item):
        """
        实现将数据插入到数据库
        :return:
        """
        dataDict = dict(item)
        sql,data = item.get_sql_insertdata(dataDict)
        #executed
        cursor.execute(sql,data)
        print('插入成功')

    def insert_faild(self,failure,item):
        """
        异步插入失败时会回调这个方法,
        数据插入失败，可以将插入失败的数据，存一份到本地
        方便以后查看
        :param failure:
        :param item:
        :return:
        """
        print(failure,item)
        dataDict = dict(item)
        dataJson = json.dumps(dataDict,ensure_ascii=False)
        self.file.write(dataJson+'\n')

    def close_spider(self,spider):

        self.dbpool.close()
        self.file.close()


