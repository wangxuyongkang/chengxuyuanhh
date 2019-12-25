# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.exceptions import DropItem
import pymysql
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.project import get_project_settings
####下载图片
#获取settings文件中的参数
IMAGES_STORE = get_project_settings().get('IMAGES_STORE')

class DemoImagePipline(ImagesPipeline):
    #重写方法一
    def get_media_requests(self, item, info):
        '''获取item的下载图片路径'''
        book_image = item['book_image']
        yield scrapy.Request(url=book_image)

    def item_completed(self, results, item, info):
        # results:存放的是图片的下载信息
        print(results)
        if results:
            for status,info in results:
                if status:
                    item['local_image_path'] = IMAGES_STORE+'//'+info['path']
                else:
                    raise DropItem('图片下载失败,丢弃item')
        return item



class DemoPipeline(object):
    
    def __init__(self):
        self.client = pymysql.Connect(
            '127.0.0.1','root','123456',
            'class1809',3306,charset='utf8',
        )
        self.cursor = self.client.cursor()

    def process_item(self, item, spider):
        """
        item:DemoItem
        item:categoryItem
        """

        if len(item['name']) == 0:
            raise DropItem('没有获取到书名')

        #存储数据
        data = dict(item)
        sql = item.get_sql_str(data)

        try:
            self.cursor.execute(sql,list(data.values()))
            self.client.commit()
        except Exception as err:
            print(err)
            self.client.rollback()

        return item

    def close_spider(self,spider):
        #可选方法,只有在爬虫结束的时候会执行一次
        self.client.close()
        self.cursor.close()
