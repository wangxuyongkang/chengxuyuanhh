import requests
from lxml import etree
import pymysql


class GaoKao(object):

    def first(self,list):
        return list[0] if len(list) == 1 else None

    def start_request(self, url, headers):
        """起始请求"""
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            self.parser(response.text)
        else:
            print('请求失败')

    def parser(self, text):
        html_text = etree.HTML(text)
        dl_htmls = html_text.xpath('//div[@class="scores_List"]/dl')
        dict_html = {}
        for dl_html in dl_htmls:
            dict_html['image'] = dl_html.xpath('.//dt/a/img/@src')[0]
            dict_html['detail_url'] = dl_html.xpath('.//dt/a/@href')[0]
            dict_html['school'] = dl_html.xpath('.//dt/strong/a/text()')[0]
            dict_html['home'] = dl_html.xpath('.//dd/ul/li[1]/text()')[0]
            dict_html['features'] = '/'.join(dl_html.xpath('.//dd/ul/li[2]/span/text()'))
            dict_html['type'] = dl_html.xpath('.//dd/ul/li[3]/text()')[0]
            dict_html['Belongto'] = dl_html.xpath('.//dd/ul/li[4]/text()')[0]
            dict_html['nature'] = dl_html.xpath('.//dd/ul/li[5]/text()')[0]
            dict_html['school_url'] = dl_html.xpath('.//dd/ul/li[6]/text()')[0]
            dict_html['next'] = self.first(dl_html.xpath('//ul[@class="fany"]/li[3]/a/@href'))
            if dict_html['detail_url']:
                self.detail_html(url=dict_html['detail_url'],headers=headers,dict_html=dict_html)
            if dict_html['next']:
                self.start_request(url=dict_html['next'],headers=headers)
            else:
                print('提取完毕')
    def detail_html(self,url,headers,**kwargs):
        response = requests.get(url=url,headers=headers)
        if response.status_code == 200:
            text = response.text
            html = etree.HTML(text)
            kwargs = kwargs.get('dict_html')
            detailhtmls = html.xpath('//div[@class="college_msg bk"]/dl')
            for detailhtml in detailhtmls:
                kwargs['professor'] = '/'.join(detailhtml.xpath('//ul[@class="left basic_infor"]/li[4]/text()'))
                kwargs['contact'] = '/'.join(detailhtml.xpath('//dd/ul[@class="left contact"]/p/text()')).replace('\r\n\t\u3000\u3000','').replace('\u3000\u3000','')
                kwargs['info'] = detailhtml.xpath('//div[@class="sm_nav bk"]/p[1]/a/@href')[0]
                if kwargs['info']:
                    info = requests.get(url=kwargs['info'],headers=headers)
                    text = info.text
                    html = etree.HTML(text)
                    kwargs['jieshao'] = ' '.join(html.xpath('//div[@class="jj"]/p[2]/text()')).replace('\r\n\t','').replace('\r\n\t\u3000\u3000','').replace('\u3000\u3000','')
                    dict = kwargs
                print(dict['school'])
                self.db_save_data(dict)

    def db_save_data(self,dict_html):
        insert_sql = """
            INSERT INTO gaokao (%s)
            VALUES (%s)
            """ % (','.join(dict_html.keys()), ','.join(['%s'] * len(dict_html)))
        try:
            cursor.execute(insert_sql, list(dict_html.values()))
            mysql_client.commit()
        except Exception as err:
            print(err)
            mysql_client.rollback()
    # def all(self,):
if __name__ == '__main__':
    mysql_client = pymysql.Connect(
        '127.0.0.1', 'root', '123456',
        'class1809', charset='utf8'
    )
    # 创建游标
    cursor = mysql_client.cursor()
    url = 'http://college.gaokao.com/schlist/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3722.400 QQBrowser/10.5.3771.400'}

    gaokao = GaoKao()
    gaokao.start_request(url,headers)
