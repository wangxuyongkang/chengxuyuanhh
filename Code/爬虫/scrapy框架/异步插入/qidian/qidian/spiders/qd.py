# -*- coding: utf-8 -*-
import scrapy,re,json
from qidian.items import QidianNovalItem,QidianChpaterItem

class QdSpider(scrapy.Spider):
    name = 'qd'
    allowed_domains = ['qidian.com']
    start_urls = ['https://www.qidian.com/all']

    def parse(self, response):
        """
        获取当前页书籍的列表，遍历
        :param response:
        :return:
        """
        noval_lis = response.xpath('//ul[@class="all-img-list cf"]/li')
        #noval_lis = response.css('ul.all-img-list.cf > li')

        for noval_li in noval_lis:
            novalItem = QidianNovalItem()
            # 封面
            novalItem['coverImage'] = 'https:' + noval_li.xpath('.//div[@class="book-img-box"]//img/@src').extract_first('')
            novalItem['coverImage'] = 'https:' + noval_li.css('div.book-img-box img ::attr(src)').extract_first('')
            # 标题
            # title = scrapy.Field()
            novalItem['title'] = noval_li.xpath('.//div[@class="book-mid-info"]/h4/a/text()').extract_first('')
            novalItem['title'] = noval_li.css('div.book-mid-info > h4 > a ::text').extract_first('')
            # # 作者
            # novalItem['author'] = noval_li.xpath('.//p[@class="author"]/a[@class="name"]/text()').extract_first('')
            # novalItem['author'] = noval_li.css('p.author a')[0].css('::text').extract_first('')
            #css 语法的语法规则   a:nth-of-type(n)：取父节点下第n个a节点
            novalItem['author'] = noval_li.css('p.author > a:nth-of-type(1) ::text').extract_first('')
            # # 分类
            # category = scrapy.Field()
            # # 状态
            # status = scrapy.Field()
            # # 简介
            # content = scrapy.Field()

            #获取小说的详情地址（带章节的详情地址）
            #https://book.qidian.com/info/1004608738#Catalog
            detailUrl = 'https:' + noval_li.xpath('.//div[@class="book-mid-info"]/h4/a/@href').extract_first('')+'#Catalog'

            #将书籍信息交给管道
            yield novalItem

            # #get请求
            # scrapy.Request()
            yield scrapy.Request(url=detailUrl,callback=self.parse_noval_detail)
            # #post请求
            # scrapy.FormRequest()

        #获取其他分页的url地址
        otehr_pages = response.xpath('//ul[@class="lbf-pagination-item-list"]/li/a/@href').extract()
        if otehr_pages:
            for pageUrl in otehr_pages:
                pageUrl = 'https:'+pageUrl
                yield scrapy.Request(url=pageUrl,callback=self.parse)

    def parse_noval_detail(self,response):
        """
        获取书籍详情信息，提取章节信息
        :param response:
        :return:
        """

        # 静态页面中包含章节信息（列表）
        # 动态加载章节信息（列表）
        #https://book.qidian.com/ajax/book/category?_csrfToken=2gp4AK8vxs2iNULVAXkBcJViBeLv0VdX4rYyKpG7&bookId=1004608738

        #提取章节目录
        div_volume = response.xpath('.//div[@class="volume"]')

        if len(div_volume) > 0:
            print('说明是静态页面')
            for div in div_volume:
                isFree = div.xpath('./h3/span/text()').extract_first('').replace(' ', '')
                if '免费' in isFree:
                    #print('这个div存放的免费章节')
                    chpater_lis = div.xpath('./ul[@class="cf"]/li')
                    for chpater_li in chpater_lis:
                        chpater_url = 'https:' + chpater_li.xpath('./a/@href').extract_first('')
                        # print('静态页面中，章节详情地址',chpater_url)
                        yield scrapy.Request(url=chpater_url,callback=self.parse_chpater_detail)
        else:
            print('当前小说章节目录是动态加载的')

            #https://book.qidian.com/ajax/book/category?
            #_csrfToken=2gp4AK8vxs2iNULVAXkBcJViBeLv0VdX4rYyKpG7
            #&bookId=1004608738

            #https://book.qidian.com/ajax/book/category?
            # _csrfToken=2gp4AK8vxs2iNULVAXkBcJViBeLv0VdX4rYyKpG7
            # &bookId=1004179514

            #获取bookId
            #https://book.qidian.com/info/1004608738#Catalog
            pattern = re.compile(r'\d+')
            bookId = re.search(pattern,response.url).group()

            url = 'https://book.qidian.com/ajax/book/category?_csrfToken=2gp4AK8vxs2iNULVAXkBcJViBeLv0VdX4rYyKpG7&bookId='+bookId
            # cookie = "_csrfToken=2gp4AK8vxs2iNULVAXkBcJViBeLv0VdX4rYyKpG7; newstatisticUUID=1550490569_122198083; qdrs=0%7C3%7C0%7C0%7C1; qdgd=1; lrbc=1011705052%7C406214100%7C0%2C1011335417%7C401796640%7C0%2C1004608738%7C339991957%7C0; rcr=1011705052%2C1011335417%2C1010734492%2C1004608738; e1=%7B%22pid%22%3A%22qd_P_all%22%2C%22eid%22%3A%22qd_B58%22%2C%22l1%22%3A5%7D; e2=%7B%22pid%22%3A%22qd_P_all%22%2C%22eid%22%3A%22qd_B58%22%2C%22l1%22%3A5%7D"
            # cookies_dict = {i.split('=')[0]:i.split('=')[1] for i in cookie.split('; ')}
            yield scrapy.Request(url=url,callback=self.parse_dynamic_chpater)

    def parse_dynamic_chpater(self,response):
        """
        解析动态加载的章节
        :param response:
        :return:
        """
        # print('11111111', response.text)
        # print('11111111', response.request.headers)
        chpater_vc = json.loads(response.text)['data']['vs']
        for item in chpater_vc:
            #item['vS'] == 0 说明是免费章节
            if item['vS'] == 0:
                chpater_list = item['cs']
                for chpater in chpater_list:
                    #https://read.qidian.com/chapter/
                    #_AaqI-dPJJ4uTkiRw_sFYA2/-Yjl2ADCXQvM5j8_3RRvhw2
                    #https://read.qidian.com/chapter/
                    #_AaqI-dPJJ4uTkiRw_sFYA2/Ul9I2kl_ETy2uJcMpdsVgA2
                    #https://read.qidian.com/chapter/
                    #-D24smocjMtcXB4XKBaZpQ2/KScsxqhD3KxMs5iq0oQwLQ2
                    chpaterUrl = 'https://read.qidian.com/chapter/'+chpater['cU']

                    yield scrapy.Request(url=chpaterUrl,callback=self.parse_chpater_detail)



    def parse_chpater_detail(self,response):
        """
        获取小说章节页面源码，提取目标数据
        :param response:
        :return:
        """

        chpaterItem = QidianChpaterItem()

        # 章节名称
        chpaterItem['chpaterName'] = response.xpath('//h3[@class="j_chapterName"]/text()').extract_first('')
        # 书籍名称
        chpaterItem['novalName'] = response.xpath('//div[@class="info fl"]/a[1]/text()').extract_first('')
        # 内容
        chpaterItem['content'] = ''.join(response.xpath('//div[@class="read-content j_readContent"]//p/text()').extract())
        # chpaterItem['content'] = ''.join(response.xpath('//div[@class="read-content j_readContent"]//text()').extract())
        # # 作者
        # chpaterItem['author'] = scrapy.Field()
        # # 字数
        # chpaterItem['sizeNum'] = scrapy.Field()
        # # 发布时间
        # chpaterItem['publishTime'] = scrapy.Field()

        yield chpaterItem

