# https://www.autohome.com.cn/all/
# xpath

import requests
from lxml import etree


class Qiche(object):
    def __init__(self):
        pass

    def start_request(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6788.400 QQBrowser/10.3.2727.400'
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            print('请求成功')
            html_utf = response.content.decode('gb2312')
            htmlData = html_utf
            # response.text获取文章
            self.parse_noval_data(htmlData)

    def parse_noval_data(self, htmlData):
        x_html = etree.HTML(htmlData)
        # 获取当前列表
        list_Data = x_html.xpath('//div[@class="article-wrapper"]/ul/li')
        print(len(list_Data))
        for li_data in list_Data:
            for li in li_data:
                info = {}
                info['Img'] = 'https:' + li.xpath('.//div[@class="article-pic"]/img/@src')[0]
                info['title'] = li.xpath('.//h3/text()')[0]
                info['minutes'] = li.xpath('.//div[@class="article-bar"]/span[1]/text()')[0]
                info['views'] = li.xpath('.//div[@class="article-bar"]/span[@class="fn-right"]/em[1]/text()')[0]
                info['comments'] = li.xpath('.//div[@class="article-bar"]/span[@class="fn-right"]/em[2]/text()')[0]
                info['content'] = li.xpath('.//p/text()')[0]
                print(info)
                # 获取下一页url地址
                #next_url = info.('page-item-next')[0]['href']
        #         next_page = li.xpath('//a[class="page-item-next"]/@href')
        #         global next_page
        # if next_page == 'javascript:void(0);':
        #     print('请求完毕')
        # else:
        #     next_page = 'https://www.autohome.com.cn'+next_page[0]
        #     self.start_request(next_page)



if __name__ == '__main__':
    start_url = 'https://www.autohome.com.cn/all/'
    qiche_url = Qiche()
    qiche_url.start_request(start_url)
