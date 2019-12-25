# 什么是xpath？
# xpath(xml path language)是一门在xml文档中查找信息的语言,
# 可以遍历和搜索xml文档中的文本和属性，同样适用于html

# 什么是xml？
# 是一门可扩展的编辑语言，是为了传输数据，内部的标签可自定义，
# xml的结构类似于html


# 安装 lxml库：pip3 install lxml

"""
xpath语法的路径表达式（常用）
nodename（节点名称）   获取此节点下所有的子节点
 /                   获取当前节点下的直接子节点
//                   获取当前节点下的节点，不考虑节点位置
.                    获取当前节点
..                   获取当前节点的父节点
@                    获取属性
"""

#案例：起点中文网

#url：
#https://www.qidian.com/all?
# orderId=&style=1&pageSize=20
# &siteid=1&pubflag=0&hiddenField=0&page=1

#https://www.qidian.com/all?
# orderId=&style=1&pageSize=20
# &siteid=1&pubflag=0&hiddenField=0&page=2

#https://www.qidian.com/all?
# orderId=&style=1&pageSize=20
# &siteid=1&pubflag=0&hiddenField=0&page=3

import requests
from lxml import etree

class QidianSpider(object):

    def __init__(self):
        pass

    def start_request(self,url):

        #构建请求头
        headers = {
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
        }

        # https://www.qidian.com/all?orderId=&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0&page=1
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            print('请求成功')
            self.parse_noval_data(response.text)



    def parse_noval_data(self,htmlData):
        # print(htmlData)
        """
        解析数据
        """
        #把html文档转换为xpath解析对象
        x_html = etree.HTML(htmlData)
        #获取页面的小说列表
        li_list = x_html.xpath('//ul[@class="all-img-list cf"]/li')
        print(len(li_list))
        #遍历，获取每一本小说的内容
        for li in li_list:

            # print(type(li))
            book_info = {}
            #封面图片(去标签的属性@属性明)
            book_info['coverImage'] = 'https:'+li.xpath('./div[@class="book-img-box"]//img/@src')[0]
            #标题(取标签的文本使用text())
            book_info['title'] = li.xpath('./div[@class="book-mid-info"]/h4/a/text()')[0]
            #作者
            book_info['author'] = li.xpath('.//p[@class="author"]/a[@class="name"][1]/text()')[0]
            #分类
            book_info['type'] = li.xpath('.//p[@class="author"]/a[2]/text()')[0] + '|' + li.xpath('.//a[@class="go-sub-type"]/text()')[0]
            #状态
            book_info['status'] = li.xpath('.//p[@class="author"]/span/text()')[0]
            #描述
            book_info['content'] = li.xpath('.//p[@class="intro"]/text()')[0].replace(' ','').replace('\r','')
            print(book_info)

        #nextpage(下一页)
        next_page = x_html.xpath('//a[@class="lbf-pagination-next "]/@href')

        if len(next_page) > 0:
            next_page = 'https:' + next_page[0]
            #继续发起请求
            self.start_request(next_page)
        else:
            print('数据获取完毕了')








if __name__ == '__main__':
    start_url = 'https://www.qidian.com/all?orderId=&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0&page=1'
    qidianspider = QidianSpider()
    qidianspider.start_request(start_url)





