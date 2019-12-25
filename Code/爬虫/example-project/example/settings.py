# Scrapy settings for example project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#
SPIDER_MODULES = ['example.spiders']
NEWSPIDER_MODULE = 'example.spiders'

USER_AGENT = 'scrapy-redis (+https://github.com/rolando/scrapy-redis)'

#1
# 表示使用scrapy_redis自己的去重组件，
# 不再使用scrapy框架内部的去重组件
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

#2
# 表示使用scrapy_redis自定义的调度器组件，
# 不再使用scrapy框架自带的调度器组件
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

#3
# 允许暂停，redis数据库中的保存的任务不会被清空，可以恢复和暂停
# （断点爬取）
SCHEDULER_PERSIST = True

#4（队列模式，不设置会使用 第一种）
# 调度器存储request队列的模式（三种）
#SpiderPriorityQueue：是scrapy_redis框架（默认）的请求队列形式
#（有自己的优先级），按照redis数据库中的有序集合的方式取
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"

#SpiderQueu：请求队列形式，按照先进先出的方式
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"
#SpiderStack：请求队列形式，按照先进的后出的方式（类似栈的结构）
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderStack"

#激活管道
ITEM_PIPELINES = {
    'example.pipelines.ChinazPipeline': 300,
    # RedisPipeline：将爬虫文件获取到的数据统一存
    # 放至 redis 数据库中 5
    'scrapy_redis.pipelines.RedisPipeline': 400,
}

# 6
#指定要存储数据的redis数据库的hsot(ip)
REDIS_HOST = '118.24.255.219'

# 7
#指定要存储数据的redis数据库的端口号
# mysql(3306) mongodb(27017) redis(6379)
REDIS_PORT = 6390
























#设置log日志等级，
LOG_LEVEL = 'DEBUG'

# Introduce an artifical delay to make use of parallelism. to speed up the
# crawl.
#设置下载延时
DOWNLOAD_DELAY = 1
