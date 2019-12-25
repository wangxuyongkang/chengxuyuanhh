# 创建项目
# scrapy startproject 项目名
#
# 创建爬虫文件 进入到项目的spider文件夹下
#
# scrapy genspider 爬虫文件 域
# #项目的目录结构
#
# spiders文件夹 ->  所有的爬虫文件都放在这个文件夹下
#
#     爬虫文件:
#         爬虫文件的名称:name
#         allow_domains:设置允许爬取的网站对应的域(list)
#         start_urls: 设置起始url (list)
#
#         def parse(self,response):
#             回调函数，获取请求(request)的相应结果
# items.py:在这里定义要爬取的字段,爬虫文件中获取的数据
#         需要赋值给这里面的类实例化对象。
#
#
# middlerware : 爬虫中间件和下载中间件
#
#
#
#
# pipeline : 数据管道
#     管道文件
#     （注意:管道文件接触items有两个前提）
#     1.确保爬虫文件中获取的itme yield 给管道了
#     2.确保管道文件在设置中被激活了
#     class xxxxxpipline(object):
#
#         def process_item(self,item,spider):
#             item:爬虫文件中获取的itme
#             spider:就是指的爬虫文件(实例化的对象)
#
# settings.py 设置文件:可以设置UA,请求头，是否遵守robot协议，下载延迟，激活管道....