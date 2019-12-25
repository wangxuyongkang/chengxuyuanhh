# -*- coding: utf-8 -*-

# Scrapy settings for crawlSpiderUsed project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

#项目的名称，我们使用startprobject创建项目的时候，
#BOT_NAME就会被自动赋值
BOT_NAME = 'crawlSpiderUsed'

#制定爬虫文件的路径
SPIDER_MODULES = ['crawlSpiderUsed.spiders']
NEWSPIDER_MODULE = 'crawlSpiderUsed.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent

# 设置User-Agent，模拟浏览器访问服务器
#USER_AGENT = 'crawlSpiderUsed (+http://www.yourdomain.com)'

# Obey robots.txt rules
# 是否准守robot协议，默认（True）是准守协议的
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# scrapy框架中下载器能发起请求的最大并发量default: 16
# 根据需求自己设定
# CONCURRENT_REQUESTS = 16

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY设置下载延时，默认是0
# （上一次请求和下一次请求的间隔时间）
DOWNLOAD_DELAY = 0
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN:设置每一个域下允许发送请求的最大并发数量
#CONCURRENT_REQUESTS_PER_DOMAIN = 16

# CONCURRENT_REQUESTS_PER_IP:设置每一个ip下允许发请求的最大并发数量
# 注意：如果CONCURRENT_REQUESTS_PER_IP和CONCURRENT_REQUESTS_PER_DOMAIN
# 同时存在，并且CONCURRENT_REQUESTS_PER_IP非0：
# 1.CONCURRENT_REQUESTS_PER_DOMAIN针对于域设置的最大并发数量将会失效，
# 这时将准讯CONCURRENT_REQUESTS_PER_IP 设置的针对于某一个ip下设置的最大并发请求数量
# 2.DOWNLOAD_DELAY下载延时将会针对于ip而不再针对于域了
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# 设置是否携带cookies,默认为True,表示携带
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNET(是一个插件),默认是启用的，可以监听爬虫的开启，运行状态
# 和操作爬虫等
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#设置默认的请求头（全局的，
# 针对某一个爬虫文件的settings设置，
# 可以使用爬虫文件中 custom_settings参数来设置）
DEFAULT_REQUEST_HEADERS = {
  # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  # 'Accept-Language': 'en',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#爬虫中间件（激活爬虫中间件）
#SPIDER_MIDDLEWARES = {
#    'crawlSpiderUsed.middlewares.CrawlspiderusedSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html

#（下载中间件）激活下载中间件，注意,下载中间件后面跟的数字，
# 表示优先级，数字越小，优先级越高
DOWNLOADER_MIDDLEWARES = {
   #'crawlSpiderUsed.middlewares.CrawlspiderusedDownloaderMiddleware': 543,
    'crawlSpiderUsed.middlewares.UserAgentDownloadMiddler':543,
   # 'crawlSpiderUsed.middlewares.SeleniumDownloadMiddlerware':544,
   # 'crawlSpiderUsed.middlewares.ProxyDownloadMiddler':544,
}


#下载中间件相关
USERAGENTS = [
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
]

#设置代理（公开代理和私密代理）
PROXIES = [
    {'ip_port': '111.8.60.9:8123', 'user_pwd': 'user1:pass1'},
    {'ip_port': '101.71.27.120:80', 'user_pwd': 'user2:pass2'},
    {'ip_port': '122.96.59.104:80', 'user_pwd': None},
    {'ip_port': '122.224.249.122:8088', 'user_pwd': None},
]

#动态设置cookies信息
COOKIES = [
    'BAIDU_SSP_lcr=https://www.baidu.com/link?url=pSmchVBgaBLPzZLdtw6Ml8KPzHGZOk9k3KN3S70QZui&wd=&eqid=a0143c050000d2a9000000025c7e0aff; Hm_lvt_aecc9715b0f5d5f7f34fba48a3c511d6=1551764228; UM_distinctid=1694c5b0b11463-0c6389be31db74-36607102-75300-1694c5b0b12285; qHistory=aHR0cDovL3Rvb2wuY2hpbmF6LmNvbSvnq5nplb/lt6Xlhbc=; Hm_lpvt_aecc9715b0f5d5f7f34fba48a3c511d6=1551764257; CNZZDATA5936831=cnzz_eid%3D1239806736-1551758961-%26ntime%3D1551838657',
    'BAIDU_SSP_lcr=https://www.baidu.com/link?url=pSmchVBgaBLPzZLdtw6Ml8KPzHGZOk9k3KN3S70QZui&wd=&eqid=a0143c050000d2a9000000025c7e0aff; Hm_lvt_aecc9715b0f5d5f7f34fba48a3c511d6=1551764228; UM_distinctid=1694c5b0b11463-0c6389be31db74-36607102-75300-1694c5b0b12285; qHistory=aHR0cDovL3Rvb2wuY2hpbmF6LmNvbSvnq5nplb/lt6Xlhbc=; Hm_lpvt_aecc9715b0f5d5f7f34fba48a3c511d6=1551764257; CNZZDATA5936831=cnzz_eid%3D1239806736-1551758961-%26ntime%3D1551838657',
    'BAIDU_SSP_lcr=https://www.baidu.com/link?url=pSmchVBgaBLPzZLdtw6Ml8KPzHGZOk9k3KN3S70QZui&wd=&eqid=a0143c050000d2a9000000025c7e0aff; Hm_lvt_aecc9715b0f5d5f7f34fba48a3c511d6=1551764228; UM_distinctid=1694c5b0b11463-0c6389be31db74-36607102-75300-1694c5b0b12285; qHistory=aHR0cDovL3Rvb2wuY2hpbmF6LmNvbSvnq5nplb/lt6Xlhbc=; Hm_lpvt_aecc9715b0f5d5f7f34fba48a3c511d6=1551764257; CNZZDATA5936831=cnzz_eid%3D1239806736-1551758961-%26ntime%3D1551838657',
]

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# 设置扩展
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#激活管道文件，后面跟的数字表示优先级，数字越小优先级越高
#ITEM_PIPELINES = {
#    'crawlSpiderUsed.pipelines.CrawlspiderusedPipeline': 300,
#}

# 设置下载延时（动态的）
# 最大的优势，设置下载延时时，间隔时间是随机的
# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED默认为False,表示关闭
# AUTOTHROTTLE_ENABLED = True
# # The initial download delay
# #初始的下载延时时间是默认是5秒（单位是秒）
# AUTOTHROTTLE_START_DELAY = 5
# # The maximum download delay to be set in case of high latencies
# #设置最大的请求下载延时时间（单位是秒）
# AUTOTHROTTLE_MAX_DELAY = 10
# # The average number of requests Scrapy should be sending in parallel to
# # each remote server
# #允许发送请求到远端服务器的最大平均并发数量
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# # Enable showing throttling stats for every response received:
# #AUTOTHROTTLE_DEBUG开启degug模式监听我们的 request请求信息
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED：默认情况为False,不开启缓存
# HTTPCACHE_ENABLED = True
# # 设置缓存的过期时间(秒为单位)
# HTTPCACHE_EXPIRATION_SECS = 0
# #设置缓存的存储路径
# HTTPCACHE_DIR = 'httpcache'
# #根据响应的状态码，设置不需要缓存的请求
# HTTPCACHE_IGNORE_HTTP_CODES = ['404','500']
# #关于缓存的一个扩展，是一个插件
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


#设置log日志的存储文件路径
LOG_FILE = 'chinaz.log'
# - CRITICAL - 严重错误(critical)
# - ERROR - 一般错误(regular errors)
# - WARNING - 警告信息(warning messages)
# - INFO - 一般信息(informational messages)
# - DEBUG - 调试信息(debugging messages)
LOG_LEVEL = 'DEBUG'