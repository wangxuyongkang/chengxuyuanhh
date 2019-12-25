# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from chinazSpider.items import ChinazspiderItem

class ChinaSpider(CrawlSpider):
    name = 'china'
    allowed_domains = ['chinaz.com']
    start_urls = ['http://top.chinaz.com/hangyemap.html']

    rules = (
        Rule(
            LinkExtractor(allow=r'http://top.chinaz.com/hangye/index_.*?.html',
                          restrict_xpaths=['//div[@class="TopMapAll"]','//div[@class="ListPageWrap"]']
                          ),
            callback='parse_item',
            follow=True
        ),
        # Rule(
        #     LinkExtractor(
        #         allow=r'http://top.chinaz.com/hangye/index_.*?.html',
        #         restrict_xpaths='//div[@class="ListPageWrap"]/a'
        #     ),
        #     callback='',
        #     follow=True
        # )
    )

    def parse_page_data(self, response):
        item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        print('请求成功',response.status,response.url)
        return item

    def parse_item(self, response):
        print('走了1111111111',response.url)
        web_lis = response.xpath('//ul[@class="listCentent"]/li')
        for web_li in web_lis:
            webItem = ChinazspiderItem()
            webItem['coverImage'] = 'https:'+ web_li.xpath('.//div[@class="leftImg"]//img/@src').extract_first('')
            webItem['title'] = web_li.xpath('.//h3[@class="rightTxtHead"]/a/text()').extract_first('')
            webItem['domains'] = 'https:' + web_li.xpath('.//h3[@class="rightTxtHead"]/span[@class="col-gray"]/text()').extract_first('')
            webItem['context'] = web_li.xpath('.//p[@class="RtCInfo"]/text()').extract_first('')
            webItem['score'] = web_li.xpath('.//div[@class="RtCRateCent"]/span/text()').extract_first('')
            print(webItem)
            yield webItem
