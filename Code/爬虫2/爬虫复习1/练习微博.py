import requests
from lxml import etree
from urllib import parse
import json
import re
import threading
from concurrent.futures import ThreadPoolExecutor

class Weibo(object):

    def __init__(self):
        pass
    #发起请求
    def start_url(self,url):
        print('正在爬去当前网页',url)
        response_text = self.send_request(url)
        if response_text:
            self.parse_html(response_text,url)


    # 发起请求
    def send_request(self,url,headers=None,allow_redirects=True,meta=None):

        if headers == None:
            headers = {
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
                'Cookie':'SINAGLOBAL=1246150059751.9626.1551868064779; wvr=6; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhpiuX7fRIoGoiFVcgO_J6O5JpX5KMhUgL.FoqfShn7e0n0eKB2dJLoIp-LxKML12-L12zLxKqLBoMLB.SpUN2t; ALF=1596508921; SSOLoginState=1564972922; SCF=Aq_L6nPQ-mXek5g3Sh-jn18o2htx_09uE-48q9rfzLfi5D8YJ_Nh5MHqj3M76slh8UmJYktgRkBAsSx0TLcClo4.; SUB=_2A25wQ-cqDeRhGeBL71oR8ybPyjiIHXVTOV_irDV8PUNbmtAKLRj9kW9NRx3ztg-OWIptrzgbr4nFuP5i_cVzRMvl; SUHB=0mxEyhlRid6ZD3; _s_tentry=login.sina.com.cn; UOR=www.mobiletrain.org,widget.weibo.com,login.sina.com.cn; Apache=173805603940.53558.1564972878299; ULV=1564972878710:5:3:2:173805603940.53558.1564972878299:1564904896991; webim_unReadCount=%7B%22time%22%3A1565004371901%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A12%2C%22msgbox%22%3A0%7D; WBStorage=edfd723f2928ec64|undefined'
            }
        try:
            response = requests.get(url,headers=headers,allow_redirects=allow_redirects,verify=True)
            if response.status_code == 200:
                return response.text
            elif response.status_code == 302:
                if not allow_redirects:
                    return response.text,response.headers,meta
        except Exception as err:
            print(err)
            print('请求失败')

    #添加线程池 使爬虫更高效
    def parse_html(self,text,current):

        # with open('sadsad.html','w',encoding='utf-8') as file:
        #     file.write(text)
        x_html = etree.HTML(text)
        weibo_list = x_html.xpath('//div[@class="card-wrap"]/div[@class="card"]')
        print(len(weibo_list))

        # 线程池 15个
        pool = ThreadPoolExecutor(15)
        for weibo in weibo_list:
            weibo_dict = {}
            weibo_dict['title'] = weibo.xpath('.//div[@class="content"]//a[@class="name"]/text()')[0]
            weibo_dict['content'] = ''.join(weibo.xpath('.//div[@class="content"]/p[@class="txt"]/text()')[0]).replace('\n','').replace(' ','')
            weibo_dict['datatime'] = weibo.xpath('.//div[@class="content"]/p[@class="from"]/a[1]/text()')[0].replace('\n','').replace(' ','')
            # weibo_dict['laizi'] = weibo.xpath('.//div[@class="content"]/p[@class="from"]/a[2]/text()')[0]
            # print(weibo_dict)

            # 个人主页
            detail_url = 'https:' + weibo.xpath('.//div[@class="content"]//a[@class="name"]/@href')[0]
            print(detail_url)

            # text, headers = self.send_request(detail_url, allow_redirects=False)
            #submit将任务 交给 send_request 发起请求 ,跟上参数
            result = pool.submit(self.send_request,detail_url,allow_redirects=False,meta=weibo_dict)
            #请求完毕后 回调到解析数据方法中
            result.add_done_callback(self.parse_prifile_page)
        #阻塞任务执行完毕为止
        pool.shutdown()

        # 获取下一页：
        next = x_html.xpath('//div[@class="m-page"]//a[@class="next"][1]/@href')
        if next:
            next = parse.urljoin(current, next[0])
            print(next)
            self.start_url(next)

    # 解析数据 回调方法
    def parse_prifile_page(self,future):
        # text,headers = future.result()
        result = future.result()#响应头参数取法
        text = result[0]
        headers = result[1]
        meta = result[2]

        detail_url = parse.urljoin(
            'https://weibo.com/ycrsksw?refer_flag=1001030103_&is_hot=1',
            headers['Location']
        )
        print(detail_url)

        detail_html = self.send_request(detail_url)

        pattern = re.compile('<script>FM.view\(({.*?})\)</script>', re.S)
        result = re.findall(pattern, detail_html)
        if len(result) > 0:
            for item in result:
                item = item.replace('<script>FM.view(', '').replace(')</script>', '').replace('<!--欧盟隐私协议弹窗-->',
                                                                                              '').replace(
                    ';</script>', '').replace('\n', '')
                try:
                    json_data = json.loads(item)
                    html = json_data.get('html', '')
                    if 'tb_counter' in html:
                        # print(html)
                        profile_etree = etree.HTML(html)
                        nums = profile_etree.xpath(
                            '//table[@class="tb_counter"]//td[@class="S_line1"]//strong[1]/text()')
                        meta['num1'] = nums[0]
                        meta['num2'] = nums[1]
                        meta['num3'] = nums[2]

                        # print(nums)
                        # #关注量
                    elif 'ul_detail' in html:
                        # print('个人简介部分的html')
                        profile_etree = etree.HTML(html)
                        # 解析个人信息
                        content_ul = profile_etree.xpath('//ul[@class="ul_detail"]')
                        print(len(content_ul))
                except Exception as err:
                    print('json数据异常', err)

        print('微博信息',meta)

if __name__ == '__main__':


    # 设置搜索关键字
    key = parse.quote('成都七中食品')

    url = 'https://s.weibo.com/weibo?q=%s&wvr=6&b=1&Refer=SWeibo_box&page=1' % (key,)

    weibo = Weibo()
    weibo.start_url(url=url)

