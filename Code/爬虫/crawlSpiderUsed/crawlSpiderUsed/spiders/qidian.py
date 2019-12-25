# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.link import Link


class QidianSpider(CrawlSpider):
    name = 'qidian'
    allowed_domains = ['qidian.com']
    start_urls = ['https://www.qidian.com/all']

    rules = (
        #https://www.qidian.com/all?orderId=&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0&page=2
        #https://www.qidian.com/all?orderId=&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0&page=3
        Rule(
            LinkExtractor(
                allow=r'.*?page=\d+',
                restrict_xpaths='//ul[@class="lbf-pagination-item-list"]'
            ),
            callback='parse_page_data',
            follow=True
        ),
        #提取书籍详情的url地址
        #https://book.qidian.com/info/1004174819
        Rule(
            LinkExtractor(
                allow=r'.*?info/\d+',
                restrict_xpaths='//ul[@class="all-img-list cf"]'
            ),
            callback='parse_noval_detail',
            follow=True,
            process_links= 'get_noval_detail_link'
        ),
        #注意继承自scrapy.spider的爬虫文件,设置回调都是self.函数名称,继承自CrawlSpider的爬虫文件,
        #设置回调函数,跟的是一个字符串,字符串是函数名称

        Rule(
            LinkExtractor(
            allow=r'',
            restrict_xpaths='//div[@class=""]'
            ),
            callback='parse_noval_detail'
        )
    )
    #rules:对应的是一个元组tuple或是一个list，里面可以有多个rule对象
    #Rule对象:设置要提取的连接规则，并且设定是否要更进
    #回调函数，拦截提取的url等操作

    """
    allow=(), :跟的是正则表达式(url的提取规则),如果是空字符串,表示提取所有url地址
    deny=(),  :(跟allow相反)跟的是正则表达式,将符合正则表达式的url地址过滤
    allow_domains=(), : 设置允许爬取的域
    deny_domains=(),  : (跟allow_domains相反)设置不允许爬取的域
    restrict_xpaths=(),: 设置xpath路径,只提取xpath路径对应节点下的url地址
    attrs=('href',),   : 可以设置要提取的标签属性(一般也不常用)
    unique=True,        :去除页面中重复的url地址,只保留一个
    restrict_css=(), :设置css语法只提取css选择的节点下的url地址
    strip=True  ： 去除空格 如果如果url地址中出现空格，会自动去除(只去除首和尾)
    """

    def parse_start_url(self, response):
        #parse_start_url 获取起始url相应结果
        # 提取分页列表中的书籍信息
        pass
    #注意: 切记不要使用parse方法 CrawlSpider内部实现了parse方法
    #如果在外面实现，会覆盖CrawlSpider内部的代码逻辑
    def parse_page_data(self, response):
        item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        print('分页数据请求成功',response.status,response.url)
        return item


    def get_noval_detail_link(self,links):
        for link in links:
            link.url = link.url+ '#Catalog'
        print(links)

        return links


    def parse_noval_detail(self,response):
        print('获取到了小说详情信息',response.url)
        with open('novaldetail.html','w') as file:
            file.write(response.text)

    def parse_noval_detail(self,response):
        """
        提取章节的url地址
        :param response:
        :return:
        """
        print('获取到了小说详情的信息',response.url)

        # 判断章节信息是否存在页面源码中
        article_div = response.xpath('//div[@class="volume"]')
        if len(article_div) > 0:
            print('章节信息在静态页面中')
        else:
            print('章节信息是加载的')
        # with open('novaldetail.html','w') as file:
        #     file.write(response.text)