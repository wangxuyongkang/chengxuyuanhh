# -*- coding: utf-8 -*-

# Scrapy settings for tianyancha project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'tianyancha'

SPIDER_MODULES = ['tianyancha.spiders']
NEWSPIDER_MODULE = 'tianyancha.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'tianyancha (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 2

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#默认情况为True，表示携带cookies
#一般情况下先把这个值设置为False，不携带cookies
#防止对方根据cookies进行反爬虫

COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  # 'Accept-Language': 'en',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'tianyancha.middlewares.TianyanchaSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'tianyancha.middlewares.TianyanchaDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'tianyancha.pipelines.TianyanchaPipeline': 300,
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

# 设置cookies信息的时候，一定要多设置几个（cookies 池）
TYC_COOKIES = [
    #'aliyungf_tc=AQAAAD9Gciu5zwwAWkxI37fnOSMX8Ogf; csrfToken=kDTktxm6CemWMujkmmx3zu3N; TYCID=0a75ba403e8911e9aec4f9c5484d69fe; undefined=0a75ba403e8911e9aec4f9c5484d69fe; ssuid=7820446254; _ga=GA1.2.1489544742.1551709396; _gid=GA1.2.999128257.1551709396; __insp_wid=677961980; __insp_nv=true; RTYCID=bf44330005904f02bdda4a819c859e03; __insp_targlpu=aHR0cHM6Ly93d3cudGlhbnlhbmNoYS5jb20vY29tcGFueS8zMjM0NzU3MTg1; __insp_targlpt=5oi%2F5bGx5Yy65q6L55a_5Lq65Yac55aX5bq35aSN5Lit5b_DX_W3peWVhuS%2FoeaBr1%2Fkv6HnlKjmiqXlkYpf6LSi5Yqh5oql6KGoX_eUteivneWcsOWdgOafpeivoi3lpKnnnLzmn6U%3D; CT_TYCID=2dc7dab168dc4cda86c22469b171ea69; __insp_norec_sess=true; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1551709395,1551710860; bannerFlag=true; token=b15cbdcec8be488da468d12743b90a29; _utm=e148c6c33ff54d22a873f6329aa65687; tyc-user-info=%257B%2522claimEditPoint%2522%253A%25220%2522%252C%2522myAnswerCount%2522%253A%25220%2522%252C%2522myQuestionCount%2522%253A%25220%2522%252C%2522explainPoint%2522%253A%25220%2522%252C%2522privateMessagePointWeb%2522%253A%25220%2522%252C%2522nickname%2522%253A%2522%25E7%25BB%25B4%25E6%258B%2589%25C2%25B7%25E6%25B3%2595%25E7%25B1%25B3%25E5%258A%25A0%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522privateMessagePoint%2522%253A%25220%2522%252C%2522state%2522%253A0%252C%2522announcementPoint%2522%253A%25220%2522%252C%2522isClaim%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522discussCommendCount%2522%253A%25221%2522%252C%2522monitorUnreadCount%2522%253A%252253%2522%252C%2522onum%2522%253A%25220%2522%252C%2522claimPoint%2522%253A%25220%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODUxODc1MzI2NSIsImlhdCI6MTU1MTcxMjYwNSwiZXhwIjoxNTY3MjY0NjA1fQ.YDyaJuerAchnXfnaZjJsh5114AYVCvJ-mUCabLpBUfi3Ewpzbphh2ZjGUnONvCt1D_pEDryzr1zE3JB_nzYUiQ%2522%252C%2522pleaseAnswerCount%2522%253A%25221%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522bizCardUnread%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252218518753265%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODUxODc1MzI2NSIsImlhdCI6MTU1MTcxMjYwNSwiZXhwIjoxNTY3MjY0NjA1fQ.YDyaJuerAchnXfnaZjJsh5114AYVCvJ-mUCabLpBUfi3Ewpzbphh2ZjGUnONvCt1D_pEDryzr1zE3JB_nzYUiQ; _gat_gtag_UA_123487620_1=1; refresh_page=null; __insp_slim=1551712635147; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1551712635; cloud_token=77449c5c03714c648fe36c9938802c1c; cloud_utm=5f0f0887cc7d44ac940f84b58dfd0d58',
    'aliyungf_tc=AQAAAD9Gciu5zwwAWkxI37fnOSMX8Ogf; csrfToken=kDTktxm6CemWMujkmmx3zu3N; TYCID=0a75ba403e8911e9aec4f9c5484d69fe; undefined=0a75ba403e8911e9aec4f9c5484d69fe; ssuid=7820446254; _ga=GA1.2.1489544742.1551709396; _gid=GA1.2.999128257.1551709396; RTYCID=bf44330005904f02bdda4a819c859e03; CT_TYCID=2dc7dab168dc4cda86c22469b171ea69; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1551709395,1551710860; bannerFlag=true; __insp_wid=677961980; __insp_nv=true; __insp_targlpu=aHR0cHM6Ly93d3cudGlhbnlhbmNoYS5jb20vbG9naW4%2FZnJvbT1odHRwcyUzQSUyRiUyRnd3dy50aWFueWFuY2hhLmNvbSUyRnNlYXJjaCUzRmJhc2UlM0Riag%3D%3D; __insp_targlpt=5aSp55y85p_lLeWVhuS4muWuieWFqOW3peWFt1%2FkvIHkuJrkv6Hmga%2Fmn6Xor6Jf5YWs5Y_45p_l6K_iX_W3peWVhuafpeivol%2FkvIHkuJrkv6HnlKjkv6Hmga%2Fns7vnu58%3D; __insp_norec_sess=true; token=1966deb87c1c47e789f3d6a91eeef1fc; _utm=eb1cbc1a3253445b81c41114fb05d32c; tyc-user-info=%257B%2522claimEditPoint%2522%253A%25220%2522%252C%2522myAnswerCount%2522%253A%25220%2522%252C%2522myQuestionCount%2522%253A%25220%2522%252C%2522explainPoint%2522%253A%25220%2522%252C%2522privateMessagePointWeb%2522%253A%25220%2522%252C%2522nickname%2522%253A%2522%25E7%25BB%25B4%25E6%258B%2589%25C2%25B7%25E6%25B3%2595%25E7%25B1%25B3%25E5%258A%25A0%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522privateMessagePoint%2522%253A%25220%2522%252C%2522state%2522%253A%25220%2522%252C%2522announcementPoint%2522%253A%25220%2522%252C%2522isClaim%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522discussCommendCount%2522%253A%25221%2522%252C%2522monitorUnreadCount%2522%253A%252253%2522%252C%2522onum%2522%253A%25220%2522%252C%2522claimPoint%2522%253A%25220%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODUxODc1MzI2NSIsImlhdCI6MTU1MTc0NzYxMiwiZXhwIjoxNTY3Mjk5NjEyfQ.ZpiVQbE9WTRkS4H1p8vpsLMdX5HtSqJtQ0W_Ai7DqxnsBAgV9_iiMtzhifpGRsgX-LaFSxjjR-g9V_o8VSbdeg%2522%252C%2522pleaseAnswerCount%2522%253A%25221%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522bizCardUnread%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252218518753265%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODUxODc1MzI2NSIsImlhdCI6MTU1MTc0NzYxMiwiZXhwIjoxNTY3Mjk5NjEyfQ.ZpiVQbE9WTRkS4H1p8vpsLMdX5HtSqJtQ0W_Ai7DqxnsBAgV9_iiMtzhifpGRsgX-LaFSxjjR-g9V_o8VSbdeg; refresh_page=null; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1551747909; __insp_slim=1551747909752; cloud_token=3b77172d8b37441e829c620a7d13bc2c; cloud_utm=a0059fa7b4dc4089a4004b7d8e301167',
]