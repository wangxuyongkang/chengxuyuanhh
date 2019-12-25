import requests
from lxml.html import etree
import json,re

class JDspider(object):
    def __init__(self):
        pass


    def strat_url(self,url):
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6788.400 QQBrowser/10.3.2727.400'
        }
        response = requests.get(url=url,headers=headers)
        if response.status_code == 200:

            print('请求成功')
            html = response.text

            x_html = etree.HTML(html)
            lis = x_html.xpath('//ul[@class="parameter2 p-parameter-list"]/li')

            if len(lis) > 0:
                # self.parse_the_data(html)
                self.send_the_data(html)
            else:
                # cont = response.content
                # cont_str = cont.decode('utf-8')
                self.parese_html(response.text)

    def send_the_data(self, html):
        # commodity_id = re.findall('.*?/(\d+)\.html', comm_id)
        x_html = etree.HTML(html)
        li_list = x_html.xpath('//ul[@class="parameter2 p-parameter-list"]/li[2]/text()')[0]
        # print(li_list)
        comm_id = re.findall('.*?(\d+)', li_list)
        # print(comm_id)
        comment_url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv120885&productId=%s&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1' % (
            comm_id[0])
        # print(comment_url)
        self.parese_html(comment_url)


    def parese_html(self,content):
        json_html = content.text.replace('fetchJSON_comment98vv120888(', '').replace(')', '').replace(';', '')
        json_html = json.loads(json_html)
        # json_html = json_html['comments']
        print(json_html)
        # self.parese_html(json_html['comments'])
        json_html = json_html['comments']
        for html in json_html:
           # for into in html:
            comment={}
            comment['user'] = html['nickname']
            comment['content'] = html['content']
            comment['cover'] = html['productColor']
            comment['size'] = html['productSize']
            comment['memory'] = html['productSales'][0]['saleValue']
            comment['time'] = html['referenceTime']
            comment['give'] = html['usefulVoteCount']
            comment['coment'] = html['replyCount']
            print(comment)
            # self.file_data(comment)
            with open('jd.json', 'w') as file:
                file.write(comment)
    # def file_data(self,comment):


if __name__ == '__main__':
    #https://sclub.jd.com/comment/productPageComments.action?
    #callback=fetchJSON_comment98vv120888&productId=5089253&
    # score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1
    url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv120888&productId=5089253&score=0&sortType=5&page=0s&pageSize=10&isShadowSku=0&rid=0&fold=1'
    #https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv120888&productId=5089253&score=0&sortType=5&page=1&pageSize=10&isShadowSku=0&rid=0&fold=1
    qiche_url = JDspider()
    qiche_url.strat_url(url)



