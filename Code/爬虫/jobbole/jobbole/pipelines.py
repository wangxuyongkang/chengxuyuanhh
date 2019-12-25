# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

#管道文件 ， 过滤数据做持久化处理
import json
import pymysql
class JobbolePipeline(object):

    def __init__(self):
        self.file = open('jobbole.json','a+')



    def process_item(self, item, spider):
        #这个方法必须实现的,
        print('1111经过了管道')


        return item

    def open_spider(self,spider):
        #并不是要必须执行的方法,在爬虫运行的时候执行一次
        print('爬虫开始执行')

    def close_spider(self,spider):


        print('结束了关闭所有的程序')



class jobbolePipelineDb(object):
    def __init__(self):
        self.mysql_data = pymysql.Connect(
            'localhost', 'root', '123456',
            'bole_data', charset='utf8',
            port=3306
        )
        # 创建游标
        self.cursor = self.mysql_data.cursor()

    def process_item(self,item,spider):
        print('222经过管道')
        data_dict = dict(item)
        # 先将item转换为字典
        # data = dict(item)
        # json_data = json.dumps(data,ensure_ascii=False)
        # self.file.write(json_data + '\n')

        my_sql = """
                insert into bole_html(%s)
                values (%s)
                """ % (
            ','.join(data_dict.keys()),
            ','.join(['%s']*len(data_dict))
        )
        try:
            self.cursor.execute(my_sql, list(data_dict.values()))
            self.mysql_data.commit()
        except Exception as err:
            self.mysql_data.rollback()
            print(err)
        """ :param item item ：这个就是爬虫文件中的yield 实例化的对象
            :param spider: 是一个对象,爬虫文件实例化的对象   

        """
        # 注意假如有多个管道，只有return item之后下一个管道才能接受到管道
        return item
    def close_spider(self,spider):
        # 爬虫结束后，关闭数据库连接和游标
        self.cursor.close()
        self.mysql_data.close()

        print('结束了关闭所有的程序')




