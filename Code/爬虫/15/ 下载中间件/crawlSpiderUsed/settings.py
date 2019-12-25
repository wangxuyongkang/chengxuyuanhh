# -*- coding: utf-8 -*-

# Scrapy settings for crawlSpiderUsed project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'crawlSpiderUsed'

SPIDER_MODULES = ['crawlSpiderUsed.spiders']
NEWSPIDER_MODULE = 'crawlSpiderUsed.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent

# 设置User-Agent
#USER_AGENT = 'crawlSpiderUsed (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.5
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  # 'Accept-Language': 'en',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'crawlSpiderUsed.middlewares.CrawlspiderusedSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html

#激活下载中间件
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
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'crawlSpiderUsed.pipelines.CrawlspiderusedPipeline': 300,
#}

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
