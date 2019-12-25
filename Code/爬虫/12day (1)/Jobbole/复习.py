#pip3 install scrpay

#创建项目
# scrapy startproject 项目名称
#
# #创建爬虫文件（进入到项目的spiders文件夹下）
# scrapy genspider 爬虫文件 域
#
# #项目的目录结构
# spiders文件夹  -> 所有的爬虫文件都放在这个文件夹下
#    爬虫文件：
#        name:爬虫文件的名称
#        allow_domains:设置允许爬取的网站对应的域 （list）
#        start_urls: 设置起始url （list）
#        def parse(self,response):
#            回调函数，获取请求（request）的响应结果
# items.py: 在这里定制要爬取的字段，爬虫文件中获取的数据
#           需要赋值给这里面的类实例化的对象。
#
# middlerware: 爬虫中间件和下载中间件
#
# pipeline:数据管道
#     管道文件
#     （注意：管道文件能够接收到item有两个前提）
#     1.确保爬虫文件中获取的item yield 给管道了
#     2.确保管道文件在设置文件中被激活了
#
#     class xxxxpipeline(object):
#
#         def process_item(self,item,spider):
#             item：爬虫文件中获取的item
#             spider：就是指的爬虫文件（实例化的对象）
#
# settings.py 设置文件:可以设置UA、请求头、
#         是否准守robot协议、下载延时、激活管道文件....
#
#
#
#
#
#
#


