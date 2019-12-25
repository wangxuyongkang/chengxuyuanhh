# pip3 install lxml
import re,threading
from lxml.html import etree
import requests
from concurrent.futures import ThreadPoolExecutor

#http://all.hengyan.com/1/0_0_0_0_0_0_0_0_0_1.aspx
#http://all.hengyan.com/1/0_0_0_0_0_0_0_0_0_2.aspx
#http://all.hengyan.com/1/0_0_0_0_0_0_0_0_0_3.aspx

class HengYanSpider(object):

    def __init__(self):
        self.first_url = 'http://all.hengyan.com/1/0_0_0_0_0_0_0_0_0_1.aspx'
        self.default_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3722.400 QQBrowser/10.5.3738.400'
        }

    def get_noval_url(self):
        """获取小说详情的url地址"""
        html = self.send_request(self.first_url)
        if html:
            #解析数据(获取xpath解析器)
            etree_html = etree.HTML(html)
            noval_urls = etree_html.xpath('//li[@class="bookname"]/a[1]/@href')

            #涉及到大量的请求任务
            pool = ThreadPoolExecutor(10)

            for noval_url in noval_urls:
                #将任务提交到线程池中，让线程池中的线程执行任务
                result = pool.submit(self.get_noval_detail(noval_url))
                result.add_done_callback(self.get_noval_detail)
        else:
            print('数据获取失败')

    def get_noval_detail(self, noval_url):
        """获取书籍详情的页面内容,解析数据"""
        html = self.send_request(noval_url)
        return html

    def pares_noval_detail(self,future):
        '''解析书籍详情'''
        html = future.result()
        if html:
            # 解析数据(获取xpath解析器)
            etree_html = etree.HTML(html)
            # print('得到了详情页面')
            noval_dict = {}
            # 书号
            book_id = self.extract_first(etree_html.xpath('//div[@class="dh"]/p/label/text()'))
            noval_dict['book_id'] = re.search('\d+', book_id).group()
            # 热度
            noval_dict['hot'] = self.extract_first(etree_html.xpath('//p[@class="wendu"]/b/text()'))
            # 火车票
            noval_dict['hot_track'] = self.extract_first(
                etree_html.xpath('//div[@class="piao"]/p[2]/span[@class="huocolor"]/text()'))
            # 冰票
            noval_dict['bing_track'] = self.extract_first(
                etree_html.xpath('//div[@class="piao"]/p[2]/span[@class="bingcolor"]/text()'))
            # 金笔
            noval_dict['jingbi'] = self.extract_first(etree_html.xpath('//div[@class="jinbi"]//li[1]/p[2]/text()'))
            # 标题
            noval_dict['title'] = self.extract_first(etree_html.xpath('//h2/text()'))
            # 简介
            noval_dict['content'] = self.extract_first(
                etree_html.xpath('//p[@class="intro ih1"]/text()|//p[@class="intro ih2"]/text()')).replace('\u3000','').replace('\r','')
            # 标签
            noval_dict['biaoqian'] = self.extract_first(etree_html.xpath('//p[@class="biaoqian"]/label/text()'))
            #点击量
            noval_dict['dianji'] = self.extract_first(etree_html.xpath('//p[@class="info"]/span[1]/text()'))
            #分类
            noval_dict['category'] = self.extract_first(etree_html.xpath('//p[@class="info"]/span[2]/a/text()'))
            #字数
            noval_dict['zishu'] = self.extract_first(etree_html.xpath('//p[@class="info"]/span[3]/text()'))
            #签约
            noval_dict['qianyue'] = self.extract_first(etree_html.xpath('//p[@class="info"]/span[4]/text()'))
            # 作者
            noval_dict['author'] = self.extract_first(etree_html.xpath('//div[@id="ainfo"]/p/span/a[2]/text()'))
            print(noval_dict)
            self.save_data(noval_dict)
    def save_data(self, noval_dict):
        """保存数据"""
        pass

    def extract_first(self, data, default=''):
        if len(data) > 0:
            return data[0]
        return default



    def send_request(self,url,header=None,data=None,method="GET"):
        """发送请求"""
        header = self.default_headers if not header else header


        if method == 'GET':
            #发送get请求
            response = requests.get(url=url,params=data,headers=header)
        else:
            #发送post请求
            response = requests.post(url=url, data=data, headers=header)

        if response.status_code == 200:
            #请求成功，返回页面源码
            return response.text


if __name__ == '__main__':

    spider = HengYanSpider()
    spider.get_noval_url()







