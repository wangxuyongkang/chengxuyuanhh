# -*- coding: utf-8 -*-
import scrapy
import re
import json
from qidian.items import QidianNovalItem , qidianItem

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
            novalItem['author'] = noval_li.xpath('.//p[@class="author"]//a[1]/text()').extract_first('')
            novalItem['author'] = noval_li.css('p.author > a')[0].css("::text").extract_first('')
            #css语法规则 a::nth-of-type(n) ::text 第n个的text文本
            #novalItem['author'] = noval_li.css('p.author > a:nth-of-type(1) ::text').extract_first('')
            # # 分类
            novalItem['category'] = noval_li.xpath('.//p[@class="author"]//a[2]/text()').extract_first('')+ '|' + noval_li.xpath('.//p[@class="author"]//a[3]/text()').extract_first('')
            novalItem['category'] = noval_li.css('p.author > a')[1].css("::text").extract_first('') + '|' +  noval_li.css('p.author > a')[2].css("::text").extract_first('')
            # # 状态
            novalItem['status_a'] = noval_li.xpath('.//p[@class="author"]//span/text()').extract_first('')
            novalItem['status_a'] = noval_li.css('p.author > span ::text').extract_first('')
            # # 简介
            novalItem['content'] = noval_li.xpath('.//p[@class="intro"]/text()').extract_first('').replace('\r','').replace(' ','')
            novalItem['content'] = noval_li.css('p.intro ::text').extract_first('').replace('\r','').replace(' ','')

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

            print(novalItem)

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
            print('说明是静态')
            for div in div_volume:
                isFree = div.xpath('./h3/span/text()').extract_first('').replace(' ', '')
                if '免费' in isFree:
                    # print('这个div存放的免费章节')
                    chpater_lis = div.xpath('./ul[@class="cf"]/li')
                    for chpater_li in chpater_lis:
                        chpater_url = 'https:' + chpater_li.xpath('./a/@href').extract_first('')
                        # print('静态页面中，章节详情地址',chpater_url)
                        yield scrapy.Request(url=chpater_url, callback=self.parse_chpater_detail)
        else:
            print('当前小说章节目录是动态加载的')
            pattern = re.compile(r'\d+')
            bookId = re.search(pattern, response.url).group()

            # url = 'https://book.qidian.com/ajax/book/category?_csrfToken=2gp4AK8vxs2iNULVAXkBcJViBeLv0VdX4rYyKpG7&bookId=' + bookId
            url = 'https://book.qidian.com/ajax/book/category?_csrfToken=wCRI378vqG9PyaLPev8snTwdojD8gi1Bz19UKNmx&bookId=' + bookId
            print(url)
            yield scrapy.Request(url=url, callback=self.parse_dynamic_chpater)

    def parse_dynamic_chpater(self,response):
        #print(response.text)
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
        #提取目标数据

        info = qidianItem()
        # 标题
        info['title'] = response.xpath('//h3[@class="j_chapterName"]/text()').extract_first('')
        # 作者
        info['author'] = response.xpath('//div[@class="info fl"]/a[1]/text()').extract_first('')
        # 内容
        info['context'] = ''.join(response.xpath('.//div[@class="read-content j_readContent"]//p/text()').extract()).replace('\u3000','').replace('\n','').replace(' ','')
        yield info