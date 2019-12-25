# # 使用scrapy_redis  分布式的基本流程
# step1： pip3 install  scrapy-redis
#
# step2: 设置settings.py设置文件
#
# （1）# 表示使用scrapy_redis自己的去重组件，
#     # 不再使用scrapy框架内部的去重组件
#     DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
#
# （2）# 表示使用scrapy_redis自定义的调度器组件，
#     # 不再使用scrapy框架自带的调度器组件
#     SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# （3）# 允许暂停，redis数据库中的保存的任务不会被清空，可以恢复和暂停
#     # （断点爬取）
#     SCHEDULER_PERSIST = True
#
# （4）如果不使用默认的request队列模式（则设置队列模式）
#     # 调度器存储request队列的模式（三种）
#     #SpiderPriorityQueue：是scrapy_redis框架（默认）的请求队列形式
#     #（有自己的优先级），按照redis数据库中的有序集合的方式取

#     #SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"
#
#     #SpiderQueu：请求队列形式，按照先进先出的方式
#     #SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"
#     #SpiderStack：请求队列形式，按照先进的后出的方式（类似栈的结构）
#     #SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderStack"
#  (5) 如果需要将item数据统一存放在redis数据库中（可选）
#     'scrapy_redis.pipelines.RedisPipeline'
#
#  (6)
#     #指定要存储数据的redis数据库的hsot(ip)
#     REDIS_HOST = '118.24.255.219'
#     #指定要存储数据的redis数据库的端口号
#     # mysql(3306) mongodb(27017) redis(6379)
#     REDIS_PORT = 6379
#
# 关于代码部分：
#  （1）如果要使用scrapy_redis的去重和存储功能（没有实现分布式）
#     则只需要修改settings.py设置文件，爬虫部分代码照常
#
#   (2) 实现crawlSpider的分布式爬虫
#       step1：导入RedisCrawlSpider
#         from scrapy_redis.spiders import RedisCrawlSpider
#
#       step2：修改爬虫文件继承的类
#         class MyCrawler(RedisCrawlSpider)
#
#       step3:添加redis_key(根据redis_key从redis数据库中获取起始任务)
#         redis_key = '爬虫名称:start_urls'
#         注意：需要将原来的start_urls去重
#
#     其他代码照常不变
#
#
#  （3）实现scrapy.spider的分布式爬虫
#     step1:导入RedisSpider
#         from scrapy_redis.spiders import RedisSpider
#
#     step2：修改爬虫文件继承的类
#         class MySpider(RedisSpider):
#
#     step3:添加redis_key(根据redis_key从redis数据库中获取起始任务)
#             redis_key = '爬虫名称:start_urls'
#             注意：需要将原来的start_urls去重
#
#     其他代码照常不变
#
#
# 注意分布式爬虫（scrapy_redis实现的）
# master端（主节点）：
#     主要是保存Requst请求，指纹，items数据，设置起始任务
#     （一般master不负责爬取工作）
#
# slave端（从节点）：
#     爬虫端，从master端获取任务，请求获取响应结果，
#     提取数据，获取新的url任务，将获取的数据和新的请求，
#     交给 master 端管理
#
# 使用redis数据库的优点
# 1.redis数据库有丰富的数据类型（string、hash、list、set、zset）
# 2.redis数据库是基于内存的存储，读写的效率高。
#
#
# scrapy_redis自定义的模块
# 1.调度器组件
# 2.去重组件
# 3.管道
# 4.base spider (RedisSpider,RedisCrawlSpider)
