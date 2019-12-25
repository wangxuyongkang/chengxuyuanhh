#什么是xpath?
#xpath(xml path language)是一门在xml文档中找找信息的语言
#可以便利和搜索xml文档的文本和属性,同样适应于html

#什么是xml?
#是一门可口站的编辑语言,是为了传输数据,内部的标签可自定义
#xml的结构类似于html

#安装 lxml库: pip3 install lxml
# xpath语法的路径表达式(常用)
# nodename （节点名称） 获取此节点下所有的子节点
# /                     获取当前节点下的直接子节点
# //                    获取当前节点下的节点，不考虑节点位置
# .                     获取当前节点
# ..                    获取当前的节点的父节点
# @                     获取属性


"""
案例:起点中文网

"""
#第二页
#url:https://www.qidian.com/all?
# orderId=&style=1&pageSize=20
# &siteid=1&pubflag=0&hiddenField=0&page=2
#第三页
#https://www.qidian.com/all?
# orderId=&style=1&pageSize=20
# &siteid=1&pubflag=0&hiddenField=0&page=3

import requests
from lxml import etree


class QdianSpider(object):
    def __index__(self):
        pass
    def start_request(self,url):
        #发起请求
        #创建请求头
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6788.400 QQBrowser/10.3.2727.400'
        }
        # url:https://www.qidian.com/all?orderId=&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0&page=1

        response = requests.get(url,headers= headers)
        if response.status_code == 200:
            print('请求成功')
            self.parse_noval_data(response.text)

    def parse_noval_data(self,htmlData):
        #print(htmlData)

        """
        分析数据
        """
        #把html文档转换为xpath解析对象
        x_html = etree.HTML(htmlData)
        #获取小说页面列表
        li_list = x_html.xpath('//ul[@class="all-img-list cf"]/li')
        print(len(li_list))
        #遍历，获取每本小说的内容
        for li in li_list:
            #封面图片
            book_info = {}
            #取标签属性@+属性名
            book_info['coverImage'] = 'https:'+ li.xpath('./div[@class="book-img-box"]//img/@src')[0]
            #取文本使用text
            book_info['title'] = li.xpath('./div[@class="book-mid-info"]/h4/a/text()')[0]
            #取作者
            book_info['author'] = li.xpath('.//p[@class="author"]/a[@class="name"][1]/text()')[0]
            print(book_info)


if __name__ == '__main__':
    start_url = 'https://www.qidian.com/all?orderId=&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0&page=1'
    qidianSpider = QdianSpider()
    qidianSpider.start_request(start_url)
