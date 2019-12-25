# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import pymysql

class WanfangPipeline(object):

    def __init__(self):
        # self.mysql_client = pymysql.Connect(
        #     '127.0.0.1','root','ljh1314',
        #     'wanwang',charset='utf8',
        # )

        self.mysql_client = pymysql.Connect(
            'rm-2zet9m2x33kh23506o.mysql.rds.aliyuncs.com','bylwdata',
            're(r02fdkW+ny9dsOD^','paper_data', charset='utf8',
        )

        self.cursor = self.mysql_client.cursor()

    def process_item(self, item, spider):
        print('1111111111111111111111111111111111')

        insertSql,insertData = item.get_sql_data(dict(item))

        try:
            self.cursor.execute(insertSql,insertData)
            self.mysql_client.commit()
        except Exception as err:
            print(err)
            self.mysql_client.rollback()
        return item

        # data = json.dumps(dict(item),ensure_ascii=False)+'\n'
        # with open('tech.json','a+') as filehandler:
        #     filehandler.write(data)
        # return item

    def close_spider(self,spider0):
        self.mysql_client.close()
        self.cursor.close()

