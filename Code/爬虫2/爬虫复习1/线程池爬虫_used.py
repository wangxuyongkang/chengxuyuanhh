# pip3 install lxml
from lxml.html import etree
import requests,re
from concurrent.futures import ThreadPoolExecutor
import pymysql,threading
#http://all.hengyan.com/1/0_0_0_0_0_0_0_0_0_1.aspx
#http://all.hengyan.com/1/0_0_0_0_0_0_0_0_0_2.aspx
#http://all.hengyan.com/1/0_0_0_0_0_0_0_0_0_3.aspx
#http://all.hengyan.com/1/0_0_0_0_0_0_0_0_0_100.aspx

class HengYanSpider(object):

    def __init__(self):
        self.first_url = 'http://all.hengyan.com/1/0_0_0_0_0_0_0_0_0_1.aspx'
        self.default_headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }
        # host = None, user = None, password = "",
        # database = None, port = 0, unix_socket = None,
        # charset = ''
        self.mysql_client = pymysql.Connect(
            '127.0.0.1','root','ljh1314',
            'class1809',3306,charset='utf8',
        )
        self.cursor = self.mysql_client.cursor()
        self.lock = threading.Lock()

    def get_noval_url(self,url=None):
        url = self.first_url if not url else url
        """获取小说详情的url地址"""
        html = self.send_request(url)
        if html:
            #解析数据(获取xpath解析器)
            etree_html = etree.HTML(html)
            noval_urls = etree_html.xpath('//li[@class="bookname"]/a[1]/@href')

            ####设计到大量的请求任务
            pool = ThreadPoolExecutor(10)
            for noval_url in noval_urls:
                #将任务提交到线程池中，让线程池中的线程执行任务
                result = pool.submit(self.get_noval_detail,noval_url)
                #add_done_callback添加回调方法 执行完毕后返回结果并处理结果
                result.add_done_callback(self.parse_noval_detail)
                # self.get_noval_detail(noval_url)
            # 内部实现了join方法
            pool.shutdown()

            #获取下一页
            if '下一页' in html:
                # 继续获取
                current_page = int(self.extract_first(etree_html.xpath('//span[@class="pageBarCurrentStyle"]/text()'),))
                next_page = current_page+1
                #http://all.hengyan.com/1/0_0_0_0_0_0_0_0_0_1.aspx
                next_url = re.sub('\d+.aspx',str(next_page)+'.aspx',url)
                print('下一页',next_url)
                self.get_noval_url(next_url)

        else:
            print('数据获取失败')

    def get_noval_detail(self,noval_url):
        """获取书籍详情的页面内容,解析数据"""
        html = self.send_request(noval_url)
        return html

    def parse_noval_detail(self,future):
        """解析书籍详情数据"""
        html = future.result()
        if html:
            # 解析数据(获取xpath解析器)
            etree_html = etree.HTML(html)
            # print('得到了详情页面')
            noval_dict = {}
            #书号
            book_id = self.extract_first(etree_html.xpath('//div[@class="dh"]/p/label/text()'))
            noval_dict['book_id'] = re.search('\d+',book_id).group()
            # #热度
            # noval_dict['hot'] = self.extract_first(etree_html.xpath('//p[@class="wendu"]/b/text()'))
            # #火车票
            # noval_dict['hot_track'] = self.extract_first(etree_html.xpath('//div[@class="piao"]/p[2]/span[@class="huocolor"]/text()'))
            # #冰票
            # noval_dict['bing_track'] = self.extract_first(etree_html.xpath('//div[@class="piao"]/p[2]/span[@class="bingcolor"]/text()'))
            # #金笔
            # noval_dict['jingbi'] = self.extract_first(etree_html.xpath('//div[@class="jinbi"]//li[1]/p[2]/text()'))
            #标题
            noval_dict['title'] = self.extract_first(etree_html.xpath('//h2/text()'))
            #简介
            noval_dict['content'] = self.extract_first(etree_html.xpath('//p[@class="intro ih1"]/text()|//p[@class="intro ih2"]/text()'))
            #作者
            noval_dict['author'] = self.extract_first(etree_html.xpath('//div[@id="ainfo"]/p/span/a[2]/text()'))

            print(noval_dict)
            self.save_data(noval_dict)


    def save_data(self,noval_dict):
        """保存数据"""
        sql_str = """
        INSERT INTO henyan(%s)
        VALUES (%s)
        """ % (
            ','.join(noval_dict.keys()), #=>"author,content,..."
            ','.join(['%s']*len(noval_dict))
        )
        # 枷锁
        self.lock.acquire()
        try:
            self.cursor.execute(sql_str,list(noval_dict.values()))
            self.mysql_client.commit()
        except Exception as err:
            print(err)
            self.mysql_client.rollback()
        # 解锁
        self.lock.release()

    def extract_first(self,data,default=''):
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







