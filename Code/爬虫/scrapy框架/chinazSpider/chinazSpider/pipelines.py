# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class ChinazspiderPipeline(object):
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
        insertSql,data = item.get_sql_insertdata(item_dict)
        print('2222',insertSql,data)
        try:
            self.cursor.execute(insertSql,data)
            self.mysql_con.commit()
            print('插入成功')
        except Exception as err:
            self.mysql_con.rollback()
            print('11111,插入失败',err)
        return item


    def close_spider(self,spider):
        #关闭游标和数据库连接
        self.cursor.close()
        self.mysql_con.close()
