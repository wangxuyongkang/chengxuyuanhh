import requests
from lxml import etree
import pymysql
#https://www.liepin.com/zhaopin/?sfrom=click-pc_homepage-centre_searchbox-search_new&d_sfrom=search_fp&key=python

def first(list):
    return list[0] if len(list) == 1 else None

def start_request(url,headers=None):
    if headers == None:
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3722.400 QQBrowser/10.5.3771.400'
        }
    response = requests.get(url=url,headers=headers)
    if response.status_code == 200:
        parsm_data(response.text,headers)
    else:
        print('请求错误')

def parsm_data(text,headers):
    item_html = etree.HTML(text)
    item_lists = item_html.xpath('//div[@class="sojob-result "]/ul/li')
    detail_url = item_html.xpath('//div[@class="pagerbar"]/a[8]/@href')
    #https://www.liepin.com/zhaopin/?init=-1&headckid=0a5faa810e36d355&fromSearchBtn=2&ckid=09f02651f6764dd6&degradeFlag=0&sfrom=click-pc_homepage-centre_searchbox-search_new&key=python&siTag=I-7rQ0e90mv8a37po7dV3Q%7EfA9rXquZc5IkJpXC-Ycixw&d_sfrom=search_fp&d_ckId=f0d91893e029a9373594f994a732f7f1&d_curPage=2&d_pageSize=40&d_headId=f0d91893e029a9373594f994a732f7f1&curPage=3
    # https://www.liepin.com/zhaopin/zhaopin/?init=-1&headckid=65fbfed2b498faed&fromSearchBtn=2&sfrom=click-pc_homepage-centre_searchbox-search_new&ckid=65fbfed2b498faed&degradeFlag=0&key=python&siTag=I-7rQ0e90mv8a37po7dV3Q%7EfA9rXquZc5IkJpXC-Ycixw&d_sfrom=search_fp&d_ckId=54496d2893f1cffe48fd31b9611c43ea&d_curPage=0&d_pageSize=40&d_headId=54496d2893f1cffe48fd31b9611c43ea&curPage=1
    print(len(detail_url),detail_url)
    print(len(item_lists))
    for item_list in item_lists:
        url = item_list.xpath('.//div[@class="sojob-item-main clearfix"]/div/h3/a/@href')[0]
        if not url.startswith('https'):
            url = 'https://www.liepin.com'+url
        print(url)
        detail(url,headers)
    #判断是否有下一页,有就发起请求
    if detail_url == 'javascript:;':
        print('数据提取完毕！')
    else:
        detail_next = item_html.xpath('//div[@class="pagerbar"]/a[8]/text()')[0]
    # 下一页url
        detail_url = 'https://www.liepin.com' + str(detail_url[0])
        start_request(url=detail_url)
#javascript:;下一页href == javascript:;说明没有url了

def detail(url,headers):
    if headers  == None:
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3722.400 QQBrowser/10.5.3771.400'
        }
    response = requests.get(url=url,headers=headers)
    if response.status_code == 200:
        item_detail = response.text
        detail_htmls = etree.HTML(item_detail)
        item_datas = detail_htmls.xpath('//div[@class="about-position"]//div')
        #公司信息
        companys = detail_htmls.xpath('//div[@class="right-blcok-post"]')
        #应聘信息
        dict_html = {}
        for item_data in item_datas:
            #职位
            dict_html['position'] = first(item_data.xpath('//div[@class="title-info"]/h1/text()'))
            if dict_html['position'] == None:
                dict_html['position'] = 'python工程师'
            #薪资
            dict_html['salary'] = item_data.xpath('//div[@class="job-title-left"]/p[1]/text()')[0].replace('\r\n',' ').replace(' ','')
            #地点
            # dict_html['place'] = item_data.xpath('//p[@class="basic-infor"]/span/text()')[0]
            #要求
            dict_html['requirements'] = '/'.join(item_data.xpath('//div[@class="job-qualifications"]/span/text()'))
            #福利
            dict_html['welfare'] = '/'.join(item_data.xpath('//ul[@class="comp-tag-list clearfix"]/li/span/text()'))
            #职位描述
            dict_html['describes'] = ' '.join(item_data.xpath('//div[@class="content content-word"]/text()')).replace('\r\n',' ').replace(' ','')
        for company in companys:
            #公司名称
            dict_html['company'] = first(company.xpath('.//div[@class="company-logo"]/p/a/text()'))
            if dict_html['company'] == None:
                dict_html['company'] = company.xpath('.//p[@class="company-name"]/@title')
            #公司地址
            dict_html['company_url'] = first(company.xpath('.//div[@class="company-logo"]/p/a/@href'))
            if dict_html['company_url'] == None:
                dict_html['company_url'] = '暂无'
        db_save_data(dict_html)
def db_save_data(dict_html):
    insert_sql = """
            INSERT INTO liepin (%s)
            VALUES (%s)
            """ % (','.join(dict_html.keys()), ','.join(['%s'] * len(dict_html)))
    try:
        cursor.execute(insert_sql, list(dict_html.values()))
        mysql_client.commit()
    except Exception as err:
        print(err)
        mysql_client.rollback()

if __name__ == '__main__':
    mysql_client = pymysql.Connect(
        '127.0.0.1', 'root', '123456',
        'class1809', charset='utf8'
    )
    # 创建游标
    cursor = mysql_client.cursor()
    url = 'https://www.liepin.com/zhaopin/?sfrom=click-pc_homepage-centre_searchbox-search_new&d_sfrom=search_fp&key=python'
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3722.400 QQBrowser/10.5.3771.400'
    }
    start_request(url=url,headers=headers)

