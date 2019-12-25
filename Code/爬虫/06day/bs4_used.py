#Beautifulsoup4?
# 是python的一个xml和html的解析器，目的是从xml或
# html中提取数据

#安装 pip3 install beautifulsoup4

# beautifulsoup4 要比xpath解析数据要慢，因为beautifulsoup4载入的是
# 整个html文档

"""
findall() 查找所有节点
find() 查找单个
支持css选择器

获取标签的属性 p['class'] => p.attrs['class']
获取标签的文本 p.get_text() => p.string
"""

#腾讯招聘为例
# 首页url地址
#https://hr.tencent.com/position.php

import requests
from bs4 import BeautifulSoup


def tenXunJobSpider():
    start_url = 'https://hr.tencent.com/position.php'
    html = start_request(start_url)
    parse_job_list(html)

def start_request(start_url):
    """
    发起请求
    :param start_url: 目标url地址
    :return:
    """
    #构建请求头
    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
    }
    response = requests.get(url=start_url,headers=headers)

    if response.status_code == 200:
        print('请求成功')
        html = response.text
        return html

def parse_job_list(htmlData):

    #实例化BeautifulSoup对象
    """
    markup="":html页面源码
    features:制定解析器
    注意：使用BeautifulSoup需要依赖其他解析器
         'lxml' 表示使用的是lxml下的html解析器  容错性好，可读性强
         'html.parser' 是python内置的解析器
    :param htmlData:
    :return:
    """
    html_soup = BeautifulSoup(htmlData,features='lxml')
    """
    name=None, 设置要获取的节点名称
    attrs={}, 是一个字典类型，设置标签的属性
    limit=None, 限制返回的条数
    text 字符串，查找符合text文本的字符串，并返回
    """
    tr_even = html_soup.find_all(name='tr',attrs={'class':'even'})
    tr_odd = html_soup.find_all(name='tr',attrs={'class':'odd'})
    # print(tr_even,tr_odd)

    for tr in tr_even+tr_odd:
        # print(tr)
        #css选择器
        # detail_url = tr.select('.l.square a')[0]['href']
        detail_url = 'https://hr.tencent.com/' + tr.select('.l.square a')[0].attrs['href']
        #print(detail_url)
        html = start_request(detail_url)
        parse_detail_data(html)

    #获取下一页url地址
    next_url = html_soup.select('a#next')[0]['href']
    if 'javascript:;' in next_url:
        print('职位数据获取完毕了')
    else:
        next_url = 'https://hr.tencent.com/' + next_url
        html = start_request(next_url)
        parse_job_list(html)

def parse_detail_data(html):

    #实例化BeautifulSoup对像
    html_soup = BeautifulSoup(html,features='lxml')

    job_info = {}

    #获取标题
    # title = html_soup.find_all(name='td',attrs={'id':'sharetitle'})[0].get_text()
    # title = html_soup.find_all(id='sharetitle')[0].string
    job_info['title'] = html_soup.select('td#sharetitle')[0].get_text()
    # 地址
    # adress = html_soup.find_all(name='span',attrs={'class':'lightblue l2'})[0].get_text()
    # adress = html_soup.find_all(class_='lightblue l2')[0].string
    job_info['adress'] = html_soup.select('tr.c.bottomline td')[0].get_text()
    #职位类别
    job_info['jobType'] = html_soup.select('tr.c.bottomline td')[1].get_text()
    #招聘人数
    job_info['needPeople'] = html_soup.select('tr.c.bottomline td')[2].get_text()
    #工作职责
    responsibilities_li = html_soup.select('ul.squareli')[0].select('li')
    responsibilities = ''
    for li in responsibilities_li:
        responsibilities = responsibilities + li.get_text()
    job_info['responsibilities'] = responsibilities
    #工作要求
    requirements_li = html_soup.select('ul.squareli')[1].select('li')
    requirements = ''
    for li in requirements_li:
        requirements = requirements + li.get_text()
    job_info['requirements'] = requirements

    print(job_info)








if __name__ == '__main__':
    tenXunJobSpider()