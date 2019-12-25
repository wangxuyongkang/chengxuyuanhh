from scrapy_redis.spiders import RedisSpider


class MySpider(RedisSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    #爬虫名称
    name = 'myspider_redis'
    #设置允许爬取的域
    allowed_domains = ['chinaz.com']
    #redis_key: 作用是获取redis数据库中设置(存储)的起始url
    redis_key = 'myspider:start_urls'

    # def __init__(self, *args, **kwargs):
    #     # Dynamically define the allowed domains list.
    #     domain = kwargs.pop('domain', '')
    #     self.allowed_domains = filter(None, domain.split(','))
    #     super(MySpider, self).__init__(*args, **kwargs)

    def parse(self, response):
       #提取分类url的地址
        response.xpath('//div[@class=""]')
