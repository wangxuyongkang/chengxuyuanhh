# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json

#管道文件，过滤数据和持久化
class JobbolePipeline(object):

    def __init__(self):

        self.file = open('jobbole.json','a+')

    def process_item(self, item, spider):
        """
        :param item: item：这个就是爬虫文件中yield 过来的item (是一个对象)
        :param spider: 是一个对象，爬虫文件实例化的对象（JobboleSpider）
        :return:
        """
        #这个方法是必须要实现的，
        print('1111经过了管道')
        #先将item转为字典
        data = dict(item)
        json_data = json.dumps(data,ensure_ascii=False)
        self.file.write(json_data + '\n')

        #注意假如有多个管道，只有return item 之后，
        #下一个管道才能接收到item
        return item

    def open_spider(self,spider):
        """
        并不是必须要实现的方法，在爬虫运行的时候，执行一次
        :param spider:
        :return:
        """
        print('爬虫开始运行')

    def close_spider(self,spider):
        """
        并不是必须要实现的方法，在爬虫结束的时候，执行一次
        :param spider:
        :return:
        """
        self.file.close()

import pymysql

class JobbolePipelineDb(object):

    def __init__(self):

        #创建数据库连接
        self.mysql_client = pymysql.Connect(
            '127.0.0.1','root','ljh1314',
            'class1808',port=3306,charset='utf8'
        )
        #创建游标（执行sql语句）
        self.cursor = self.mysql_client.cursor()


    def process_item(self, item, spider):
        print('2222经过了管道')
        data_dict = dict(item)

        sql_insert = """
        INSERT INTO jobbole (%s)
        VALUES (%s)
        """ % (
            ','.join(data_dict.keys()),
            ','.join(['%s']*len(data_dict))
        )
        try:
            self.cursor.execute(sql_insert,list(data_dict.values()))
            self.mysql_client.commit()
        except Exception as err:
            self.mysql_client.rollback()
            print(err)

        return item

    def close_spider(self,spider):
        #爬虫结束后，关闭数据库连接和游标
        self.cursor.close()
        self.mysql_client.close()


import pymongo
class JobbolePipelineMongodb(object):

    def __init__(self):
        #创建数据库连接
        self.mongo_client = pymongo.MongoClient(
            '127.0.0.1',27017,
        )
        #获取要操作数据
        db = self.mongo_client['class1808']
        #获取要操作的集合
        self.col = db['jobbole']

    def process_item(self, item, spider):

        data_dict = dict(item)
        try:
            result = self.col.insert(data_dict)
            print(result)
        except Exception as err:
            print(err)

        return item

    def close_spider(self,spider):
        
        self.mongo_client.close()

