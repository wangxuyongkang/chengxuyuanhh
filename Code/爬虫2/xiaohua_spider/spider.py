###爬虫主体代码
from xiaohua_spider.downloader import send_request
from xiaohua_spider import app
from lxml import etree
from xiaohua_spider import dupefilter
#入口方法
dp = dupefilter.RFPDupeFilter()
#ignore_result=True 如果celery异步执行的函数没有返回值，默认返回None，则backend会将None存储到redis数据库中，ignore_result=True，忽略结果存储
@app.task(ignore_result=True)
def start_request(url):
    #起始url
    #request_seen
    if  dp.request_seen(url):
        text = send_request(url=url)
        if text:
            parse_page_response.delay(text)
@app.task()
def parse_page_response(text):
    '''解析分页的数据，提取详情url地址,和其他分页url地址href="http://www.xiaohuar.com/p-1-2084.html"'''
    etree_html = etree.HTML(text)
    urls = etree_html.xpath('//div[@class="title"]/span/a/@href')
    for url in urls:
        
        #获取到详情的url地址，发起详情请求
        send_detail_request.delay(url)
    #获取分页url地址
    others_pages = etree_html.xpath('//div[@class="page_num"]/a/@href')
    for page in others_pages:
        start_request.delay(page)
@app.task()
def send_detail_request(url):
    '''根据详情url地址发送请求，获取详情地址'''
    text = send_request(url)
    if text:
        parse_detail_data.delay(text)
def parse_detail_data(text):
    etree_html = etree.HTML(text)
    #解析详情数据
    item = {}
    if 'detail-id' not in text:
        #是需要提取的网页结构
        #姓名
        item['name'] = etree_html.xpath('//div[@class="infodiv"]/table//tr[1]/td[2]/text()')[0]
        #学校名
        item['schoolname'] = etree_html.xpath('//div[@class="infodiv"]/table//tr[5]/td[2]/text()')[0]
        #简介
        item['info'] = ','.join(etree_html.xpath('//div[@class="infocontent"]/p//text()'))
        #美女图片
        item['image'] = etree_html.xpath('//a[@class="imglink"]/img/@src')[0]
    #item 存在
    return item
