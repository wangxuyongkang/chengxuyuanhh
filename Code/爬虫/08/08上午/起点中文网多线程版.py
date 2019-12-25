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
from concurrent.futures import ThreadPoolExecutor

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
        """
        解析每一页的书籍列表
        :param htmlData:
        :return:
        """
        # print(htmlData)
        """
        解析数据
        """
        #把html文档转换为xpath解析对象
        x_html = etree.HTML(htmlData)
        #获取页面的小说列表
        li_list = x_html.xpath('//ul[@class="all-img-list cf"]/li')
        print(len(li_list))
        novalPool = ThreadPoolExecutor(10)
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
            # print(book_info)

            #详情的url地址
            # 书籍详情的章节目录url地址
            # https://book.qidian.com/info/1010734492#Catalog
            detail_url = li.xpath('./div[@class="book-mid-info"]/h4/a/@href')[0]
            detail_url = 'https:'+detail_url+'#Catalog'
            # print(detail_url)
            # #根据数据详情的url发请求，获取html页面源码
            # html = self.send_request(detail_url)
            # #解析书籍详情中的章节目录
            # self.parse_chpater_list(html)
            result = novalPool.submit(self.send_request,detail_url)
            #线程执行完毕之后的回调
            result.add_done_callback(self.parse_chpater_list)
        novalPool.shutdown()
        #nextpage(下一页)
        next_page = x_html.xpath('//a[@class="lbf-pagination-next "]/@href')

        if len(next_page) > 0:
            next_page = 'https:' + next_page[0]
            #继续发起请求
            self.start_request(next_page)
        else:
            print('数据获取完毕了')

    def send_request(self,url):
        #构建请求头
        headers = {
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
        }
        response = requests.get(url=url,headers=headers,verify=True)
        if response.status_code == 200:
            print('书籍详情请求成功')
            return response.text

    # def parse_chpater_list(self,html):
    def parse_chpater_list(self, futures):
        #获取线程执行完毕后的返回结果
        html = futures.result()
        #实例化一个xpath的解析对象
        x_html = etree.HTML(html)

        #提取章节目录
        div_volume = x_html.xpath('.//div[@class="volume"]')

        #创建一个线程池（爬取章节详情信息）
        chpaterPool = ThreadPoolExecutor(10)
        if len(div_volume) > 0:
            print('说明是静态页面')
            for div in div_volume:
                isFree = div.xpath('./h3/span/text()')[0].replace(' ','')
                if '免费' in isFree:
                    # print('这个div存放的免费章节')
                    chpater_lis = div.xpath('./ul[@class="cf"]/li')
                    for chpater_li in chpater_lis:
                        chpater_url = 'https:'+chpater_li.xpath('./a/@href')[0]
                        # print(chpater_url)
                        # html = self.send_request(chpater_url)
                        # self.parse_chpater_detail(html)
                        result = chpaterPool.submit(self.send_request,chpater_url)
                        result.add_done_callback(self.parse_chpater_detail)
        else:
            print('当前小说章节目录是动态加载的')
        #内部相当于执行了join()（阻塞线程，确保线程线程中的任务
        # 执行完毕后，然后回到主线程继续操作）
        chpaterPool.shutdown()

    # def parse_chpater_detail(self,html):
    def parse_chpater_detail(self, futures):

        html = futures.result()

        x_html = etree.HTML(html)
        chpaterInfo = {}
        # 章节标题
        chpaterInfo['title'] = x_html.xpath('//h3[@class="j_chapterName"]/text()')[0]
        #书籍名称
        chpaterInfo['novalTitle'] = x_html.xpath('//div[@class="info fl"]/a[1]/text()')[0]
        #书籍内容
        chpaterInfo['content'] = ''.join(x_html.xpath('//div[@class="read-content j_readContent"]/p/text()')).replace('\u3000','')

        print(chpaterInfo)










if __name__ == '__main__':
    start_url = 'https://www.qidian.com/all?orderId=&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0&page=1'
    qidianspider = QidianSpider()
    qidianspider.start_request(start_url)





