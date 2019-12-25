# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request,Response
from demo.items import DemoItem
from scrapy_redis.spiders import RedisSpider
# class HengyanSpider(scrapy.Spider):
#第一步：修改继承的类
class HengyanSpider(RedisSpider):
    name = 'hengyan'
    # 设置允许爬取的域 (可以设置多个)
    allowed_domains = ['hengyan.com']
    # 设置起始url地址  (可以设置多个)
    # start_urls = ['http://top.hengyan.com/mianfei/default.aspx?p=1']

    #第二步:从redis数据库获取起始url地址
    redis_key = 'hengyan:start_urls'

    # def start_requests(self):
    # 如果起始任务是post请求，就必须重写这个方法，创建
    # post请求Request对象
    #     for url in self.start_urls:

            # get请求Request对象
            # yield scrapy.Request(
            #     url,
            #     dont_filter=True,
            #     callback=self.customer_parse
            # )

            #post请求Request对象
            # yield scrapy.FormRequest(
            #     url,
            #     dont_filter=True,
            #     formdata = {'name':'存放表单数据'},
            #     callback=self.customer_parse
            # )

    # def customer_parse(self, response):
    #     # 解析起始url的响应结果
    #     print(response.status,response.url)

    def parse(self, response):
        #解析起始url的响应结果
        # response(status,headers,body,url,request,meta,text)
        # print(response.status,response.url,response.text)
        # urls = response.xpath('//a[@class="bn"]/@href').extract()
        #urls:存放的是小说详情的url地址们
        urls = response.css('a.bn ::attr(href)').extract()
        print(urls)
        for url in urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse_detail,
                meta={'url':url}
            )

        #下一页们
        next_urls = response.xpath('//p[@class="pager"]//a/@href').extract()
        if next_urls:
            for url in next_urls:
                url = response.urljoin(url)
                yield scrapy.Request(
                    url=url,
                    callback=self.parse,
                    # cookies=
                )

    def parse_detail(self,response):
        """解析详情数据"""
        url = response.meta['url']
        #取数据
        item = DemoItem()
        item['name'] = response.xpath('//h2/text()').extract_first('')
        item['point_nums'] = int(response.xpath('//p[@class="info"]/span[1]/text()').re('\d+')[0])
        item['category']= response.xpath('//p[@class="info"]/span[2]/a/text()').extract_first('')
        item['size'] = int(response.xpath('//p[@class="info"]/span[3]/text()').re('\d+')[0])
        item['other'] = response.xpath('//p[@class="info"]/span[4]/text()').extract_first('')
        item['content'] = ''.join(response.xpath('//div[@class="des"]/p[2]/text()').extract())
        item['tags'] = response.xpath('//p[@class="biaoqian"]/label/text()').extract_first('')
        item['url'] = url
        item['book_image'] = response.css('div.huobg a img ::attr(src)').extract_first('')
        # print(item)

        yield item




