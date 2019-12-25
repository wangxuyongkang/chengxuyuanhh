# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from crawlSpiderUsed.items import ChinazWebItem


class ChinaSpider(CrawlSpider):
    name = 'china'
    allowed_domains = ['chinaz.com']
    start_urls = ['http://top.chinaz.com/hangyemap.html']

    rules = (
        #http://top.chinaz.com/hangye/index_yule_yinyue.html
        #http://top.chinaz.com/hangye/index_yule_yinyue_2.html

        #http://top.chinaz.com/hangye/index_shopping_dianshang.html
        #http://top.chinaz.com/hangye/index_gov_zhengfu.html
        Rule(
            LinkExtractor(
                allow=r'http://top.chinaz.com/hangye/index_.*?.html',
                restrict_xpaths= [
                    '//div[@class="TopMapAll"]',
                    '//div[@class="ListPageWrap"]'
                ]
            ),
             callback='parse_item',
            follow=True
        ),
    )

    def parse_item(self, response):

        print(response.status,response.url)
        print(response.request.headers)

        #
        web_lis = response.xpath('//ul[@class="listCentent"]/li')

        for web_li in web_lis:
            webItem = ChinazWebItem()
            # 封面图
            webItem['coverImage'] = web_li.xpath('.//div[@class="leftImg"]//img/@src').extract_first('')
            # 标题
            webItem['title'] = web_li.xpath('.//h3[@class="rightTxtHead"]/a/text()').extract_first('')
            # 域
            webItem['domains'] = web_li.xpath('.//h3[@class="rightTxtHead"]/span[@class="col-gray"]/text()').extract_first('')
            # 描述
            webItem['content'] = web_li.xpath('.//p[@class="RtCInfo"]/text()').extract_first('')

            # yield webItem
            #
            # yield scrapy.Request()
