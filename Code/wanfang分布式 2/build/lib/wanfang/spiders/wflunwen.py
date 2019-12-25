# -*- coding: utf-8 -*-
import scrapy
from wanfang.items import WanfangPerioItem,WanfangDegreeItem,WanfangConferenceItem,WanfangTechItem
import re
from urllib import parse
import json
from scrapy_redis.spiders import RedisSpider


# class WflunwenSpider(scrapy.Spider):
class WflunwenSpider(RedisSpider):
    name = 'wflunwen'
    allowed_domains = ['wanfangdata.com.cn']
    """
    http://g.wanfangdata.com.cn/search/searchList.do?searchType=perio&showType=&pageSize=&searchWord=%E6%B3%95%E5%BE%8B&isTriggerTag=
    http://g.wanfangdata.com.cn/search/searchList.do?beetlansyId=aysnsearch&searchType=perio&pageSize=20&page=2&searchWord=%E6%B3%95%E5%BE%8B&order=correlation&showType=detail&isCheck=check&isHit=&isHitUnit=&firstAuthor=false&rangeParame=&navSearchType=perio
    """
    # start_urls = [
    #     'http://www.wanfangdata.com.cn/search/searchList.do?beetlansyId=aysnsearch&searchType=degree&pageSize=50&page=1&searchWord=%E6%B3%95%E5%BE%8B&order=correlation&showType=detail&isCheck=check&isHit=&isHitUnit=&firstAuthor=false&rangeParame=&navSearchType=degree',
    #     'http://www.wanfangdata.com.cn/search/searchList.do?beetlansyId=aysnsearch&searchType=degree&pageSize=50&page=1&searchWord=%E6%94%BF%E6%B2%BB&order=correlation&showType=detail&isCheck=check&isHit=&isHitUnit=&firstAuthor=false&rangeParame=&navSearchType=degree',
    #     'http://www.wanfangdata.com.cn/search/searchList.do?beetlansyId=aysnsearch&searchType=perio&pageSize=50&page=1&searchWord=%E6%94%BF%E6%B2%BB&order=correlation&showType=detail&isCheck=check&isHit=&isHitUnit=&firstAuthor=false&rangeParame=&navSearchType=perio',
    #     'http://www.wanfangdata.com.cn/search/searchList.do?beetlansyId=aysnsearch&searchType=perio&pageSize=50&page=1&searchWord=%E6%B3%95%E5%BE%8B&order=correlation&showType=detail&isCheck=check&isHit=&isHitUnit=&firstAuthor=false&rangeParame=&navSearchType=perio',
    #     'http://www.wanfangdata.com.cn/search/searchList.do?beetlansyId=aysnsearch&searchType=conference&pageSize=50&page=1&searchWord=%E6%B3%95%E5%BE%8B&order=correlation&showType=detail&isCheck=check&isHit=&isHitUnit=&firstAuthor=false&rangeParame=&navSearchType=conference',
    #     'http://www.wanfangdata.com.cn/search/searchList.do?beetlansyId=aysnsearch&searchType=conference&pageSize=50&page=1&searchWord=%E6%94%BF%E6%B2%BB&order=correlation&showType=detail&isCheck=check&isHit=&isHitUnit=&firstAuthor=false&rangeParame=&navSearchType=conference',
    #     'http://www.wanfangdata.com.cn/search/searchList.do?beetlansyId=aysnsearch&searchType=tech&pageSize=50&page=1&searchWord=%E6%B3%95%E5%BE%8B&order=correlation&showType=detail&isCheck=check&isHit=&isHitUnit=&firstAuthor=false&rangeParame=&navSearchType=tech',
    #     'http://www.wanfangdata.com.cn/search/searchList.do?beetlansyId=aysnsearch&searchType=tech&pageSize=50&page=1&searchWord=%E6%94%BF%E6%B2%BB&order=correlation&showType=detail&isCheck=check&isHit=&isHitUnit=&firstAuthor=false&rangeParame=&navSearchType=tech',
    # ]
    redis_key = 'wflunwen:start_urls'


    def parse(self, response):
        # 获取当前请求搜索的关键字
        pattern = re.compile('.*?searchWord=(.*?)&', re.S)
        searchKeyWord = re.findall(pattern, response.url)[0]
        searchKeyWord = parse.unquote(searchKeyWord)
        # 获取当前请求搜素的分类
        pattern = re.compile('.*?searchType=(.*?)&', re.S)
        searchType = re.findall(pattern, response.url)[0]

        totalRow = int(response.xpath('.//input[@id="totalRow"]/@value').extract_first(''))

        if totalRow > 5000:
            #获取到的第一页数据总数量大于5000的时候
            """
            searchType: degree
            searchWord: (%E6%94%BF%E6%B2%BB)（政治）
            facetField: 
            isHit: 
            startYear: 
            endYear: 
            offset: 0
            limit: 6
            hqfwfacetField: 
            navSearchType: 
            """
            print(searchKeyWord, searchType, '数据量', totalRow,'大于5000')
            form_data = {
                'searchType': searchType,
                'searchWord': '('+parse.quote(searchKeyWord)+')',
                'facetField':'',
                'isHit':'',
                'startYear':'',
                'endYear':'',
                'offset': '0',
                'limit': '20',
                'hqfwfacetField':'',
                'navSearchType':'',
            }

            yield scrapy.FormRequest(url='http://g.wanfangdata.com.cn/search/navigation.do',formdata=form_data,
                                     callback=self.parse_navigation_data,meta={'baseUrl':response.url,'searchType':form_data['searchType'],'searchKeyWord':searchKeyWord},
                                     dont_filter=True
                                     )

            yield scrapy.Request(url=response.url, callback=self.parse_pagelist_data, dont_filter=True)

        else:

            print(searchKeyWord, searchType, '数据量', totalRow, '小于5000')
            yield scrapy.Request(url=response.url,callback=self.parse_pagelist_data,dont_filter=True)

    def parse_navigation_data(self,response):
        print('导航栏数据获取成功', response.meta['searchType'], response.meta['searchKeyWord'])
        # print('导航栏数据获取成功',response.meta['searchType'],response.meta['searchKeyWord'],response.text)
        data = json.loads(response.text)
        base_url = response.meta['baseUrl']
        for sub_dict in data['facetTree']:
            if sub_dict['pId'] != '-1':
                print(sub_dict)
                if sub_dict['facetField'] == '$common_year':
                    # &facetField=$common_year:2018&facetName=2018:$common_year
                    full_url = base_url + '&facetField=%s&facetName=%s' % (sub_dict['facetField']+':'+sub_dict['value'],sub_dict['value']+':'+sub_dict['facetField'])
                    # print(full_url)
                    yield scrapy.Request(url=full_url, callback=self.parse_pagelist_data)

                elif sub_dict['facetField'] == '$subject_classcode_level':
                    # &facetField=$subject_classcode_level:%E2%88%B7/D&facetName=%E6%94%BF%E6%B2%BB%E3%80%81%E6%B3%95%E5%BE%8B:$subject_classcode_level
                    # &facetField=$subject_classcode_level:∷/D&facetName=政治、法律:$subject_classcode_level
                    full_url = base_url + '&facetField=%s&facetName=%s' % (sub_dict['facetField']+':'+'%E2%88%B7'+'/'+sub_dict['value'],parse.quote(sub_dict['showName'])+':'+sub_dict['facetField'])
                    # print(full_url)
                    yield scrapy.Request(url=full_url, callback=self.parse_pagelist_data)

                elif sub_dict['facetField'] == '$degree_level':
                    """
                    &facetField=$degree_level:%E7%A1%95%E5%A3%AB&facetName=%E7%A1%95%E5%A3%AB:$degree_level
                    &facetField=$degree_level:硕士&facetName=硕士:$degree_level
                    """
                    full_url = base_url + '&facetField=%s&facetName=%s' % (sub_dict['facetField']+':'+parse.quote(sub_dict['value']),parse.quote(sub_dict['value'])+':'+sub_dict['facetField'])
                    # print(full_url)
                    yield scrapy.Request(url=full_url, callback=self.parse_pagelist_data)

                elif sub_dict['facetField'] == '$language':
                    """
                    &facetField=$language:chi&facetName=%E4%B8%AD%E6%96%87:$language
                    &facetField=$language:chi&facetName=中文:$language
                    """
                    full_url = base_url + '&facetField=%s&facetName=%s' % (sub_dict['facetField']+':'+sub_dict['value'],parse.quote(sub_dict['showName'])+':'+sub_dict['facetField'])
                    # print(full_url)
                    yield scrapy.Request(url=full_url, callback=self.parse_pagelist_data)

                elif sub_dict['facetField'] == '$tutor_name':
                    """
                    &facetField=$tutor_name:%E8%83%A1%E9%B8%BF%E9%AB%98&facetName=%E8%83%A1%E9%B8%BF%E9%AB%98:$tutor_name
                    &facetField=$tutor_name:胡鸿高&facetName=胡鸿高:$tutor_name
                    """
                    full_url = base_url + '&facetField=%s&facetName=%s' % (sub_dict['facetField']+':'+parse.quote(sub_dict['showName']),parse.quote(sub_dict['showName'])+':'+sub_dict['facetField'])
                    # print(full_url)
                    yield scrapy.Request(url=full_url, callback=self.parse_pagelist_data)


    def parse_pagelist_data(self,response):

        print('列表数据请求的状态码:', response.status)
        # 获取论文列表
        #thesis = response.xpath('//div[@class="ResultList"]/div[@class="ResultCont"]/div[@class="title"]')
        thesis = response.xpath('//div[contains(@class,"ResultList")]/div[@class="ResultCont"]/div[@class="title"]')

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
            "Referer": response.url,
        }
        # 获取当前请求搜索的关键字
        pattern = re.compile('.*?searchWord=(.*?)&', re.S)
        searchKeyWord = re.findall(pattern, response.url)[0]
        searchKeyWord = parse.unquote(searchKeyWord)
        # 获取当前请求搜素的分类
        pattern = re.compile('.*?searchType=(.*?)&', re.S)
        searchType = re.findall(pattern, response.url)[0]
        print(searchKeyWord, searchType)

        info = {
            'searchKeyWord': searchKeyWord,
            'searchType': searchType,
        }

        if len(thesis) > 0:
            print('获取到了' + str(len(thesis)) + '条数据', info)
            # 便利循环论文列表获取详情链接
            for article in thesis:
                # print(article)
                title = ''.join(article.xpath('./a[1]//text()').extract())
                # http://www.wanfangdata.com.cn/details/detail.do?_type=standards&id=T/OVMA%20024-2018
                detail_url = response.urljoin(article.xpath('./a[1]/@href').extract_first(''))
                if '目录' in title.replace(' ', '') and 'javascript:void(0)' in detail_url:
                    title = ''.join(article.xpath('./a[2]//text()').extract())
                    detail_url = response.urljoin(article.xpath('./a[2]/@href').extract_first(''))
                yield scrapy.Request(url=detail_url, headers=headers, callback=self.parse_detail_data,
                                     meta={'info': info, 'title': title})

            # 提取下一页分页地址
            cur_page_num = int(response.xpath('.//input[@id="pageNum"]/@value').extract_first(''))
            pageTotal = int(response.xpath('.//input[@id="pageTotal"]/@value').extract_first(''))
            if cur_page_num <= pageTotal:
                next_page_num = cur_page_num + 1
                pattern = re.compile('page=\d+', re.S)
                next_url = re.sub(pattern, 'page=' + str(next_page_num), response.url)
                print('第' + str(next_page_num) + '页', next_url)

                """
                对比分页的链接，寻找规律
                http://g.wanfangdata.com.cn/search/searchList.do?beetlansyId=aysnsearch&searchType=perio&pageSize=20&page=4&searchWord=%E6%B3%95%E5%BE%8B
                &order=correlation&showType=detail&isCheck=check&isHit=&isHitUnit=&firstAuthor=false&rangeParame=&navSearchType=perio

                http://g.wanfangdata.com.cn/search/searchList.do?beetlansyId=aysnsearch&searchType=perio&pageSize=20&page=2&searchWord=%E6%B3%95%E5%BE%8B
                &order=correlation&showType=detail&isCheck=check&isHit=&isHitUnit=&firstAuthor=false&rangeParame=&navSearchType=perio
                """
                yield scrapy.Request(url=next_url, headers=headers, callback=self.parse_pagelist_data)
            else:
                print(info, '分页数据加载完毕')
        else:
            print('当前页面获取数据失败')
            print(response.url)


    def parse_detail_data(self, response):

        info = response.meta['info']
        print('详情请求状态码', response.meta['title'], info, response.status,)
        if info['searchType'] == 'degree':
            print('正在获取学位分类论文信息')
            item = self.parse_degree(response, info)
            yield item
        elif info['searchType'] == 'perio':
            print('正在获取期刊分类论文信息')
            item = self.parse_perio(response, info)
            yield item
        elif info['searchType'] == 'conference':
            print('正在获取会议分类论文信息')
            item = self.parse_conference(response, info)
            yield item
        elif info['searchType'] == 'tech':
            print('正在获取科技报告分类论文信息')
            item = self.parse_tech(response, info)
            yield item

    def parse_degree(self, response, info):
        item = WanfangDegreeItem()
        item['url'] = response.url
        # title(中文标题)
        item['title'] = ''.join(response.xpath('//div[@class="title"]/text()').extract()).replace('\r\n', '').replace(
            '\t', '').replace('目录', '').replace(' ', '')
        # keywords(关键词)
        item['keywords'] = ';'.join(response.xpath('//ul[@class="info"]/li[1]//a/text()').extract())
        # authors(作者)
        item['authors'] = response.xpath('//ul[@class="info"]/li[2]//a[1]/text()').extract_first('')
        # 学位授权单位
        item['degreeUnit'] = response.xpath('//ul[@class="info"]/li[3]//a[1]/text()').extract_first('')
        # 授予学位
        item['awardedTheDegree'] = response.xpath(
            '//ul[@class="info"]/li[4]/div[@class="info_right author"]/text()').extract_first('')
        # 学科专业
        item['professional'] = response.xpath('//ul[@class="info"]/li[5]//a[1]/text()').extract_first('')
        # 导师姓名
        item['mentorName'] = response.xpath('//ul[@class="info"]/li[6]//a[1]/text()').extract_first('')
        # 学位年度
        item['degreeInAnnual'] = response.xpath('//ul[@class="info"]/li[7]/div[2]/text()').extract_first('')
        # 语种
        item['languages'] = response.xpath('//ul[@class="info"]/li[8]/div[2]/text()').extract_first('').replace('\r\n',
                                                                                                                '').replace(
            '\t', '')
        if response.xpath('//ul[@class="info"]/li[9]/div[@class="info_left"]/text()').extract_first('') == "分类号：":
            # 分类号
            item['classNumber'] = ''.join(response.xpath('//ul[@class="info"]/li[9]/div[2]/text()').extract()).replace(
                '\r\n', '').replace('\t', '')
            # 在线出版日期
            item['publishTime'] = response.xpath('//ul[@class="info"]/li[10]/div[2]/text()').extract_first('').replace(
                '\r\n', '').replace('\t', '').replace(' ', '')
        elif response.xpath('//ul[@class="info"]/li[9]/div[@class="info_left"]/text()').extract_first('') == "在线出版日期：":
            # 分类号
            item['classNumber'] = ''
            # 在线出版日期
            item['publishTime'] = response.xpath('//ul[@class="info"]/li[9]/div[2]/text()').extract_first('').replace(
                '\r\n', '').replace('\t', '').replace(' ', '')
        # print(item)

        item['searchKey'] = info['searchKeyWord']
        item['searchType'] = info['searchType']

        return item

    def parse_perio(self, response, info):
        item = WanfangPerioItem()
        item['url'] = response.url
        # title(中文标题)
        item['title'] = response.xpath('//div[@class="title"]/text()').extract_first('').replace('\r\n', '').replace(
            ' ', '').replace('\t', '')
        # englishTitle(英文标题)
        item['englishTitle'] = response.xpath('//div[@class="English"]/text()').extract_first('暂无').replace('\t', '')
        # content(摘要)
        item['content'] = response.xpath('//input[@class="share_summary"]/@value').extract_first('').replace('\t',
                                                                                                             '').replace(
            ' ', '').replace('\r\n', '')

        lis = response.xpath('//ul[@class="info"]//li')
        print(len(lis))
        for li in lis:
            # print(li.xpath('./div[@class="info_left"]/text()').extract_first(''))
            if li.xpath('./div[@class="info_left"]/text()').extract_first('') == "doi：":
                item['doi'] = li.xpath('.//a/text()').extract_first('').replace('\t', '').replace(' ', '')
            elif li.xpath('./div[@class="info_left"]/text()').extract_first('') == "关键词：":
                # keywords(关键词)
                item['keywords'] = '、'.join(li.xpath('.//a/text()').extract())
            elif li.xpath('./div[@class="info_left"]/text()').extract_first('') == "Keyword：":
                item['englishKeyWords'] = '、'.join(li.xpath('.//a/text()').extract())
            elif li.xpath('./div[@class="info_left"]/text()').extract_first('') == "作者：":
                item['authors'] = '、'.join(li.xpath('.//a/text()').extract())
            elif li.xpath('./div[@class="info_left"]/text()').extract_first('') == "Author：":
                item['englishAuthors'] = '、'.join(li.xpath('.//a/text()').extract()).replace('\n', '')
            elif li.xpath('./div[@class="info_left"]/text()').extract_first('') == "作者单位：":
                item['unit'] = '、'.join(li.xpath('.//a/text()').extract())
            elif li.xpath('./div[@class="info_left"]/text()').extract_first('') == "刊名：":
                item['journalName'] = li.xpath('.//a[@class="college"]/text()').extract_first('')
            elif li.xpath('./div[@class="info_left"]/text()').extract_first('') == "Journal：":
                item['journal'] = li.xpath('.//a[1]/text()').extract_first('')
            elif li.xpath('./div[@class="info_left"]/text()').extract_first('') == "年，卷(期)：":
                item['yearsInfo'] = li.xpath('.//a/text()').extract_first('')
            elif li.xpath('./div[@class="info_left"]/text()').extract_first('') == "所属期刊栏目：":
                item['journalSection'] = li.xpath('.//a/text()').extract_first('')
            elif li.xpath('./div[@class="info_left"]/text()').extract_first('') == "分类号：":
                item['classNumber'] = li.xpath('.//div[2]/text()').extract_first('').replace('\r', '').replace('\n',
                                                                                                               '').replace(
                    '\t', '')
            elif li.xpath('./div[@class="info_left"]/text()').extract_first('') == "基金项目：":
                item['fundProgram'] = li.xpath('.//a[1]/text()').extract_first('')
            elif li.xpath('./div[@class="info_left"]/text()').extract_first('') == "在线出版日期：":
                item['publishTime'] = li.xpath('.//div[2]/text()').extract_first('').replace('\r\n', '').replace(' ',
                                                                                                                 '').replace(
                    '\t', '')
            elif li.xpath('./div[@class="info_left"]/text()').extract_first('') == "页数：":
                item['pages'] = li.xpath('.//div[2]/text()').extract_first('')
            elif li.xpath('./div[@class="info_left"]/text()').extract_first('') == "页码：":
                item['pageNumber'] = li.xpath('.//div[2]/text()').extract_first('')

        item['searchKey'] = info['searchKeyWord']
        item['searchType'] = info['searchType']
        return item

    def parse_conference(self, response, info):

        item = WanfangConferenceItem()
        item['url'] = response.url
        # title(中文标题)
        item['title'] = ''.join(response.xpath('//div[@class="title"]/text()').extract()).replace('\r\n', '').replace(
            '\t', '').replace('目录', '').replace(' ', '')
        # content(摘要)
        item['content'] = response.xpath('//input[@class="share_summary"]/@value').extract_first('').replace('\t',
                                                                                                             '').replace(
            ' ', '').replace('\r\n', '').replace('\u3000', '')

        lis = response.xpath('//ul[@class="info"]//li')
        print(len(lis))
        for li in lis:
            if li.xpath('./div[@class="info_left"]/text()').extract_first('') == "关键词：":
                # keywords(关键词)
                item['keywords'] = '、'.join(li.xpath('.//a/text()').extract())
            elif li.xpath('./div[@class="info_left"]/text()').extract_first('') == "作者：":
                # authors(作者)
                item['authors'] = '、'.join(li.xpath('.//a/text()').extract())
            elif li.xpath('./div[@class="info_left"]/text()').extract_first('') == "作者单位：":
                # 作者单位
                item['unit'] = '、'.join(li.xpath('.//a[1]/text()').extract())
            elif li.xpath('./div[@class="info_left"]/text()').extract_first('') == "母体文献：":
                # 母体文献
                item['literature'] = li.xpath('./div[2]/text()').extract_first('')
            elif li.xpath('./div[@class="info_left"]/text()').extract_first('') == "会议名称：":
                # 会议名称
                item['meetingName'] = li.xpath('./div[2]/a[2]/text()').extract_first('')
            elif li.xpath('./div[@class="info_left"]/text()').extract_first('') == "会议时间：":
                # 会议时间
                item['meetingTime'] = li.xpath('./div[2]/text()').extract_first('').replace('\r\n', '').replace('\t',
                                                                                                                '').replace(
                    ' ', '')
            elif li.xpath('./div[@class="info_left"]/text()').extract_first('') == "会议地点：":
                # 会议地点
                item['meetingAdress'] = li.xpath('./div[2]/text()').extract_first('')
            elif li.xpath('./div[@class="info_left"]/text()').extract_first('') == "主办单位：":
                # 主办单位
                item['organizer'] = '、'.join(li.xpath('./div[2]//a/text()').extract())
            elif li.xpath('./div[@class="info_left"]/text()').extract_first('') == "语 种：":
                # 语种
                item['languages'] = li.xpath('./div[2]/text()').extract_first('').replace('\r\n', '').replace('\t', '')
            elif li.xpath('./div[@class="info_left"]/text()').extract_first('') == "分类号：":
                # 分类号
                item['classNumber'] = ''.join(li.xpath('./div[2]/text()').extract()).replace('\r\n', '').replace('\t',
                                                                                                                 '')
            elif li.xpath('./div[@class="info_left"]/text()').extract_first('') == "在线出版日期：":
                # 发布时间
                item['publishTime'] = li.xpath('./div[2]/text()').extract_first('').replace('\r\n', '').replace('\t',
                                                                                                                '').replace(
                    ' ', '')
            elif li.xpath('./div[@class="info_left"]/text()').extract_first('') == "页码：":
                # 页码
                item['pageNumber'] = li.xpath('./div[2]/text()').extract_first('')

        item['searchKey'] = info['searchKeyWord']
        item['searchType'] = info['searchType']
        return item

    def parse_tech(self, response, info):

        item = WanfangTechItem()
        item['url'] = response.url
        # title(中文标题)
        item['title'] = response.xpath('//div[@class="title"]/text()').extract_first('').replace('\r\n', '').replace(
            ' ', '').replace('\t', '')
        # englishTitle(英文标题)
        item['englishTitle'] = response.xpath('//div[@class="English"]/text()').extract_first('暂无').replace('\t', '')
        # content(摘要)
        item['content'] = ''.join(response.xpath('//input[@class="share_summary"]/@value').extract()).replace('\t',
                                                                                                              '').replace(
            ' ', '').replace('\r\n', '')

        lis = response.xpath('//ul[@class="info"]//li')
        print(len(lis))
        for li in lis:
            if li.xpath('./div[@class="info_left"]/text()').extract_first('') == "关键词：":
                # keywords(关键词)
                item['keywords'] = '、'.join(li.xpath('.//a/text()').extract())
            elif li.xpath('./div[@class="info_left"]/text()').extract_first('') == "作者：":
                # authors(作者)
                item['authors'] = '、'.join(li.xpath('.//a/text()').extract())
            elif li.xpath('./div[@class="info_left"]/text()').extract_first('') == "作者单位：":
                # 作者单位
                item['unit'] = '、'.join(li.xpath('.//a[1]/text()').extract())
            elif li.xpath('./div[@class="info_left"]/text()').extract_first('') == "报告类型：":
                # 报告类型
                item['reportType'] = li.xpath('./div[2]/text()').extract_first('')
            elif li.xpath('./div[@class="info_left"]/text()').extract_first('') == "公开范围：":
                # 公开范围
                item['openRange'] = li.xpath('./div[2]/text()').extract_first('')
            elif li.xpath('./div[@class="info_left"]/text()').extract_first('') == "全文页数：":
                # 全文页数
                item['pageNumber'] = li.xpath('./div[2]/text()').extract_first('')
            elif li.xpath('./div[@class="info_left"]/text()').extract_first('') == "项目/课题名称：":
                # 项目/课题名称
                item['projectName'] = li.xpath('./div[2]/text()').extract_first('')
            elif li.xpath('./div[@class="info_left"]/text()').extract_first('') == "计划名称：":
                # 计划名称
                item['planName'] = li.xpath('./div[2]/text()').extract_first('')
            elif li.xpath('./div[@class="info_left"]/text()').extract_first('') == "编制时间：":
                # 编制时间
                item['compileTime'] = li.xpath('./div[2]/text()').extract_first('').replace('\t', '').replace(' ',
                                                                                                              '').replace(
                    '\r\n', '')
            elif li.xpath('./div[@class="info_left"]/text()').extract_first('') == "立项批准年：":
                # 立项批准年
                item['approvalYear'] = li.xpath('./div[2]/text()').extract_first('')
            elif li.xpath('./div[@class="info_left"]/text()').extract_first('') == "馆藏号：":
                # 馆藏号
                item['collection'] = li.xpath('./div[2]/text()').extract_first('')

        item['searchKey'] = info['searchKeyWord']
        item['searchType'] = info['searchType']
        return item



