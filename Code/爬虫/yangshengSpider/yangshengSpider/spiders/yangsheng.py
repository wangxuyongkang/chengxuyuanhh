# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from yangshengSpider.items import YangshengspiderItem,YangshengspiderItem_data

class YangshengSpider(CrawlSpider):
    name = 'yangsheng'
    allowed_domains = ['ys137.com']
    start_urls = ['https://www.ys137.com/zyys/']

    rules = (#https://www.ys137.com/zyys/zycs/
        Rule(LinkExtractor(allow=r'https://www.ys137.com/zyys/.*?/',
                           restrict_xpaths='//div[@class="channel-sons pull-left"]'
                           ),
             callback='parse_item',
             follow=True
             ),#list_8_897.html
        #下一页
        Rule(LinkExtractor(allow=r'https://www.ys137.com/zyys/.*?.html',
                           restrict_xpaths='//ul[@class="pagination"]'
                            ),
             callback='parse_item',
             follow=True
            ),
        Rule(LinkExtractor(#https://www.ys137.com/zyys/1814913.html
                            allow=r'https://www.ys137.com/zyys/.*?.html',
                            restrict_xpaths='//div[@class="arc-infos clearfix"]'
                        ),
            callback='parse_item_data',
            follow=True
            )
    )



    def parse_page_data(self,response):
        item = {}
        print('请求到了', response.status, response.url, )
        return item



    def parse_item(self, response):
        print('11111',response.url)
        web_lis = response.xpath('//div[@class="pull-left m-left article channel-articlelist"]/ul/li')
        print(len(web_lis))
        # print(web_lis)

        for info in web_lis:
            html_data = YangshengspiderItem()
            html_data['coverImage'] = info.xpath('.//div[@class="arc-infos clearfix"]/a/img/@src').extract_first()
            html_data['title'] = info.xpath('.//div[@class="arc-infos clearfix"]/h2/a/text()').extract_first()
            html_data['context'] = ' '.join(info.xpath('.//div[@class="arc-infos clearfix"]/p/text()').extract()).replace('\n','').replace('\t','')
            html_data['time_data'] = info.xpath('.//div[@class="arc-tags clearfix"]/span/text()').extract_first()
            #print(html_data)
            yield html_data

        # web_left = response.xpath('//div[@class="mybox-main"]')
        # #web_left_tow = response.xpath('//div[@class="clearfix"]')
        # html_text = YangshengSpidermongo_data()
        # # item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        # # item['name'] = response.xpath('//div[@id="name"]').get()
        # # item['description'] = response.xpath('//div[@id="description"]').get()
        # # 左侧内容
        # html_text['buzz'] = ';'.join(web_left.xpath('.//ul[1]/li/a/text()').extract())
        #
        # print(html_text)
        # yield html_text

    def parse_item_data(self,response):
        print('222222',response.url)
        web_div = response.xpath('//div[@class="pull-left m-left article"]')

        # print(len(web_div))
        # print(web_div)
        html_text = YangshengspiderItem_data()
        html_text['title'] =web_div.xpath('.//h1/text()').extract_first()
        html_text['source'] = web_div.xpath('.//div[@class="article-infos"]/span[1]/text()').extract_first()
        html_text['author']  = web_div.xpath('.//div[@class="article-infos"]/span[2]/text()').extract_first()
        html_text['context'] = ''.join(response.xpath('//div[@class="article-content"]/table/tr/td/p/text()').extract()).replace('\n','').replace('\t','') #+ info_one.xpath('.//div[@class="article-content"]/p/text()').extract()

        #print(html_text)
        yield html_text







