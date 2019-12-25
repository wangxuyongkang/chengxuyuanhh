# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Response
from Jobbole.items import JobboleItem

class JobboleSpider(scrapy.Spider):
    #爬虫文件的名称
    name = 'jobbole'
    #设置爬虫允许爬取的域，可以设置多个 （是一个list）
    allowed_domains = ['jobbole.com']
    #设置起始的url地址，可以设置多个（是一个list）
    start_urls = ['http://blog.jobbole.com/all-posts/']

    #parse,获取响应结果的回调方法
    def parse(self, response):
        """
        :param response: 请求的响应结果
        :return:
        """
        print('请求成功，获取到了页面源码')
        #获取响应的状态码
        code = response.status
        # # 获取响应的页面源码
        # html = response.text
        # 获取当前请求的url地址
        url = response.url
        #获取响应的二进制数据
        # b_html = response.body
        # #获取响应头
        # response_headers = response.headers
        # #获取当前请求的request对想
        # request = response.request
        # #获请求的请求头
        # request_headers = response.request.headers

        print(code, url)
        # 提取目标数据
        # 获取文章列表
        article_divs = response.xpath('//div[@class="post floated-thumb"]')

        print(len(article_divs))

        for article_div in article_divs:
            articleItem = JobboleItem()
            # title(标题)
            # title = article_div.xpath('.//a[@class="archive-title"]/text()').extract()[0]
            #extract_first():优势，如果没有取到返回 None，也可以自己设置一个默认值
            articleItem['title'] = article_div.xpath('.//a[@class="archive-title"]/text()').extract_first('')

            # title = article_div.css('a.archive-title ::text').extract_first('')
            # # 封面图
            articleItem['coverImage'] = article_div.xpath('.//div[@class="post-thumb"]/a/img/@src').extract_first('暂无')
            print(articleItem)

            #获取详情页面的url地址
            detailUrl = article_div.xpath('.//a[@class="archive-title"]/@href').extract_first()
            if detailUrl:
                #存在则发起请求
                """
                 url, :要请求的url地址
                 callback=None, 请求成功的回调函数
                 method='GET', 设置请求的方式
                 headers=None, 设置请求头,dict类型
                 cookies=None, 设置用户的cookies信息 dict类型
                 meta=None, 传递参数 dict类型
                 encoding='utf-8', （编码类型，一般不需要改变）
                 priority=0, （设置优先级，不需要改变）
                 dont_filter=False, （是否过滤url,False表示过滤，True：表示不过滤）
                 errback=None ,设置请求错误的回调函数
                """
                yield scrapy.Request(
                    detailUrl,
                    callback=self.parse_article_data,
                    meta={'item':articleItem}
                )

        #获取下一页url地址，继续发起请求
        # next_url = response.xpath('//a[@class="next page-numbers"]/@href').extract_first()
        # if next_url:
        #     yield scrapy.Request(next_url,callback=self.parse)

    def parse_article_data(self,response):
        """
        文章详情，请求成功够的回调
        :param response:
        :return:
        """
        print(response.status,'文章详情获取成功')
        #取出meta传递过来的值
        articleItem = response.meta['item']

        # # source（来源）
        articleItem['source'] = response.xpath('//div[@class="copyright-area"]/a[1]/text()').extract_first('暂无出处')
        # # 内容
        # articleItem['content'] = ';'.join(response.xpath('//div[@class="entry"]//p/text()').extract())
        # # 点赞量
        articleItem['zanNum'] = int(response.xpath('//span[@class=" btn-bluet-bigger href-style vote-post-up   register-user-only "]/h10/text()').extract_first('0'))
        # # 评论量
        # commentNum = scrapy.Field()
        # # 收藏
        # markNum = scrapy.Field()
        # # 发布时间
        publishTime = ','.join(response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract()).replace(' ','').replace('\n','').replace('\r','')

        #注意这里使用的是yield
        #激活管道，只有激活了，管道文件才能接收到item
        yield articleItem
        # print(articleItem)








