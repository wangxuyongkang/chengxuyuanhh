from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from example.items import ChianzWebItem

# 这个案例并没有实现分布式，存在的意义
# 可以使用scrapy_redis中的去重 功能和
# 存储request和item的功能
class DmozSpider(CrawlSpider):
    """Follow categories and extract links."""
    name = 'dmoz'
    allowed_domains = ['chinaz.com']
    start_urls = ['http://top.chinaz.com/hangyemap.html']

    rules = [
        #http://top.chinaz.com/hangye/index_yule_yinyue.html
        #http://top.chinaz.com/hangye/index_zonghe_falu.html
        Rule(
            LinkExtractor(
                allow=r'http://top.chinaz.com/hangye/index_.*?.html',
                restrict_xpaths=['//div[@class="TopMapAll"]','//div[@class="ListPageWrap"]']
            ),
            callback='parse_category_data',
            follow=True,
        )
    ]

    def parse_category_data(self, response):

        web_lis = response.xpath('//ul[@class="listCentent"]/li')

        for web_li in web_lis:
            #实例化item
            web_item = ChianzWebItem()
            # 标题
            web_item['title'] = web_li.xpath('.//h3[@class="rightTxtHead"]/a/text()').extract_first('')
            # 域
            web_item['domain'] = web_li.xpath('.//h3[@class="rightTxtHead"]/span/text()').extract_first('')
            # content
            web_item['content'] = web_li.xpath('.//p[@class="RtCInfo"]/text()').extract_first('')

            yield web_item


