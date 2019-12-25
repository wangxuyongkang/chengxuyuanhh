# -*- coding: utf-8 -*-
import scrapy
import json


class SpiderUsedSpider(scrapy.Spider):
    name = 'spider_used'
    allowed_domains = ['jiayuan.com']
    start_urls = ['http://search.jiayuan.com/v2/search_v2.php']

    # 如果一开始发起的请求是post请求
      #case1：本身获取数据的接口就是post请求
      #case2：网站模拟登录后，获取数据

    def start_requests(self):
        form_data = {
            'sex': 'f',
            'key':'',
            'stc': '1:11,2:20.28,23:1',
            'sn': 'default',
            'sv': '1',
            'p': '2',
            'f': 'search',
            'listStyle': 'bigPhoto',
            'pri_uid': '0',
            'jsversion': 'v5'
        }

        for url in self.start_urls:
            #使用FormRequest发起post请求
            yield scrapy.FormRequest(
                url=url,
                formdata=form_data,
                dont_filter=True,
                meta={'formData':form_data}
            )

    def parse(self, response):
        print(response.status)
        # print(response.text)
        data = response.text.replace('##jiayser##','').replace('//','')
        json_data = json.loads(data)
        # print(json_data)
        #提取json数据
        #....

        #提取完本页面数据之后。构建下一页请求
        formData = response.meta['formData']

        print('当前获取的是',formData['p'],'页')

        formData['p'] = str(int(formData['p'])+1)

        #什么时候停止？
        pageTotal = json_data['pageTotal']

        if int(formData['p']) < int(pageTotal)+1:

            print('下一页',formData)
            yield scrapy.FormRequest(
                response.url,
                formdata=formData,
                callback=self.parse,
                meta={'formData': formData}
            )
