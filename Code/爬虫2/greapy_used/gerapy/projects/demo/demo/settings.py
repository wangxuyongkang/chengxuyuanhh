# -*- coding: utf-8 -*-

# Scrapy settings for demo project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'demo'

SPIDER_MODULES = ['demo.spiders']
NEWSPIDER_MODULE = 'demo.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'demo (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#设置下载器最大的并发请求数量default: 16
CONCURRENT_REQUESTS = 3

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#设置下载延时（单位时间为秒）
DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default:True)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# COOKIES_ENABLED = True：Cokies放在请求头中是不生效的
# COOKIES_ENABLED = False：Cokies放在请求头中是生效的

DEFAULT_REQUEST_HEADERS = {
  # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  # 'Accept-Language': 'en',
   'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'demo.middlewares.DemoSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#激活下载中间件，数字越大，优先级越底
DOWNLOADER_MIDDLEWARES = {
   'demo.middlewares.DemoDownloaderMiddleware': 543,
   'demo.middlewares.CustomUADownloadMiddlerWare':544,
   # 'demo.middlewares.SeleniumMiddleware':545,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#激活管道,后面的数字表示优先级,数字越小，优先级越高，越先执行
ITEM_PIPELINES = {
   # 'demo.pipelines.DemoImagesPipeline':299,
   # 'demo.pipelines.DemoPipeline': 300,
    #将分布式爬虫端获取的item数据同一存储到redis数据库
    'scrapy_redis.pipelines.RedisPipeline': 400,
}

##设置图片的存储路径
IMAGES_STORE = '/Users/ljh/Desktop/桌面/1809人工智能4/代码/第29天/demo/images'

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


####UA池
USER_AGENTS = [
   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:68.0) Gecko/20100101 Firefox/68.0',
]

###模拟代理池（少量ip的时候，多的时候存入数据库）
PROXIES = [
    {'ip_port': '111.8.60.9:8123', 'user_pwd': 'user1:pass1'},
    {'ip_port': '101.71.27.120:80', 'user_pwd': 'user2:pass2'},
    {'ip_port': '122.96.59.104:80', 'user_pwd': None},
    {'ip_port': '122.224.249.122:8088', 'user_pwd': None},
]


###cookies 池（少量cookies的时候，多的时候存入数据库）
COOKIES = [
   'BAIDU_SSP_lcr=https://www.baidu.com/link?url=M68Q8fh1IG099c-ys0ja2R0sJeNxDRE7xccSihvd2702wjmxbidzef6T60VmMwPv&wd=&eqid=91c09f09000ecdd2000000025d4a7af2; Hm_lvt_7839b44f7a3c4b83b2e218c8d227dfad=1565158932,1565162231; readrecord=6474%2C232376%2C%u7231%u60C5%u516C%u5BD35%2C%u300A%u7231%u60C5%u516C%u5BD35%u300B%u5B8C%u7ED3%u611F%u8A00%2C2019-08-08%2014%3A11%3A27%248985%2C962973%2C%u65E0%u4E0A%u5251%u9053%2C%u7B2C%u4E00%u7AE0%20%u83AB%u51E1%2C2019-08-08%2014%3A13%3A24%246699%2C230681%2C%u751F%u547D%u638C%u63A7%u8005%u4E4B%u7EB5%u6A2A%u5929%u4E0B%2C%u7B2C%u4E00%u7AE0%uFF1A%u82E6%u903C%u9752%u5E74%2C2019-08-08%2014%3A22%3A12%24; Hm_lpvt_7839b44f7a3c4b83b2e218c8d227dfad=1565245334',
   'BAIDU_SSP_lcr=https://www.baidu.com/link?url=M68Q8fh1IG099c-ys0ja2R0sJeNxDRE7xccSihvd2702wjmxbidzef6T60VmMwPv&wd=&eqid=91c09f09000ecdd2000000025d4a7af2; Hm_lvt_7839b44f7a3c4b83b2e218c8d227dfad=1565158932,1565162231; readrecord=6474%2C232376%2C%u7231%u60C5%u516C%u5BD35%2C%u300A%u7231%u60C5%u516C%u5BD35%u300B%u5B8C%u7ED3%u611F%u8A00%2C2019-08-08%2014%3A11%3A27%248985%2C962973%2C%u65E0%u4E0A%u5251%u9053%2C%u7B2C%u4E00%u7AE0%20%u83AB%u51E1%2C2019-08-08%2014%3A13%3A24%246699%2C230681%2C%u751F%u547D%u638C%u63A7%u8005%u4E4B%u7EB5%u6A2A%u5929%u4E0B%2C%u7B2C%u4E00%u7AE0%uFF1A%u82E6%u903C%u9752%u5E74%2C2019-08-08%2014%3A22%3A12%24; Hm_lpvt_7839b44f7a3c4b83b2e218c8d227dfad=1565245334',
   'BAIDU_SSP_lcr=https://www.baidu.com/link?url=M68Q8fh1IG099c-ys0ja2R0sJeNxDRE7xccSihvd2702wjmxbidzef6T60VmMwPv&wd=&eqid=91c09f09000ecdd2000000025d4a7af2; Hm_lvt_7839b44f7a3c4b83b2e218c8d227dfad=1565158932,1565162231; readrecord=6474%2C232376%2C%u7231%u60C5%u516C%u5BD35%2C%u300A%u7231%u60C5%u516C%u5BD35%u300B%u5B8C%u7ED3%u611F%u8A00%2C2019-08-08%2014%3A11%3A27%248985%2C962973%2C%u65E0%u4E0A%u5251%u9053%2C%u7B2C%u4E00%u7AE0%20%u83AB%u51E1%2C2019-08-08%2014%3A13%3A24%246699%2C230681%2C%u751F%u547D%u638C%u63A7%u8005%u4E4B%u7EB5%u6A2A%u5929%u4E0B%2C%u7B2C%u4E00%u7AE0%uFF1A%u82E6%u903C%u9752%u5E74%2C2019-08-08%2014%3A22%3A12%24; Hm_lpvt_7839b44f7a3c4b83b2e218c8d227dfad=1565245334',
   'BAIDU_SSP_lcr=https://www.baidu.com/link?url=M68Q8fh1IG099c-ys0ja2R0sJeNxDRE7xccSihvd2702wjmxbidzef6T60VmMwPv&wd=&eqid=91c09f09000ecdd2000000025d4a7af2; Hm_lvt_7839b44f7a3c4b83b2e218c8d227dfad=1565158932,1565162231; readrecord=6474%2C232376%2C%u7231%u60C5%u516C%u5BD35%2C%u300A%u7231%u60C5%u516C%u5BD35%u300B%u5B8C%u7ED3%u611F%u8A00%2C2019-08-08%2014%3A11%3A27%248985%2C962973%2C%u65E0%u4E0A%u5251%u9053%2C%u7B2C%u4E00%u7AE0%20%u83AB%u51E1%2C2019-08-08%2014%3A13%3A24%246699%2C230681%2C%u751F%u547D%u638C%u63A7%u8005%u4E4B%u7EB5%u6A2A%u5929%u4E0B%2C%u7B2C%u4E00%u7AE0%uFF1A%u82E6%u903C%u9752%u5E74%2C2019-08-08%2014%3A22%3A12%24; Hm_lpvt_7839b44f7a3c4b83b2e218c8d227dfad=1565245334',
   'BAIDU_SSP_lcr=https://www.baidu.com/link?url=M68Q8fh1IG099c-ys0ja2R0sJeNxDRE7xccSihvd2702wjmxbidzef6T60VmMwPv&wd=&eqid=91c09f09000ecdd2000000025d4a7af2; Hm_lvt_7839b44f7a3c4b83b2e218c8d227dfad=1565158932,1565162231; readrecord=6474%2C232376%2C%u7231%u60C5%u516C%u5BD35%2C%u300A%u7231%u60C5%u516C%u5BD35%u300B%u5B8C%u7ED3%u611F%u8A00%2C2019-08-08%2014%3A11%3A27%248985%2C962973%2C%u65E0%u4E0A%u5251%u9053%2C%u7B2C%u4E00%u7AE0%20%u83AB%u51E1%2C2019-08-08%2014%3A13%3A24%246699%2C230681%2C%u751F%u547D%u638C%u63A7%u8005%u4E4B%u7EB5%u6A2A%u5929%u4E0B%2C%u7B2C%u4E00%u7AE0%uFF1A%u82E6%u903C%u9752%u5E74%2C2019-08-08%2014%3A22%3A12%24; Hm_lpvt_7839b44f7a3c4b83b2e218c8d227dfad=1565245334',
]


#####分布式爬虫设置
#设置scrapy_redis的去重组件，不再使用scrapy框架自带的去重组件
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
#调度器:使用scrapy-redis自定义的调度器组件，而不再使用scrapy自带的调度器
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

#三种存储请求任务的队列模式
#scrapy—redis默认的队列模式，有自己的优先级
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"
#存储任务：先进先出
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"
#存储任务：先进后出
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderStack"

#断点爬取
SCHEDULER_PERSIST = True


#指定主节点的redis服务器的ip
REDIS_HOST = '127.0.0.1'
# REDIS_HOST = '118.24.255.219'
#指定主节点的redis服务器的端口
REDIS_PORT = 6379
# REDIS_PORT = 6380
