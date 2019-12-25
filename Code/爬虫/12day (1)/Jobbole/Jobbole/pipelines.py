# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json

import scrapy
# from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.pipelines.images import ImagesPipeline
#DropItem 丢弃item
from scrapy.exceptions import DropItem
from scrapy.utils.project import get_project_settings
import os
# os.rename(源文件的名称,新的名称)

#获取图片存储的文件夹路径
image_store = get_project_settings().get('IMAGES_STORE')

#图片下载管道文件
class MyImagesPipeline(ImagesPipeline):

    # def file_path(self, request, response=None, info=None):
    #     # 可以返回一个图片的路径
    #     #return 'full/%s.jpg' % (image_guid)
    #     return 'full/%s.jpg' % (图片的名称)

    def get_media_requests(self, item, info):
        # 第一步从item中获取要下载的图片地址
        # for image_url in item['image_urls']:
        #     #根据图片的 url地址构建一个Request对象，
        #     #最终交给调度器
        #     yield scrapy.Request(image_url)
        yield scrapy.Request(item['coverImage'])

    def item_completed(self, results, item, info):
        #图片请求完毕后会有一个回调结果， item_completed就是
        #我们的回调函数，results
        image_paths = [x['path'] for status, x in results if status]
        if not image_paths:
            #丢弃item
            raise DropItem("Item contains no images")
        else:
            #修改图片的文件名称
            new_image_paths = []
            for img_path in image_paths:
                os.rename(image_store + '/' + img_path, image_store + '/' + 'full/' + item['title'] + '.jpg')
                new_image_paths.append(image_store + '/' + 'full/' + item['title'] + '.jpg')
        #将获取到的图片存储路径赋值给 item
        print('66666666666666',new_image_paths)
        item['image_paths'] = ','.join(new_image_paths)
        return item


#管道文件，过滤数据和持久化
# class JobbolePipeline(object):
#
#     def __init__(self):
#
#         self.file = open('jobbole.json','a+')
#
#     def process_item(self, item, spider):
#         """
#         :param item: item：这个就是爬虫文件中yield 过来的item (是一个对象)
#         :param spider: 是一个对象，爬虫文件实例化的对象（JobboleSpider）
#         :return:
#         """
#         #这个方法是必须要实现的，
#         print('1111经过了管道')
#         #先将item转为字典
#         data = dict(item)
#         json_data = json.dumps(data,ensure_ascii=False)
#         self.file.write(json_data + '\n')
#
#         #注意假如有多个管道，只有return item 之后，
#         #下一个管道才能接收到item
#         return item
#
#     def open_spider(self,spider):
#         """
#         并不是必须要实现的方法，在爬虫运行的时候，执行一次
#         :param spider:
#         :return:
#         """
#         print('爬虫开始运行')
#
#     def close_spider(self,spider):
#         """
#         并不是必须要实现的方法，在爬虫结束的时候，执行一次
#         :param spider:
#         :return:
#         """
#         self.file.close()

import pymysql
from Jobbole.items import JobboleItem,JobboleDetailItem

# class JobbolePipelineDb(object):
#
#     def __init__(self,host,user,pwd,db,port):
#         #创建数据库连接
#         self.mysql_client = pymysql.Connect(
#             host,user,pwd,
#             db,port=port,charset='utf8'
#         )
#         #创建游标（执行sql语句）
#         self.cursor = self.mysql_client.cursor()
#
#
#     @classmethod
#     def from_settings(cls,settings):
#         # cls 可以理解为当前的类型的名称
#         #host
#         host = settings['MYSQL_HOST']
#         user = settings['MYSQL_USER']
#         pwd = settings['MYSQL_PWD']
#         db = settings['MYSQL_DB']
#         port = settings['MYSQL_PORT']
#
#         #cls(host,user,pwd,db,port)实例化当前类
#         return cls(host,user,pwd,db,port)
#
#     # def __init__(self):
#     #
#     #     #创建数据库连接
#     #     self.mysql_client = pymysql.Connect(
#     #         '127.0.0.1','root','ljh1314',
#     #         'class1808',port=3306,charset='utf8'
#     #     )
#     #     #创建游标（执行sql语句）
#     #     self.cursor = self.mysql_client.cursor()
#     #
#
#     def process_item(self, item, spider):
#         print('2222经过了管道')
#         data_dict = dict(item)
#
#         # sql_insert = """
#         #         INSERT INTO jobbole (%s)
#         #         VALUES (%s)
#         #         """ % (
#         #     ','.join(data_dict.keys()),
#         #     ','.join(['%s'] * len(data_dict))
#         # )
#
#         tablename = ''
#
#         if isinstance(item,JobboleItem):
#             tablename = 'jobbole'
#
#         elif isinstance(item,JobboleDetailItem):
#             tablename = 'jobboledetail'
#
#
#         sql_insert = """
#         INSERT INTO %s (%s)
#         VALUES (%s)
#         """ % (
#             tablename,
#             ','.join(data_dict.keys()),
#             ','.join(['%s'] * len(data_dict))
#         )
#
#
#         try:
#             self.cursor.execute(sql_insert,list(data_dict.values()))
#             self.mysql_client.commit()
#         except Exception as err:
#             self.mysql_client.rollback()
#             print(err)
#
#         return item
#
#     def close_spider(self,spider):
#         #爬虫结束后，关闭数据库连接和游标
#         self.cursor.close()
#         self.mysql_client.close()


#优化（解藕）
class JobbolePipelineDb(object):

    def __init__(self, host, user, pwd, db, port):
        # 创建数据库连接
        self.mysql_client = pymysql.Connect(
            host, user, pwd,
            db, port=port, charset='utf8'
        )
        # 创建游标（执行sql语句）
        self.cursor = self.mysql_client.cursor()

    @classmethod
    def from_settings(cls, settings):
        # cls 可以理解为当前的类型的名称
        # host
        host = settings['MYSQL_HOST']
        user = settings['MYSQL_USER']
        pwd = settings['MYSQL_PWD']
        db = settings['MYSQL_DB']
        port = settings['MYSQL_PORT']

        # cls(host,user,pwd,db,port)实例化当前类
        return cls(host, user, pwd, db, port)

    def process_item(self, item, spider):
        print('2222经过了管道')
        data_dict = dict(item)

        sql, insertData = item.insert_data(data_dict)

        try:
            self.cursor.execute(sql,insertData)
            self.mysql_client.commit()

        except Exception as err:
            self.mysql_client.rollback()
            print(err)

        return item

    def close_spider(self, spider):
        # 爬虫结束后，关闭数据库连接和游标
        self.cursor.close()
        self.mysql_client.close()

# import pymongo
# class JobbolePipelineMongodb(object):
#
#     def __init__(self):
#         #创建数据库连接
#         self.mongo_client = pymongo.MongoClient(
#             '127.0.0.1',27017,
#         )
#         #获取要操作数据
#         db = self.mongo_client['class1808']
#         #获取要操作的集合
#         self.col = db['jobbole']
#
#     def process_item(self, item, spider):
#
#         data_dict = dict(item)
#         try:
#             result = self.col.insert(data_dict)
#             print(result)
#         except Exception as err:
#             print(err)
#
#         return item
#
#     def close_spider(self,spider):
#
#         self.mongo_client.close()
#
