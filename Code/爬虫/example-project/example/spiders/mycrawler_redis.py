from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from scrapy_redis.spiders import RedisCrawlSpider

from example.items import ChianzWebItem


class MyCrawler(RedisCrawlSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    # 爬虫名称
    name = 'mycrawler_redis'
    #
    allowed_domains = ['chinaz.com']
    # 获取redis数据库中设置的起始的url任务
    redis_key = 'mycrawler:start_urls'


    # 在初识化方法中，动态获取要爬取的域（一般不用）
    # def __init__(self, *args, **kwargs):
    #     # Dynamically define the allowed domains list.
    #     domain = kwargs.pop('domain', '')
    #     self.allowed_domains = filter(None, domain.split(','))
    #     super(MyCrawler, self).__init__(*args, **kwargs)

    # 设置提取url的规则
    rules = [
        # http://top.chinaz.com/hangye/index_yule_yinyue.html
        # http://top.chinaz.com/hangye/index_zonghe_falu.html
        Rule(
            LinkExtractor(
                allow=r'http://top.chinaz.com/hangye/index_.*?.html',
                restrict_xpaths=['//div[@class="TopMapAll"]', '//div[@class="ListPageWrap"]']
            ),
            callback='parse_category_data',
            follow=True,
        )
    ]

    def parse_category_data(self, response):
        web_lis = response.xpath('//ul[@class="listCentent"]/li')

        for web_li in web_lis:
            # 实例化item
            web_item = ChianzWebItem()
            # 标题
            web_item['title'] = web_li.xpath('.//h3[@class="rightTxtHead"]/a/text()').extract_first('')
            # 域
            web_item['domain'] = web_li.xpath('.//h3[@class="rightTxtHead"]/span/text()').extract_first('')
            # content
            web_item['content'] = web_li.xpath('.//p[@class="RtCInfo"]/text()').extract_first('')

            yield web_item
