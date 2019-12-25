# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from qidian.items import QidianNovalItem,QidianChpaterItem
scrapy.FormRequest
class QdSpider(CrawlSpider):
    name = 'qd'
    allowed_domains = ['qidian.com']
    start_urls = ['https://www.qidian.com/all?orderId=&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0&page=1']

    rules = (
        Rule(
            LinkExtractor(allow=r'.*?page=\d+',restrict_xpaths='//ul[@class="lbf-pagination-item-list"]'),
            callback='parse_item',
            follow=True
        ),
        #详情的url地址
        #http://book.qidian.com/info/1010734492
        Rule(
            LinkExtractor(allow=r'.*?/info/\d+',restrict_xpaths='//div[@class="book-mid-info"]'),
            callback='parse_noval_detail',
            follow=True,
            process_links='check_noval_link'
        ),
        #章节详情地址：
        # https://read.qidian.com/chapter/ORlSeSgZ6E_MQzCecGvf7A2/atYOCLHSg35Ms5iq0oQwLQ2
        # https://vipreader.qidian.com/chapter/1010734492/397543156
        Rule(
            LinkExtractor(allow=r'//read.qidian.com/chapter/.*?',restrict_xpaths='//div[@class="volume"]'),
            callback='parse_chpater_detail',
            follow=True
        )
    )

    def parse_start_url(self, response):
        """起始url请求完成后的回调方法"""
        pass

    def parse_item(self, response):
        """
        找到小说的列表,提取每一本小说的内容
        :param response:
        :return:
        """
        #小说列表
        noval_list = response.xpath('//ul[@class="all-img-list cf"]/li')
        print(len(noval_list))

        if len(noval_list) > 0:
            for noval_li in noval_list:
                noval_item = QidianNovalItem()
                # 封面图片
                noval_item['coverImage'] = noval_li.xpath('.//div[@class="book-img-box"]/a[1]/img/@src').extract_first('')
                # 小说名称
                noval_item['novalTitle'] = noval_li.xpath('.//div[@class="book-mid-info"]/h4/a/text()').extract_first('')
                # 作者
                noval_item['author'] = noval_li.xpath('.//div[@class="book-mid-info"]//a[@class="name"]/text()').extract_first('')
                # 分类
                noval_item['category'] = '|'.join(noval_li.xpath('.//p[@class="author"]/a/text()')[1:].extract())
                # 连载状态
                noval_item['status'] = noval_li.xpath('//p[@class="author"]/span/text()').extract_first('')
                # 简介
                noval_item['content'] = ''.join(noval_li.xpath('.//p[@class="intro"]/text()').extract()).replace('\r','').replace(' ','')

                print(noval_item)

                #将数据yield交给管道
                yield noval_item


    def check_noval_link(self,links):
        """
        正在这里做url的过滤和拦截
        :param links:
        :return:
        """
        #links得到的是一个list,里面存放的都是Link对象
        change_links = []
        for link in links:
            # url,text
            link.url = link.url+'#Catalog'
            change_links.append(link)

        return change_links


    def parse_noval_detail(self,response):
        print('小说倾向获取成功')
        pass

    def parse_chpater_detail(self,response):
        print('获取到了章节详情内容',response.status)
        #在这里解析章节详情的数据

        chpater_item = QidianChpaterItem()

        # 小说的标题
        chpater_item['novalTitle'] = response.xpath('//div[@class="info fl"]/a/text()').extract_first('')
        # 章节的标题
        chpater_item['chpaterTitle'] = response.xpath('//h3[@class="j_chapterName"]/text()').extract_first('')
        # 章节的字数
        chpater_item['chpaterSize'] = response.xpath('//span[@class="j_chapterWordCut"]/text()').extract_first('')
        # 章节的内容
        chpater_item['chpaterContent'] = ''.join(response.xpath('//div[@class="read-content j_readContent"]//p/text()').extract()).replace(' ','').replace('\n','').replace('\u3000','')
        # 发布时间
        chpater_item['publishTime'] = response.xpath('//span[@class="j_updateTime"]/text()').extract_first('').replace('\u3000','')

        print(chpater_item)

        yield chpater_item

