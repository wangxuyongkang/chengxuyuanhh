from scrapy_redis.spiders import RedisSpider
import scrapy
from example.items import ChianzWebItem

# class MySpider(scrapy.spiders):
class MySpider(RedisSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    # 爬虫的名称
    name = 'myspider_redis'
    # 设置允许爬取的域
    allowed_domains = ['chinaz.com']
    # redis_key :作用是获取redis数据库中设置（存储）的起始url
    #http://top.chinaz.com/hangyemap.html
    redis_key = 'myspider:start_urls'

    # def __init__(self, *args, **kwargs):
    #     # Dynamically define the allowed domains list.
    #     domain = kwargs.pop('domain', '')
    #     self.allowed_domains = filter(None, domain.split(','))
    #     super(MySpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        #提取分类的url地址（就是每一个分类的首页的url地址）
        category_urls = response.xpath('//div[@class="TopMapAll"]//div[@class="Taright"]/a/@href').extract()

        for category_url in category_urls:
            print(category_url)
            yield scrapy.Request(url=category_url,callback=self.parse_category_data)

    def parse_category_data(self, response):
        """
        解析分类的列表数据
        :param response:
        :return:
        """

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

        #获取每一个分类下其他分页数据
        next_pages= response.xpath('//div[@class="ListPageWrap"]//a/@href').extract()
        if len(next_pages) > 0:
            for next_page in next_pages:
                if '.html' in next_page:
                    #http://top.chinaz.com/hangye/index_yule_yinyue.html
                    #http://top.chinaz.com/hangye/index_gov_zhengfu.html
                    # next_page = 'http://top.chinaz.com/hangye/'+next_page
                    #将不完整的url 地址评级完整
                    next_page = response.urljoin(next_page)

                    yield scrapy.Request(url=next_page,callback=self.parse_category_data)



