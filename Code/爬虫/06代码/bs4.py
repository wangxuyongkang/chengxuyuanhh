# Beautifulsoup4?
# 是python的一个xml和html的解析器,目的是从xml或html中提取数据

# 安装: pip3 install beautifulsoup4

# beautifulsoup4 要比xpath解析数据要慢,因为beautifulsoup4载入的是整个html
"""
indall()方法 查找所有节点

find()方法 查找单个

支持css选择器

获取标签属性 p['class'] => p.attrs['class']
获取标签的文本 p.get_text() => p.string

"""
import requests
from bs4 import BeautifulSoup


def tenXunjobSpider():
    start_url = 'https://hr.tencent.com/position.php'
    html = start_request(start_url)
    parse_job_list(html)

def start_request(start_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6788.400 QQBrowser/10.3.2727.400'
    }
    response = requests.get(url=start_url, headers=headers)
    if response.status_code == 200:
        print('请求成功')
        html = response.text
        return html


def parse_job_list(htmlData):
    html_soup = BeautifulSoup(htmlData, features='lxml')
    tr_even = html_soup.find_all(name='tr', attrs={'class': 'even'})
    tr_odd = html_soup.find_all(name='tr', attrs={'class': 'odd'})
    for tr in tr_even + tr_odd:
        # css选择器
        #detail_url = tr.select('.l.square a')[0]['href']
        detail_url = 'https://hr.tencent.com/' + tr.select('.l.square a')[0].attrs['href']
        print(detail_url)
        html = start_request(detail_url)

def parse_detail_data(html):
    #实例化一个BeautifulSoup对象
    html_soup = BeautifulSoup(html, features='lxml')
    #获取标题
    # title = html_soup.find_all(name='td',attrs={'id':'sharetitle'})[0].get_text()
    # title = html_soup.find_all(id='sharetitle')[0].string
    title = html_soup.select('td#sharetitle')[0].get_text()
    #获取
    adress = html_soup.find_all(name='span',attrs={'class':'lightblue l2'})[0].get_text()
    adress = html_soup.find_all(class_='lightblue l2')[0].string
    print(title)

if __name__ == '__main__':
    tenXunjobSpider()
