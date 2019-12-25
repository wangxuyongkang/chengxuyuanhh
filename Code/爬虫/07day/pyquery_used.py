# 什么是pyquery？

# 是jquery的python的python实现，同样可以从html文档中提取数据
# ，易用性和解读行都很好。

# 安装：pip3 install pyquery

from pyquery import PyQuery

"""
find(selector) : 使用css选择器查找
filter(selector) : 根据id或者class过滤节点
直接对pyquery对象使用css选择器查找节点
.eq(index) : 根据索引获取指定的节点（从0开始）
.text(): 获取节点的文本
.attr('属性名') ：获取节点的属性
"""

#糗事百科
#目标url：https://www.qiushibaike.com/textnew/
import requests
#exceptions来做异常处理
from requests import exceptions
import pymongo

def qiushiSpider():
    start_url = 'https://www.qiushibaike.com/textnew/'
    start_request(start_url)

def start_request(url):
    #发起请求，获取页面源码
    html,currentUrl = send_request(url)
    if html:
        #解析数据
        nextUrl = parse_page_data(html)
        if nextUrl:
            start_request(nextUrl)
    else:
        print('当前url请求失败',currentUrl)
        #可以在这里继续请求当前页


def send_request(url):
    # 发起请求
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
    }
    try:
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            print('请求成功')
            return response.text,url
    except exceptions.RequestException as err:
        print(err, '请求错误')
    except exceptions.HTTPError as err:
        print(err, 'HTTPError')
    except exceptions.ConnectTimeout as err:
        print(err, '链接超时')
    return None,url

def parse_page_data(html):
    """
    根据页面源码解析数据（pyquery）
    :param html:
    :return:
    """
    #实例化一个PyQuery对象
    pq_html = PyQuery(html)

    #获取段子列表
    #article_divs = pq_html.find('div#content-left > div')
    #article_divs = pq_html.find('div').filter('#content-left').find('div').filter('.article.block.untagged.mb15')
    article_divs = pq_html.find('div').filter('.article.block.untagged.mb15')
    # print(type(article_divs))

    #items() 将PyQuery转为可迭代对象
    for article_div in article_divs.items():
        print(type(article_div))
        article = {}
        # 名称
        # article['name'] = article_div('div.author.clearfix a').eq(1).attr('title')
        article['name'] = article_div('div.author.clearfix a').eq(1)('h2').text()
        #年龄
        article['age'] = article_div('div.articleGender').text()
        #个人主页
        article['personUrl'] = article_div('div.author.clearfix a').eq(1).attr('href')
        #内容
        article['content'] = article_div('div.content > span').text()
        #投票
        article['vote'] = article_div('span.stats-vote > i').text()
        #评论
        article['comments'] = article_div('span.stats-comments a i').text()
        print(article)
        save_data_to_mongo(article)

    #获取下一页地址
    nextUrl = pq_html('span.next').parent().attr('href')
    if nextUrl:
        nextUrl = 'https://www.qiushibaike.com' + nextUrl
        print(nextUrl)
        return nextUrl
    else:
        print('结束')
        return None

def save_data_to_mongo(article):

    try:
        col.insert(article)
    except Exception as err:
        print(err)


if __name__ == '__main__':
    #创建数据库连接
    mongo_client = pymongo.MongoClient(
        host='localhost',port=27017
    )
    #获取要操作的数据库
    db = mongo_client['qiushi']
    #获取要操作的集合
    col = db['new']

    qiushiSpider()







