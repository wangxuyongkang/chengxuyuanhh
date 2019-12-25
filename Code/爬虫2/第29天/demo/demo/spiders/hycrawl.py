# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from demo.items import DemoItem


class HycrawlSpider(CrawlSpider):
    name = 'hycrawl'
    allowed_domains = ['hengyan.com']
    start_urls = ['http://top.hengyan.com/mianfei/default.aspx?p=1']

    #rules（列表或者元祖）:Rule对象，定制url的提取规则对象
    """
    Rule：
        LinkExtractor：根据正则规则或则xpath路径等寻找url地址
            allow:
                case1：为空的时候,提取页面中所有的URL地址
                case2: 设置一个正则表达式,只提取符合正则表达式的url地址
            deny:
                更allow相反，标示不允许提取的url地址
                设置一个正则表达式,不请求符合正则表达式的url地址
                deny优先级比allow要高
                
            allow_domains：设置允许爬取的域
            deny_domains：设置不允许爬取的域，deny_domains优先级比allow_domains高
            
            restrict_xpaths：设置xpath表达式路径，只提取xpath定位到的标签下的url地址
            restrict_css：设置css表达式路径，只提取css定位到的标签下的url地址
            
        callback：请求成功的回调函数
        follow:是否根据（是否需要在请求的响应结果中继续提取新的url地址）
        process_links:设置一个函数,拦截个过滤提取的url地址 
        process_request:设置一个函数,拦截个过滤提取Request请求对像 
    """

    rules = (
        #http://www.hengyan.com/book/4047.aspx
        Rule(
            LinkExtractor(
                allow=r'/book/\d+\.aspx',
                restrict_xpaths='//a[@class="bn"]'
            ),
            callback='parse_item',
            follow=True
        ),
        #http://www.hengyan.com/dir/6699.aspx
        Rule(
            LinkExtractor(
                allow=r'/dir/\d+\.aspx',
                restrict_xpaths='//a[@class="goml"]'
            ),
            follow=True
        ),

        #http://www.hengyan.com/article/230681.aspx
        Rule(
            LinkExtractor(
                allow=r'/article/\d+\.aspx',
            ),
            callback='parse_chpater_detail',
            follow=True,
        ),
        #http://top.hengyan.com/mianfei/default.aspx?p=2
        Rule(
            LinkExtractor(
                allow=r'/mianfei/default.aspx?p=\d+',
                restrict_xpaths='//p[@class="pager"]/a'
            ),
            follow=True
        )
    )

    def parse_start_url(self, response):
        """parse_start_url：接收起始url请求的响应结果"""
        pass

    def parse_item(self, response):
        """解析书籍详情"""
        print(response.url)
        # 取数据
        item = DemoItem()
        item['name'] = response.xpath('//h2/text()').extract_first('')
        item['point_nums'] = int(response.xpath('//p[@class="info"]/span[1]/text()').re('\d+')[0])
        item['category'] = response.xpath('//p[@class="info"]/span[2]/a/text()').extract_first('')
        item['size'] = int(response.xpath('//p[@class="info"]/span[3]/text()').re('\d+')[0])
        item['other'] = response.xpath('//p[@class="info"]/span[4]/text()').extract_first('')
        item['content'] = ''.join(response.xpath('//div[@class="des"]/p[2]/text()').extract())
        item['tags'] = response.xpath('//p[@class="biaoqian"]/label/text()').extract_first('')
        item['url'] = response.url
        item['book_image'] = response.css('div.huobg a img ::attr(src)').extract_first('')

        yield item

        #提取书籍章节列表的url地址
        # url = response.urljoin(response.xpath('//a[@class="goml"]/@href').extract_first())
        # yield scrapy.Request(
        #     url=url,
        #     callback=
        # )

    def parse_chpater_detail(self,response):
        print(response.url,'解析章节详情')